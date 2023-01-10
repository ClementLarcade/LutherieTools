from operator import index
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import hankel, svd
from scipy.signal import decimate
import json
from codecs import open
from functools import wraps


""""
Ester : calculer la matrice U depuis ESPRIT
puis en fonction d'une variable de choix d'algo d'estimation 
appeler ESTER depuis ESPRIT en fournissant U

retourner J en sortie de ESPRIT

de manière générale : appeler l'algo d'estimation depuis ESPRIT
"""

def memoize(func):
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        
        if key not in cache:
            cache[key] = func(*args, **kwargs)
            
        return cache[key]

    return wrapper 


def exportJson(mat: np.ndarray,
               file_path: str
               ) -> None:
    """
    Pour exporter les matrices résultats sous forme de fichier .json

    Args:
        mat (np.ndarray): La matrice à exporter
        file_path (str): Le chemin où exporter
    """    
    matList = mat.tolist()# nested lists with same data, indices
    
    json.dump(matList, 
              open(file_path, 'w', encoding='utf-8'), 
              separators=(',', ':'), 
              sort_keys=True, 
              indent=4) ### this saves the array in .json format
    
    return 


def decimation(signal: np.ndarray,
               samplerate: int,
               newSamplerate: int
               ) -> tuple[np.ndarray, int]:
    
    facteur: int = int(samplerate/newSamplerate)
    signal = decimate(signal, facteur, ftype = 'fir') # fonction scipy
    
    
    return signal, newSamplerate


def seuil(inputArray: np.ndarray,
          seuil: float
          ) -> np.ndarray:
    
    array: np.ndarray = np.zeros_like(inputArray)    
    
    for (i,j), x in np.ndenumerate(inputArray):
        if x < seuil:
            array[i,j] = np.NaN
        else:
            array[i,j] = x
            
    return array

@memoize
def ESTER(W: np.ndarray, nbPolesMax: int) -> np.ndarray:
        
    J: np.ndarray = np.zeros(nbPolesMax)
    
    for poles in range(nbPolesMax):
        
        Ws: np.ndarray = W[:, 0: poles+1]
        Wup: np.ndarray = Ws[1::, :]
        Wdown: np.ndarray = Ws[0: -1, :]
        
        phi: np.ndarray = np.linalg.pinv(Wdown) @ Wup
        E: np.ndarray = Wup - Wdown @ phi
        
        J[poles] = 1/(np.linalg.norm(E, 2)**2)
        
    return J
    

@memoize #utiliser pour accélerer l'algorithme ESPRIT en réutilisant les valeurs déja calculées
def ESPRIT(signal: np.ndarray, nbPoles: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Appel de l'algorithme ESPRIT pour la détermination des paramêtres du signal
    Appelle également l'algorithme d'estimation ESTER pour déterminer l'ordre du modèle

    Args:
        signal (np.ndarray): Signal à étudier 
        nbPoles (int): nombre de pôles à déterminer

    Returns:
        np.ndarray, np.ndarray: les matrices Z (ESPRIT) et J (ESTER)
    """    
    # contient également l'implémentation du critère ESTER 
    
    N: int = signal.shape[0]

    M: int = int(N/3)
    L: int = N - M + 1 # M vaut N /3 et l vaut horizon - M + 1

    H: np.ndarray = hankel(signal[0 : M], signal[L : -1])
    C: np.ndarray =  1/L * H @ H.T
  
    W, _V, _L = svd(C, full_matrices=False)
    del _V, _L
    
    W = W[:, 0: nbPoles]
    Wup: np.ndarray = W[1: -1, :]
    Wdown: np.ndarray = W[0: -2, :]
    
    Rk: np.ndarray = np.linalg.pinv(Wdown) @ Wup
    Z: np.ndarray = np.linalg.eig(Rk)[0]
    

    # Calcul du critère ESTER
    
    J = ESTER(W, int(nbPoles/2))
    
    return Z, J

    
def moindreCarres(vecPoles: np.ndarray, signal: np.ndarray) -> np.ndarray:
    
    Ve = np.vander(vecPoles, signal.size).T
    b = np.linalg.pinv(Ve) @ signal
    
    return b


def vdm(z: np.ndarray, N: int) -> np.ndarray:

    n = np.arange(0, N - 1)
    V = np.exp(n @ np.log(z))

    V[np.isnan(V)] = 0
    
    return V


def parametres(signal: np.ndarray, 
               samplerate: float,
               nbPoles: int
               ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: 
    """Fonction qui appelle espritBd() puis formate les matrice f, ksi, b, J

    Args:
        signal (_type_): _description_
        samplerate (_type_): _description_
        nbPoles (_type_): _description_

    Returns:
        tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: _description_
    """    

    
    signalZ, J= ESPRIT(signal, 2*nbPoles)
    
    # régler le pb de dimension de signal_Z dans np.linalg.eig()
    
    f: np.ndarray = np.angle(signalZ) * samplerate/(2*np.pi)
    b: np.ndarray = moindreCarres(signalZ, signal)    
    ksi: np.ndarray = -np.log10(abs(signalZ))*samplerate
    
    f = f[f > 0]
    b = np.abs(b[np.imag(b) > 0])  
    ksi = ksi[ksi > 0]
    
    f = np.resize(f, (nbPoles))
    b = np.resize(b, (nbPoles))
    ksi = np.resize(ksi, (nbPoles)) 

    # tri des vecteurs de parameteres
    indexes = np.argsort(f)
    f = f[indexes]
    b = b[indexes]
    ksi = ksi[indexes]

    return f, b, ksi, J