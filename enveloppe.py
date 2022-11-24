import numpy as np
import matplotlib.pyplot as plt 
plt.close('all')


attackTime = 1000 # ms
decayTime = 1000
samplerate = 44100

attackEnvelope = np.flip(1 - np.linspace(0, attackTime, attackTime*samplerate)**2) 
decayEnvelope = np.flip(np.linspace(0, decayTime, decayTime*samplerate )**2)

ampEnveloppe = np.concatenate((attackEnvelope, decayEnvelope))


plt.plot(ampEnveloppe)
plt.show()