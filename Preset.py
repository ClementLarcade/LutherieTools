from SignauxTest import signauxTest
from scipy.io.wavfile import read
import Fonctions
import json
from time import time
import numpy as np



def Preset(preset: str,
           paramsPath: str,
           signalPreset = "diapason"
           ) -> tuple[np.ndarray, float, float, float, int, str ]:
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
    signal = np.array([])
    samplerate = 0
    horizon = 0.
    overlap = 0.
    nbPoles = 0


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
        
        newSamplerate = samplerate / 2
        
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
        
        newSamplerate = samplerate / 2
            
        signal, samplerate = Fonctions.decimation(signal, samplerate, newSamplerate)

    
    exportFolder = "export_" + str(int(time()))
    
    signal = signal/np.max(signal)
        
    return signal, samplerate, horizon, overlap, nbPoles, exportFolder

