import numpy as np
from scipy.linalg import hankel
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


def exportJson(mat: np.ndarray, file_path: str) -> None:
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


def seuil(inputArray: np.ndarray, seuil: float) -> np.ndarray:
    
    array = np.zeros_like(inputArray)    
    
    for (i,j), x in np.ndenumerate(inputArray):
        if x < seuil:
            array[i,j] = np.NaN
        else:
            array[i,j] = x
            
    return array


def esterBd(signal, nbPolesMax):
    
    # calcul du parametre ESTER : plus utilisé car intégré dans espritBd pour
    # pas recalculer la svd longue et gagner en temps de calcul
    
    signal = signal[:]
    N = signal.size
    H = int(N/3)
    
    X = hankel(signal[0 : H], signal[H : -1])
    H = X @ np.transpose(X)     # @ c'est le produit matriciel
    
    U, _V, _L = np.linalg.svd(H)    
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


@memoize #utiliser pour accélerer l'algorithme ESPRIT en réutilisant les valeurs déja calculées
def espritBd(signal: np.ndarray,
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
        
    signal = signal[:]
    N = signal.shape[0]

    H = int(N/3)

    X = hankel(signal[0 : H], signal[H : -1])
    H = X @ np.transpose(X) 
  

    U, _V, _L = np.linalg.svd(H, full_matrices=False)
    del _V, _L
    
    U = U[:, 0:nbPoles]
    Uup = U[1:-1, :]
    Udown = U[0:-2, :]
    
    phi = np.linalg.pinv(Udown) @ Uup

    Z = np.linalg.eig(phi)[0]
    
    
    # Calcul du critère ESTER
    
    nbPolesMax = nbPoles//2
    
    J = np.zeros(nbPolesMax)
    
    for pole in range(1, nbPolesMax + 1):
        
        Us = U[:, 0: pole]
        Uup = Us[1: -1, :]
        Udown = Us[0: -2, :]
        phi = np.linalg.pinv(Udown) @ Uup
        E = Uup - Udown @ phi
        J[pole - 1] = 1/np.linalg.norm(E, 2)
    
    return Z, J

    
def moindreCarres(Z: np.ndarray, S: np.ndarray) -> np.ndarray:
    
    V = np.transpose(np.vander(Z, S.size))
    B = np.linalg.pinv(V) @ S
    
    return B


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
    signal_z, J= espritBd(signal, 2*nbPoles)
    
    # régler le pb de dimension de signal_Z dans np.linalg.eig()
    
    f = np.angle(signal_z)*samplerate/(2*np.pi)
    ksi = -np.log10(abs(signal_z))*samplerate
    b = moindreCarres(signal_z, signal)    
    
    f = f[f > 0]
    ksi = ksi[ksi > 0]
    b = np.abs(b[np.imag(b) > 0])
    
    f = np.resize(f, (nbPoles))
    ksi = np.resize(ksi, (nbPoles))
    b = np.resize(b, (nbPoles))
    
    
    return f, ksi, b, J