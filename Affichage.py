import matplotlib.pyplot as plt
import numpy as np


def affichage(
    frequences: np.ndarray,
    color: np.ndarray, 
    temps: np.ndarray, 
    signalPreset: str, 
    datatoplot: str,
    critere: str,
    save: bool
    ) -> None:
    

    plt.close("all")
    
    ylimit = (0, 3500)
    
    fig, ax = plt.subplots()

    graph = ax.scatter(temps, frequences, s=15, c=color, cmap = "jet")
    ax.set_ylim(ylimit)
    ax.set_xlim(0, temps[0, -1])
    ax.set_title(f"{datatoplot} - {signalPreset} - {critere}")
    ax.set_xlabel("Temps (s)")
    ax.set_ylabel("Fréquence (Hz)")

    plt.colorbar(graph)
    ax.grid(True)
    
    #ax.plot([temps[0,0], temps[0, -1]], [440, 440])

    return