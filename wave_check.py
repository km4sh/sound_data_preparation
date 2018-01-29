import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from scipy import fftpack, signal

wave1, sampleRate = sf.read('/home/simon/rec_jan12/aligned_combined_timit3.wav')
wave2, sampleRate = sf.read('/home/simon/rec_jan12/aligned_rec_combined_timit3.wav')

print(len(wave1), len(wave2))

curOrigiChannel = wave1[:15*sampleRate]
curMultiChannel = wave2[:15*sampleRate]

singleChann1 = [curMultiChannel[i][0] for i in range(len(curMultiChannel))]
singleChann2 = [curMultiChannel[i][1] for i in range(len(curMultiChannel))]

fftChann1 = fftpack.fft(singleChann1)
fftChann2 = fftpack.fft(singleChann2)
fftOrigin = fftpack.fft(curOrigiChannel)

fftOriginr = - fftOrigin.conjugate()
corr1 = (np.abs(fftpack.ifft(fftChann1*fftOriginr)))[:sampleRate]
corr2 = (np.abs(fftpack.ifft(fftChann2*fftOriginr)))[:sampleRate]
delay1 = np.argmax(corr1)
delay2 = np.argmax(corr2)

print(delay1, delay2)

plt.figure(1)
plt.subplot(311)
plt.plot(curOrigiChannel)
plt.subplot(312)
plt.plot(singleChann1)
plt.subplot(313)
plt.plot(singleChann2)

plt.figure(2)
plt.subplot(211)
plt.plot(corr1)
plt.subplot(212)
plt.plot(corr2)
plt.show()
