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
                presetSignal: Literal["diapason",
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
    
    preDelay = 50 #ms
    prePad = np.zeros(int(0.001*50*samplerate))

    duree = duree - 0.001* preDelay
    t = np.arange(0, duree, 1/samplerate)

    diapason: int = 440 #Hz
    freqMiGrave: float = 82.0 #Hz
    nHarmoniques:int = 40
    vecFrequences = np.arange(freqMiGrave, nHarmoniques*freqMiGrave, freqMiGrave)
    damping: float = 1E-2
    bodydamping: float = 0.1
    inharmonicdamping: float = 5*damping
    modesCorps = [90, 200, 250]
    inharmonicCoefficient: float = 1E-4

    # diapason simple
    if presetSignal == "diapason":
        signal = np.sin(2*np.pi*diapason*t)
    

    # corde ideale : empilement de sinusoides
    elif presetSignal == "cordeIdeale":
        signal = np.zeros_like(t)

        for freq in vecFrequences:
            signal += np.sin(2*np.pi*freq*t)


    # guitare simulee : sinusoides ammorties exponentiellement
    elif presetSignal == "guitareSimulee":
        signal = np.zeros_like(t)

        for freq in vecFrequences:
            signal += np.sin(2*np.pi*freq*t) * np.exp(-damping*freq*t)


    # guitare simulee avec les modes de corps
    elif presetSignal == "guitareCorps":
        signal = np.zeros_like(t)

        for freq in vecFrequences:
            signal += np.sin(2*np.pi*freq*t) * np.exp(-damping*freq*t)

        for freq in modesCorps:
            signal += np.sin(2*np.pi*freq*t) * np.exp(-bodydamping*freq*t)


    # guitare simulee avec les modes inharmoniques
    elif presetSignal == "guitareModesDoubles":
        signal = np.zeros_like(t)

        for freq in vecFrequences:
            signal += np.sin(2*np.pi*freq*t) * np.exp(-damping*freq*t)
            signal += np.sin(2*np.pi*freq*np.sqrt(1 + inharmonicCoefficient**2)*t) * np.exp(-inharmonicdamping*freq*t)

        # for freq in modesCorps:
        #     signal += np.sin(2*np.pi*freq*t) * np.exp(-bodydamping*freq*t)


    # guitare avec bruit additif
    elif presetSignal == "guitareBruit":
        signal = np.zeros_like(t)

        for freq in vecFrequences:
            signal += np.sin(2*np.pi*freq*t) * np.exp(-damping*freq*t)
            signal += np.sin(2*np.pi*freq * np.sqrt(1 + inharmonicCoefficient**2) * t) * np.exp(-inharmonicdamping*freq*t)

        for freq in modesCorps:
            signal += np.sin(2*np.pi*freq*t) * np.exp(-bodydamping*freq*t)

        SNR: int = -10
        SNRLin = 10**(SNR/20)
        noise = SNRLin * (2*np.random.rand(t.size) - 1)

        signal += noise


    else:
        print("mauvais parametre")
        signal = np.zeros_like(t)

    signal = np.concatenate((prePad, signal))
    return signal