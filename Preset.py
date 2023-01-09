from signauxtest import signauxTest
from scipy.io.wavfile import read
import fonctions
import json
from time import time
import numpy as np

from typing import Literal




def Preset(preset: str,
           paramsPath: str,
           signalPreset: Literal["diapason",
                                 "cordeIdeale",
                                 "guitareSimulee", 
                                 "guitareCorps",
                                 "guitareModesDoubles", 
                                 "guitareBruit"]
           ) -> tuple[np.ndarray, int, float, float, int, str ]:
    """
    Fonction déterminant quel signal et paramètres on utilisera : 
    - "gen" : signal généré
    - "sample" : un fichier déterminé par son chemin
    - "json" : comme "json" mais utilisé pour appeler le programme depuis le terminal du serveur 

    Args:
        preset (str): "gen", "sample", "json"
        signalPreset (str): preset pour le signal à générer
        paramsPath (str): le chemin vers le fichier .json contenant les paramètres 

    Returns:
        tuple[np.ndarray, float, float, float, int, str ]:
        signal, samplerate, horizon, overlap, nbPoles, exportFolder
    """    
    signal: np.ndarray = np.array([])
    samplerate: int = 0
    horizon: float = 0.
    overlap: float = 0.
    nbPoles: int = 0


    if preset == "gen":
        
        samplerate = 48000
        duree = 2
        signal = signauxTest(duree, samplerate, signalPreset)
            
        horizon = 0.05
        overlap = 0.
        nbPoles = 50

        
    elif preset == "sample":
        
        [samplerate, signal] = read("Clips audio/Clip_basse2.wav")
        
        if signal.ndim > 1:
            # on isole le premier canal
            signal = signal[:, 0]
            
        signal = np.array(signal, dtype = "float")
            
        duree = signal.size/samplerate
        print(f'duree du signal = {duree}')
        
        # Preparation du signal diminution de la samplerate
        
        newSamplerate: int = int(samplerate / 2)
        
        # on remarque que pour une samplerate < 15000 Hz l'algo affiche n'importe quoi
        
        #signal, samplerate = Fonctions.decimation(signal, samplerate, newSamplerate)
        
        
        horizon = 0.05
        overlap = 0.
        nbPoles = 50
        
        
    elif preset == 'json': 
        
        argsDict = json.load(open(paramsPath))
        
        [samplerate, signal] = read(argsDict["filepath"])
        
        if signal.shape[0] > 1:
            signal = signal[:,0]
        
        
        horizon = argsDict["horizon"]
        overlap = argsDict["overlap"]
        nbPoles = argsDict["nbPoles"]

        # Preparation 
        
        #exportFolder = argsDict["exportFolder"]
        
        newSamplerate: int = int(samplerate / 2)
            
        signal, samplerate = fonctions.decimation(signal, samplerate, newSamplerate)

    
    exportFolder: str = "export_" + str(int(time()))
    
    signal = signal/np.max(signal)
        
    return signal, samplerate, horizon, overlap, nbPoles, exportFolder

