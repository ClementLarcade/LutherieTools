import matplotlib.pyplot as plt
import numpy as np

import fonctions


def affichage(signal: np.ndarray,
              samplerate: float,
              matFk: np.ndarray,
              matBk: np.ndarray,
              matKsik: np.ndarray,
              matJk: np.ndarray,
              T: np.ndarray,
              signalPreset: str,
              save: bool = False
              ) -> None:
    
    
    if signalPreset == "gen": plotTitle = signalPreset

    else: plotTitle = "HROGramme"

    plt.close('all')
    ylim = (0, 3000)

    # Passer tout ca dans son fichier perso
    ###############################################
    fig, ax = plt.subplots()

    #ax.set_facecolor("#440154")
    plot = ax.scatter(T[:], 
                    matFk[:],
                    s = 5,
                    c = matBk[:],
                    cmap = "Greys"
                    )
    
    ax.set_xlim((0, signal.size/samplerate))
    ax.set_ylim(ylim[0], ylim[1])
    ax.set_title(plotTitle, fontsize = "13")
    ax.set_xlabel("Temps (s)", fontsize = "13")
    ax.set_ylabel("Fréquence (Hz)", fontsize = "13")
    fig.colorbar(plot, ax=ax, label = "Amplitude (dB)")


    if save: fig.savefig(f"{signalPreset}.png", dpi = 1000)

    plt.show()
    
    return