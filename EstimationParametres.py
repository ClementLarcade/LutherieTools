import numpy as np
from scipy.linalg import hankel, svd, pinv, eig

import matplotlib.pyplot as plt


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

    H: np.ndarray = hankel(signal[0 : M], signal[M : -1])
    C: np.ndarray =  1/L * H @ H.T
  
    W, _V, _L = svd(C, full_matrices=False, overwrite_a=True)
    del _V, _L
    
    W = W[:, 0: nbPoles]
    Wup: np.ndarray = W[1: -1, :]
    Wdown: np.ndarray = W[0: -2, :]
    
    Rk: np.ndarray = pinv(Wdown, check_finite=False) @ Wup
    Z: np.ndarray = eig(Rk, right=False)
    
    # Calcul du critère ESTER
    
    #DBGIMSHOW(C, W, np.abs(Z))
    
    J = ESTER(W, int(nbPoles/2))
    
    return Z, J


def parametres(signal: np.ndarray, 
               samplerate: float,
               nbPoles: int
               ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: 
    """Fonction qui appelle ESPRIT() puis formate les matrice f, ksi, b, J

    Args:
        signal (_type_): _description_
        samplerate (_type_): _description_
        nbPoles (_type_): _description_

    Returns:
        tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: _description_
    """    

    poles, J = ESPRIT(signal, 2*nbPoles)
    
    # régler le pb de dimension de signal_Z dans np.linalg.eig()
    
    f: np.ndarray = np.angle(poles) * samplerate/(2*np.pi)
    b: np.ndarray = leastsquares(poles, signal)    
    ksi: np.ndarray = -np.log(abs(poles))*samplerate
    
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
    
    #DBGPLOT(signal,f, b)

    return f, b, ksi, J


def leastsquares(vecPoles: np.ndarray, signal: np.ndarray) -> np.ndarray:
    
    Ve = vandermonde(vecPoles, signal.size)
    b = pinv(Ve, check_finite=False) @ signal
    
    return b


def vandermonde(z: np.ndarray, N: int) -> np.ndarray:

    n = np.arange(0, N)
    V = np.exp( np.outer(n, np.log(z)) )

    V[np.isnan(V)] = 0
    
    return V


def DBGPLOT(signal, f, b):
    fig, (ax1, ax2) = plt.subplots(2, 1)
    
    ax1.plot(f, 20*np.log10(b))
    ax2.plot(signal)
    return 
    
    
def DBGIMSHOW(mat1, mat2, poles):
    
    plt.figure(1)
    
    plt.subplot(3,1,1)
    plt.imshow(mat1)
    
    plt.subplot(3,1,2)
    plt.imshow(mat2)
    
    plt.subplot(3,1,3)
    plt.plot(poles)
