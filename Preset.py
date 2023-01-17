import numpy as np
from scipy.io.wavfile import read
import json
from time import time
from typing import Literal
from Classes import Params

from SignauxTest import signauxTest


def preset(preset: str,
           paramsPath: str,
           signalPreset: Literal["diapason",
                                 "cordeIdeale",
                                 "guitareSimulee", 
                                 "guitareCorps",
                                 "guitareModesDoubles", 
                                 "guitareBruit"]
           ) -> tuple[np.ndarray, Params, str]:
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
        tuple[np.ndarray, Params, str]:
        signal, params, exportfolder
    """    
    signal: np.ndarray = np.array([])
    
    params = Params()

    if preset == "gen":
        
        params.samplerate = 48000
        duree = 2
        signal = signauxTest(duree, params.samplerate, signalPreset)
            
        params.horizon = 0.03
        params.overlap = 0.
        params.nbPoles = 50

    elif preset == "sample":
        
        [params.samplerate, signal] = read(f"Clips audio/{signalPreset}.wav")
        
        if signal.ndim > 1:
            # on isole le premier canal
            signal = signal[:, 0]
            
        signal = np.array(signal, dtype = "float")
            
        duree = signal.size/params.samplerate
        print(f'duree du signal = {duree}')
        
        params.horizon = 0.05
        params.overlap = 0.
        params.nbPoles = 100
        
    elif preset == 'json': 
        
        argsDict = json.load(open(paramsPath))
        
        [params.samplerate, signal] = read(argsDict["filepath"])
        
        if signal.shape[0] > 1:
            signal = signal[:,0]
        
        params.horizon = argsDict["horizon"]
        params.overlap = argsDict["overlap"]
        params.nbPoles = argsDict["nbPoles"]
        params.exportfolder = argsDict["exportfolder"]

        # Preparation 
        
        #exportFolder = argsDict["exportFolder"]
        
    exportfolder: str = "export_" + str(params.exportfolder)
    
    signal = signal/np.max(signal)
        
    return signal, params, exportfolder