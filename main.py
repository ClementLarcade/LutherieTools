import numpy as np
from numpy.matlib import repmat
import matplotlib.pyplot as plt
from sys import argv
from time import perf_counter

from HROgramme import HROgramme
import Fonctions
from Preset import preset
from Affichage import affichage
from Stability import stability


timeDebut = perf_counter()


# Seuiller matKsik et matJk
# tester les signaux tests
# trouver des plages de variations pour les params d'étude


argvPreset: str = "sample"     
# "gen","sample" ou "json" 
signalPreset: str = "guitareSimulee"
# Envelope, battements, sinusAleatoires, diapason, cordeIdeale
# guitareSimulee, guitareCorps, guitareModesDoubles, guitareBruit

paramsPath: str = ''
afficher: bool = True

signal: np.ndarray = np.array([])
exportfolder: str = ""

# forme d'appel : python mainHROgramme.py args.json 

if len(argv) > 1:
    paramsPath = argv[1]
    argvPreset: str = "json"
    
(signal, params, exportfolder) = preset(argvPreset, paramsPath, signalPreset)

# Process

signalLength: float = signal.size/params.samplerate

print(f"samplerate = {params.samplerate}")
print(f"horizon = {params.horizon}")
print(f"overlap = {params.overlap}")
print(f"nbPoles = {params.nbPoles}")

#%% Calcul du HROgramme

matrices = HROgramme(signal, params)

matrices.T = repmat(np.linspace(0, signalLength, matrices.F.shape[1]), params.nbPoles, 1)


# Calcul des perfs

timeFin: float = perf_counter()
timeTotal: float = timeFin - timeDebut
print(f"temps d'execution = {timeTotal}")


#%% conditionnement

# algo de stabilité
tolerancestabilite = 1
numcolstoverify = 2
matrices.FStable = stability(matrices.F, numcolstoverify, tolerancestabilite)


# seuillage de la matrice des B
matrices.BdB = 20*np.log10(matrices.B)
Fonctions.seuil(matrices, -60)

#%% Export en json des matrices 

if True:
    Fonctions.export(matrices, exportfolder)

#%% affichage

if afficher:
    plt.close("all")
    
    affichage(
        matrices.F,
        matrices.BdBSeuil,
        matrices.T, 
        signalPreset,
        "Amplitude (dB)", 
        "sans critere",
        False)
    
    affichage(
        matrices.FStable,
        matrices.BdBSeuil,
        matrices.T, 
        signalPreset,
        "Amplitude (dB)", 
        "Stabilité",
        False)
    
    plt.show()
 
