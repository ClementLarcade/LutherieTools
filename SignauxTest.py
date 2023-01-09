import numpy as np
from typing import Literal


# signaux tests

# 1 diapason                            
# 2 corde idéale (somme de sinusoide)     
# 3 guitare simulée (somme de sinusoide amorties)
# 4 guitare simulée + modes de corps 
# 5 guitatre simulée + modes de corps + modes doubles 
# (modes séparés par un epsilon de frequence pour faire des battements)
# 6 (5) + bruit
# 
# si l'algo réussit tout ca on admet qu'il fonctionne


def signauxTest(duree: float,
                samplerate: int,
                signalPreset: Literal["diapason",
                                      "cordeIdeale",
                                      "guitareSimulee", 
                                      "guitareCorps",
                                      "guitareModesDoubles", 
                                      "guitareBruit"]
                ) -> np.ndarray:
    """_summary_
    Cette fonction génère les différents signaux de test pour tester le fonctionnement
    de l'algorithme. 
    

    Args:
        duree (float): duree du signal 
        samplerate (int): fréquence d'échantillonnage 
        signalPreset (str): "Envelope", "battements", "sinusAleatoires", "diapason", "cordeIdeale", "guitareSimulee", "guitareCorps", "guitareModesDobules", "guitareBruit"

    Returns:
        t, singal : vecteur temps, signal test
    """    
    
    t: np.ndarray = np.arange(0, duree, 1/samplerate)
    preDelay: int = 50 # ms
    
    attackTime: int = 50 # ms
    decayTime: int = 300
    
    prePad: np.ndarray = np.zeros(int(preDelay*samplerate*0.001))
    attackEnvelope: np.ndarray = np.flip(1 - np.linspace(0, 1, int(attackTime*samplerate*0.001))**2) 
    decayEnvelope: np.ndarray = np.flip(np.linspace(0, 1, int(decayTime*samplerate*0.001) )**2)

    ampEnvelope: np.ndarray = np.concatenate((prePad, attackEnvelope, decayEnvelope))
    ampEnvelope = np.pad(ampEnvelope, (0, t.size - ampEnvelope.size))

    if signalPreset == "Envelope":
        return ampEnvelope
    
    if signalPreset == "battements":
        signal = np.sin(2*np.pi*440*t) + 0.5 * np.sin(2*np.pi*450*t)
        return signal

    if signalPreset == "sinusAleatoires":
        taille = 10
        
        amplitudes = 0.5 * np.random.random(taille) + 0.5
        frequences = 1000 * np.random.random(taille) + 100
        print(f"amplitudes = {amplitudes}")
        print(f"frequences = {frequences}")
        signal = np.zeros_like(t)
        
        for i in range(amplitudes.shape[0]):
            signal += ampEnvelope * amplitudes[i] * np.sin(2*np.pi*frequences[i]*t)
 
        return signal 

    
    diapason = 600
    fondamental = diapason * 0.5
    
    FList = [fondamental,
            2*fondamental,
            3*fondamental,
            4*fondamental,
            5*fondamental]
    
    FListCorps = [40, 50, 60, 70]
    
    signal = np.zeros_like(t)


    # Simple diapasion
    if signalPreset == "diapason":
        signal = np.sin(2*np.pi*diapason*t)
        return signal
    
    
    # Corde idéale
    for i in FList:
        signal += np.sin(2*np.pi*i*t)
    
    if signalPreset == "cordeIdeale":
        return signal    


    # Ajout de l'envelope d'amplitude
    signal = ampEnvelope*signal
    
    if signalPreset == "guitareSimulee":
        return signal
    
    
    # Ajout des modes de corps
    for i in FListCorps:
        signal += ampEnvelope * np.sin(2*np.pi*i*t)
  
    if signalPreset == "guitareCorps":
        return signal


    # Ajout des modes doubles
    for i in FList:
        signal += ampEnvelope * np.sin(2*np.pi*1.01*i*t)
           
    if signalPreset == "guitareModesDoubles":
       return signal 


    # Ajout du bruit
    bruit = np.random.randn(signal.size) * 0.1
    signal += bruit
    
    if signalPreset == "guitareBruit":
        return signal
                    
    else:
        print("Mauvais paramètre")
        return signal