import numpy as np
from scipy.linalg import hankel, svd
from scipy.signal import decimate
import json
from codecs import open
from functools import wraps
import matplotlib.pyplot as plt

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
               ) -> tuple[np.ndarray, float]:
    
    facteur = int(samplerate/newSamplerate)
    signal = decimate(signal, facteur, ftype = 'fir') # fonction scipy
    
    
    return signal, newSamplerate


def seuil(inputArray: np.ndarray,
          seuil: float
          ) -> np.ndarray:
    
    array = np.zeros_like(inputArray)    
    
    for (i,j), x in np.ndenumerate(inputArray):
        if x < seuil:
            array[i,j] = np.NaN
        else:
            array[i,j] = x
            
    return array


def esterBd(signal: np.ndarray,
            nbPolesMax: int
            ) -> np.ndarray:
    
    # calcul du parametre ESTER : plus utilisé car intégré dans espritBd pour
    # pas recalculer la svd longue et gagner en temps de calcul
    
    signal = signal[:]
    N = signal.size
    H = int(N/3)
    
    X = hankel(signal[0 : H], signal[H : -1])
    H = X @ np.transpose(X)     # @ c'est le produit matriciel
    
    U, _V, _L = np.linalg.svd(H)    
    # essayer avec la SVD de scipy (sans doute plus rapide)
    del _V, _L
    
    J = np.zeros(nbPolesMax)
    
    for nbPoles in range(1, nbPolesMax + 1):
        
        Us = U[:, 0: nbPoles]
        Uup = Us[1: -1, :]
        Udown = Us[0: -2, :]
        phi = np.linalg.pinv(Udown) @ Uup
        E = Uup - Udown @ phi
        J[nbPoles - 1] = 1/np.linalg.norm(E, 2)
        
        
    return J


def stabilité(signal: np.ndarray, 
              matBk:np.ndarray,
              nbPoles: int
              ):
    
    return
    

@memoize #utiliser pour accélerer l'algorithme ESPRIT en réutilisant les valeurs déja calculées
def ESPRIT(signal: np.ndarray,
           nbPoles: int
           ) -> tuple[np.ndarray, np.ndarray]:
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
    
    N = signal.shape[0]

    M = int(N/3)
    L = N - M + 1 # M vaut N /3 et l vaut horizon - M + 1

    H = hankel(signal[0 : M], signal[L : -1])
    C =  1/L * H @ H.T
  
    W, _V, _L = np.linalg.svd(C, full_matrices=False)
    del _V, _L
    
    W = W[:, 0: nbPoles]
    Wup = W[1: -1, :]
    Wdown = W[0: -2, :]
    
    RK = np.linalg.pinv(Wdown) @ Wup

    Z = np.linalg.eig(RK)[0]
    
    
    # Calcul du critère ESTER
    
    nbPolesMax = int(nbPoles/2)
    
    J = np.zeros(nbPolesMax)
    
    for pole in range(1, nbPolesMax + 1):
        
        Ws = W[:, 0: pole]
        Wup = Ws[1: -1, :]
        Wdown = Ws[0: -2, :]
        RK = np.linalg.pinv(Wdown) @ Wup
        E = Wup - Wdown @ RK
        J[pole - 1] = 1/np.linalg.norm(E, 2)
    
    return Z, J

    
def moindreCarres(vecPoles: np.ndarray,
                  signal: np.ndarray
                  ) -> np.ndarray:
    
    Ve = np.transpose(np.vander(vecPoles, signal.size))
    b = np.linalg.pinv(Ve) @ signal
    
    return b


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
   
    Hamm = np.hamming(signal.size)
    signal *= Hamm
    
    signal_z, J= ESPRIT(signal, 2*nbPoles)
    
    # régler le pb de dimension de signal_Z dans np.linalg.eig()
    
    f = np.angle(signal_z) * samplerate/(2*np.pi)
    ksi = -np.log(abs(signal_z))*samplerate
    b = moindreCarres(signal_z, signal)    
    
    f = f[f > 0]
    ksi = ksi[ksi > 0]
    b = np.abs(b[np.imag(b) > 0])  
    
    f = np.resize(f, (nbPoles))
    ksi = np.resize(ksi, (nbPoles)) 
    #pb de dimension des ksik
    b = np.resize(b, (nbPoles))
    
    
    return f, ksi, b, J