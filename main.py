import numpy as np
from numpy.matlib import repmat
import matplotlib.pyplot as plt
from sys import argv
from os import mkdir

from time import perf_counter

from HROgramme import HROgramme
import Fonctions
from Preset import Preset
from Affichage import affichage

timeDebut = perf_counter()


# Seuiller matKsik et matJk
# tester les signaux tests
# trouver des plages de variations pour les params d'étude


preset = "gen"     
# "gen","sample" ou "json" 
signalPreset = "diapason"
# Envelope, battements, sinusAleatoires, diapason, cordeIdeale
# guitareSimulee, guitareCorps, guitareModesDoubles, guitareBruit

paramsPath = ''
affichager = False

# forme d'appel : python mainHROgramme.py args.json 

if len(argv) > 1:
    paramsPath = argv[1]
    preset = "json"
    
(signal, samplerate, horizon, 
 overlap, nbPoles, exportFolder) = Preset(preset, 
                                          paramsPath,
                                          signalPreset=signalPreset
                                          )
signal = np.array(signal)

# Process

signalLength = signal.size/samplerate

print(f"samplerate = {samplerate}")
print(f"horizon = {horizon}")
print(f"overlap = {overlap}")
print(f"nbPoles = {nbPoles}")

matFk, matBk, matKsik, matJk = HROgramme(signal,
                                         samplerate,
                                         horizon,
                                         overlap,
                                         nbPoles
                                         )

T = repmat(np.linspace(0, signalLength, matFk.shape[1]), nbPoles, 1)


# Calcul des perfs

timeFin = perf_counter()
timeTotal = timeFin - timeDebut
print(f"temps d'execution = {timeTotal}")


#%% Export en json des matrices 

if preset == "json" or preset == 'jsonConsole':
    
    mkdir("exports/" + exportFolder)
    Fonctions.exportJson(matFk, "exports/" + exportFolder + "/Fk.json")
    Fonctions.exportJson(matBk, "exports/" + exportFolder + "/Bk.json")
    Fonctions.exportJson(matBk, "exports/" + exportFolder + "/Ksik.json")
    Fonctions.exportJson(matJk, "exports/" + exportFolder + "/Jk.json")
    Fonctions.exportJson(T,     "exports/" + exportFolder + "/T.json")



#%% affichage


# seuillage des Bk

#matBk = matBk/np.nanmax(matBk)




matBkdB = 20*np.log10(matBk)
matBkSeuil = Fonctions.seuil(matBkdB, -60)

if affichager:
    affichage(signal, samplerate, matFk, matBkSeuil, matKsik, matJk, T, signalPreset=preset)





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




