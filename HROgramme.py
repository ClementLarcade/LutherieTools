import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

from estimation_parametres import parametres
from Classes import Params, Matrices 


def HROgramme(signal: np.ndarray, params: Params) -> Matrices:

    signalLength: int = signal.size
    
    echParHorizon: int = int(params.horizon * params.samplerate)
    echParRecouvrement: int = int(echParHorizon * params.overlap)
    curseur: int = 0
    
    nbFenetres: int = int(signalLength/(echParHorizon*(1 - params.overlap)))
    
    matrices = Matrices()
    matrices.F: np.ndarray =     np.zeros((params.nbPoles, nbFenetres))
    matrices.Ksi: np.ndarray =   np.zeros((params.nbPoles, nbFenetres))
    matrices.B: np.ndarray =     np.zeros((params.nbPoles, nbFenetres))
    matrices.J: np.ndarray =     np.zeros((params.nbPoles, nbFenetres))    
    
    print(f"taille de fenetre (samples) = {echParHorizon}")
    print(f'nbFenetres = {nbFenetres}')
    
    for k in range(nbFenetres):
        
        if k %  10 == 0:    
            print(f'{k}/{nbFenetres}')
            
        curseur = int(k*(echParHorizon - echParRecouvrement) + 1)
        
        if (curseur + echParHorizon) > signalLength:
            print("sortie de boucle")
            break
        
        fenetre: np.ndarray = deepcopy(signal[curseur : curseur + echParHorizon])
        
        parametresEstimes = parametres(fenetre, params.samplerate, params.nbPoles)
        matrices.F[:, k] = parametresEstimes[0]
        matrices.B[:, k] = parametresEstimes[1] 
        matrices.Ksi[:, k] = parametresEstimes[2]
        matrices.J[:, k] = parametresEstimes[3]
        
        
    antialiasingfilter(matrices, params)
        
    return matrices


def antialiasingfilter(matrices, params):

    for (i,j), x in np.ndenumerate(matrices.F):
        # Supprimer les frequences calculées au delà de F nyquist
        if x > 0.5*params.samplerate:
            
            matrices.F[i,j] = np.NaN
            matrices.B[i,j] = np.NaN
            matrices.J[i,j] = np.NaN

    return matrices