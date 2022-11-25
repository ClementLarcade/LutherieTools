import numpy as np
from numpy.matlib import repmat
import matplotlib.pyplot as plt
from sys import argv
from os import mkdir

from time import perf_counter

from HROgramme import HROgramme
import Fonctions
from Preset import Preset

timeDebut = perf_counter()

# Seuiller matKsik et matJk
# tester les signaux tests
# trouver des plages de variations pour les params d'étude



preset = "gen"     # "gen","sample" ou "json" ou "jsonConsole"
paramsPath = ''

# forme d'appel : python mainHROgramme.py args.json jsonConsole

if len(argv) > 1:
    paramsPath = argv[1]
    preset = argv[2]
    
signal, samplerate, horizon, overlap, nbPoles, exportFolder = Preset(preset, paramsPath)
signal = np.array(signal)

# Process

signalLength = signal.size/samplerate

print(f"samplerate = {samplerate}")
print(f"horizon = {horizon}")
print(f"overlap = {overlap}")
print(f"nbPoles = {nbPoles}")

matFk, matKsik, matBk, matJk = HROgramme(signal,
                                         samplerate,
                                         horizon,
                                         overlap,
                                         nbPoles)

T = repmat(np.linspace(0, signalLength, matFk.shape[1]), nbPoles, 1)



#%% Export en json des matrices 

if preset == "json" or preset == 'jsonConsole':
    
    mkdir("exports/" + exportFolder)
    Fonctions.exportJson(matFk, "exports/" + exportFolder + "/Fk.json")
    Fonctions.exportJson(matBk, "exports/" + exportFolder + "/Bk.json")
    Fonctions.exportJson(matBk, "exports/" + exportFolder + "/Ksik.json")
    Fonctions.exportJson(matJk, "exports/" + exportFolder + "/Jk.json")
    Fonctions.exportJson(T,     "exports/" + exportFolder + "/T.json")


# Calcul des perfs

timeFin = perf_counter()
timeTotal = timeFin - timeDebut
print(f"temps d'execution = {timeTotal}")


#%% affichage


# seuillage des Bk
matBkSeuil = Fonctions.seuil(matBk, 10E-0)
matBkSeuil = matBkSeuil/np.nanmax(matBkSeuil)

plt.close('all')
ylim = (0,3000)


fig, ax1 = plt.subplots(1,2, figsize = (12,6))

ax = ax1[0]
ax.scatter(T[:], matFk[:], s = 15, c = matBkSeuil[:], cmap='Greys')
ax.set_xlim((0, signal.size/samplerate))
ax.set_ylim(ylim[0], ylim[1])
ax.set_title("les Bk")

ax = ax1[1]
ax.specgram(list(signal), 8192, samplerate)
ax.set_xlim((0, signal.size/samplerate))
ax.set_ylim(ylim[0], ylim[1])
             
t = np.linspace(0, signal.size/samplerate, signal.size)


fig2, ax2 = plt.subplots()

ax2.plot(t, signal)
ax2.set_xlim((0, signal.size/samplerate))
ax2.set_title("Signal")
plt.tight_layout()


"""
fig3, ax3 = plt.subplots()

ax3.scatter(T[:], matFk[:], s = 15, c = 1 - matKsik[:])
ax3.set_xlim((0, signal.size/samplerate))
ax3.set_ylim(ylim[0], ylim[1])


fig4, ax4 = plt.subplots()

ax4.scatter(T[:], matFk[:], s = 15, c = 1 - matJk[:])
ax4.set_xlim((0, signal.size/samplerate))
ax4.set_ylim(ylim[0], ylim[1])
"""

plt.show()


