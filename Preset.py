from SignauxTest import signauxTest
from scipy.io.wavfile import read
import Fonctions
import json
from time import time
import numpy as np



def Preset(preset: str,
           paramsPath: str
           ) -> tuple[np.ndarray, float, float, float, int, str ]:
    """
    Fonction déterminant quel signal et paramètres on utilisera : 
    - "gen" : signal généré
    - "sample" : un fichier déterminé par son chemin
    - "json" : le chemin du fichier et les paramètres sont stockés dans un fichier .json
    - "jsonConsole" : comme "json" mais utilisé pour appeler le programme depuis le terminal du serveur 

    Args:
        preset (str): "gen", "sample", "json", "jsonConsole"
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
        
        samplerate = 22050
        duree = 1
        t, signal = signauxTest(duree, samplerate, "sinusAleatoires")
            
        horizon = 0.005
        overlap = 0.75
        nbPoles = 100

        
    elif preset == "sample":
        
        [samplerate, signal] = read("Clips audio/Violon.wav")
        
        if signal.ndim > 1:
            # on isole le premier canal
            signal = signal[:, 0]
            
        duree = signal.size/samplerate
        print(f'duree du signal = {duree}')
        
        # Preparation du signal diminution de la samplerate
        
        newSamplerate = samplerate / 2
        
        # on remarque que pour une samplerate < 15000 Hz l'algo affiche n'importe quoi
        
        signal, samplerate = Fonctions.decimation(signal, samplerate, newSamplerate)
        
        
        horizon = 0.01
        overlap = 0.25
        nbPoles = 50
        

    elif preset == "json": 
        """
        on a reussi à mettre les paramètres et le chemin du son dans un fichier JSON
        pour simuler l'envoie depuis l'appli vers le serveur
        
        """
        
        arguments = open("arguments.json")
        argsDict = json.load(arguments)
        
        [samplerate, signal] = read(argsDict["filepath"])
        
        if signal.shape[0] > 1:
            signal = signal[:,0]
        
        
        horizon = argsDict["horizon"]
        overlap = argsDict["overlap"]
        nbPoles = argsDict["nbPoles"]

        
        # Preparation 
        
        newSamplerate = samplerate / 2
            
        signal, samplerate = Fonctions.decimation(signal, samplerate, newSamplerate)
        
        
    elif preset == 'jsonConsole':
        
        jsonPath = paramsPath    
        
        arguments = open(jsonPath)
        argsDict = json.load(arguments)
        
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

    
    exportFolder = "export_"+str(int(time()))
        
    return signal, samplerate, horizon, overlap, nbPoles, exportFolder

