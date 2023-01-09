import numpy as np
import fonctions
import matplotlib.pyplot as plt
from copy import deepcopy


def HROgramme(signal: np.ndarray,
              samplerate: int,
              horizon: float,
              overlap: float,
              nbPoles: int
              ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:

    
    signalLength: int = signal.size
    
    echParHorizon: int = int(horizon * samplerate)
    echParRecouvrement: int = int(echParHorizon * overlap)
    curseur: int = 0
    
    nbFenetres: int = int(signalLength/(echParHorizon*(1 - overlap)))
    
    
    matFk: np.ndarray =     np.zeros((nbPoles, nbFenetres))
    matKsik: np.ndarray =   np.zeros((nbPoles, nbFenetres))
    matBk: np.ndarray =     np.zeros((nbPoles, nbFenetres))
    matJk: np.ndarray =     np.zeros((nbPoles, nbFenetres))    
    
    print(f"taille de fenetre (samples) = {echParHorizon}")
    print(f'nbFenetres = {nbFenetres}')
    
    for k in range(nbFenetres):
        
        if k %  10 == 0:    
            print(f'{k}/{nbFenetres}')
            
        
        curseur = int(k*(echParHorizon - echParRecouvrement) + 1)
        
        if curseur + echParHorizon >= signalLength:
            break
        
        fenetre: np.ndarray = deepcopy(signal[curseur : curseur + echParHorizon])
        
        matFk[:, k], matKsik[:, k], matBk[:, k], matJk[:, k] = fonctions.parametres(fenetre, samplerate, nbPoles)
        
        #matJk[:, k] = Fonctions.esterBd(fenetre, nbPoles)
        
        
    for (i,j), x in np.ndenumerate(matFk):
        # Supprimer les frequences calculées au delà de F nyquist
        if x > 0.5*samplerate:
            
            matFk[i,j] = np.NaN
            matBk[i,j] = np.NaN
            matJk[i,j] = np.NaN
        
        
    return matFk, matBk, matKsik, matJk