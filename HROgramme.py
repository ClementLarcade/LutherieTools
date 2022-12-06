import numpy as np
import Fonctions
import matplotlib.pyplot as plt
from copy import deepcopy


def HROgramme(signal: np.ndarray,
              samplerate: float,
              horizon: float,
              overlap: float,
              nbPoles: int
              ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:

    
    signalLength = signal.size
    
    echParHorizon = int(horizon * samplerate)
    echParRecouvrement = int(echParHorizon * overlap)
    curseur = 0
    
    nbFenetres = int(signalLength/(echParHorizon*(1 - overlap)))
    
    
    matFk =     np.zeros((nbPoles, nbFenetres))
    matKsik =   np.zeros((nbPoles, nbFenetres))
    matBk =     np.zeros((nbPoles, nbFenetres))
    matJk =     np.zeros((nbPoles, nbFenetres))    
    
    print(f"taille de fenetre (samples) = {echParHorizon}")
    print(f'nbFenetres = {nbFenetres}')
    
    for k in range(nbFenetres):
        
        if k %  10 == 0:    
            print(f'{k}/{nbFenetres}')
            
        
        curseur = int(k*(echParHorizon - echParRecouvrement) + 1)
        
        if curseur + echParHorizon >= signalLength:
            break
        
        fenetre = deepcopy(signal[curseur : curseur + echParHorizon])
        
        matFk[:, k], matKsik[:, k], matBk[:, k], matJk[:, k] = Fonctions.parametres(fenetre, samplerate, nbPoles)
        
        #matJk[:, k] = Fonctions.esterBd(fenetre, nbPoles)
        
        
    for (i,j), x in np.ndenumerate(matFk):
        # Supprimer les frequences calculées au delà de F nyquist
        if x > 0.5*samplerate:
            
            matFk[i,j] = np.NaN
            matBk[i,j] = np.NaN
            matJk[i,j] = np.NaN
        
        
    return matFk, matKsik, matBk, matJk