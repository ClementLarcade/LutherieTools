import numpy as np
from numpy.matlib import repmat
import matplotlib.pyplot as plt
from sys import argv
from os import mkdir
from time import perf_counter
from typing import TypeAlias, Any
Matrice: TypeAlias = np.ndarray[Any, np.dtype[np.float64]]

from hrogramme import HROgramme
import fonctions
import preset
import affichage
from stability import stability
from Classes import Params, Matrices


timeDebut = perf_counter()


# Seuiller matKsik et matJk
# tester les signaux tests
# trouver des plages de variations pour les params d'étude


argvPreset: str = "gen"     
# "gen","sample" ou "json" 
signalPreset: str = "guitareBruit"
# Envelope, battements, sinusAleatoires, diapason, cordeIdeale
# guitareSimulee, guitareCorps, guitareModesDoubles, guitareBruit

paramsPath: str = ''
afficher: bool = True

signal: np.ndarray = np.array([])
exportFolder: str = ""

# forme d'appel : python mainHROgramme.py args.json 

if len(argv) > 1:
    paramsPath = argv[1]
    argvPreset: str = "json"
    
(signal, params, exportFolder) = preset.preset(argvPreset, paramsPath, signalPreset)

# Process

signalLength: float = signal.size/params.samplerate

print(f"samplerate = {params.samplerate}")
print(f"horizon = {params.horizon}")
print(f"overlap = {params.overlap}")
print(f"nbPoles = {params.nbPoles}")

matrices = HROgramme(signal, params)

matrices.T = repmat(np.linspace(0, signalLength, matrices.F.shape[1]), params.nbPoles, 1)


# Calcul des perfs

timeFin: float = perf_counter()
timeTotal: float = timeFin - timeDebut
print(f"temps d'execution = {timeTotal}")


#%% Export en json des matrices 

if argvPreset == "json":
    
    mkdir("exports/" + exportFolder)
    fonctions.exportJson(matrices.F, "exports/" + exportFolder + "/F.json")
    fonctions.exportJson(matrices.B, "exports/" + exportFolder + "/B.json")
    fonctions.exportJson(matrices.B, "exports/" + exportFolder + "/Ksi.json")
    fonctions.exportJson(matrices.J, "exports/" + exportFolder + "/J.json")
    fonctions.exportJson(matrices.T,     "exports/" + exportFolder + "/T.json")



#%% affichage

# seuillage des Bk
tolerancestabilite = 1
numcolstoverify = 2
matrices.FStable = stability(matrices.F, numcolstoverify, tolerancestabilite)

matrices.BdB = 20*np.log10(matrices.B)
matrices.BdBSeuil = fonctions.seuil(matrices.BdB, -60)

if afficher:
    affichage.affichage(signal, 
                        params.samplerate, 
                        matrices.F, 
                        matrices.B, 
                        matrices.Ksi, 
                        matrices.J, 
                        matrices.T, 
                        signalPreset=argvPreset
                        )






"""
ax = ax1[1]
spectrogramme = ax.specgram(list(signal), 8192, samplerate)
ax.set_xlim((0, signal.size/samplerate))
ax.set_ylim(ylim[0], ylim[1])
plt.colorbar(spectrogramme[3])
################################################
            



################################################
fig2, ax2 = plt.subplots()

t = np.linspace(0, signal.size/samplerate, signal.size)
ax2.plot(t, signal)
ax2.set_xlim((0, signal.size/samplerate))
ax2.set_title("Signal")
plt.tight_layout()
###############################################


fig3, ax3 = plt.subplots()

ax3.scatter(T[:], matFk[:], s = 15, c = 1 - matKsik[:])
ax3.set_xlim((0, signal.size/samplerate))
ax3.set_ylim(ylim[0], ylim[1])


fig4, ax4 = plt.subplots()

ax4.scatter(T[:], matFk[:], s = 15, c = 1 - matJk[:])
ax4.set_xlim((0, signal.size/samplerate))
ax4.set_ylim(ylim[0], ylim[1])
"""




