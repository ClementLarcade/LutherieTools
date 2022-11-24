import numpy as np


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
                presetSignal: str
                ) -> tuple[np.ndarray, np.ndarray]:
    """_summary_
    Cette fonction génère les différents signaux de test pour tester le fonctionnement
    de l'algorithme. 
    

    Args:
        duree (float): duree du signal 
        samplerate (int): fréquence d'échantillonnage 
        presetSignal (str): "Envelope", "battements", "sinusAleatoires", "diapason", "cordeIdeale", "guitareSimulee", "guitareCorps", "guitareModesDobules", "guitareBruit"

    Returns:
        t, singal : vecteur temps, signal test
    """    
    
    t = np.arange(0, duree, 1/samplerate)
    preDelay = 50 # ms
    
    attackTime = 50 # ms
    decayTime = 300
    
    prePad = np.zeros(int(preDelay*samplerate*0.001))
    attackEnvelope = np.flip(1 - np.linspace(0, 1, int(attackTime*samplerate*0.001))**2) 
    decayEnvelope = np.flip(np.linspace(0, 1, int(decayTime*samplerate*0.001) )**2)

    ampEnvelope = np.concatenate((prePad, attackEnvelope, decayEnvelope))
    ampEnvelope = np.pad(ampEnvelope, (0, t.size - ampEnvelope.size))

    if presetSignal == "Envelope":
        return t, ampEnvelope
    
    if presetSignal == "battements":
        signal = np.sin(2*np.pi*440*t) + 0.5 * np.sin(2*np.pi*450*t)
        return t, signal

    if presetSignal == "sinusAleatoires":
        taille = 10
        
        amplitudes = 0.5 * np.random.random(taille) + 0.5
        frequences = 1000 * np.random.random(taille) + 100
        print(f"amplitudes = {amplitudes}")
        print(f"frequences = {frequences}")
        signal = np.zeros_like(t)
        
        for i in range(amplitudes.shape[0]):
            signal += ampEnvelope * amplitudes[i] * np.sin(2*np.pi*frequences[i]*t)
 
        return t, signal 
        
    
    diapason = 440
    fondamental = diapason * 0.5
    
    FList = [fondamental,
            2*fondamental,
            3*fondamental,
            4*fondamental,
            5*fondamental]
    
    FListCorps = [40, 50, 60, 70]
    
    signal = np.zeros_like(t)


    # Simple diapasion
    if presetSignal == "diapason":
        signal = np.sin(2*np.pi*fondamental*t)
        return t, signal
    
    
    # Corde idéale
    for i in FList:
        signal += np.sin(2*np.pi*i*t)
    
    if presetSignal == "cordeIdeale":
        return t, signal    


    # Ajout de l'envelope d'amplitude
    signal = ampEnvelope*signal
    
    if presetSignal == "guitareSimulee":
        return t, signal
    
    
    # Ajout des modes de corps
    for i in FListCorps:
        signal += ampEnvelope * np.sin(2*np.pi*i*t)
  
    if presetSignal == "guitareCorps":
        return t, signal


    # Ajout des modes doubles
    for i in FList:
        signal += ampEnvelope * np.sin(2*np.pi*1.01*i*t)
           
    if presetSignal == "guitareModesDoubles":
       return t, signal 


    # Ajout du bruit
    bruit = np.random.randn(signal.size) * 0.5
    signal += bruit
    
    if presetSignal == "guitareBruit":
        return t, signal
                    
    else:
        print("Mauvais paramètre")
        return t, signal