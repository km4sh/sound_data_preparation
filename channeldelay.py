import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import operator
from scipy import fftpack, signal
from collections import Counter

def framedelay( wave1, wave2, sampleRate, sec ):
    samp = range(0, len(wave2)-(2*sec*sampleRate), 2*sec*sampleRate)
    delay1 = []
    delay2 = []
    for i in samp:
        curOrigiChannel = wave1[i:i+(sec*sampleRate)]
        curMultiChannel = wave2[i:i+(sec*sampleRate)]
        singleChann1 = [curMultiChannel[i][0] for i in range(len(curMultiChannel))]
        singleChann2 = [curMultiChannel[i][1] for i in range(len(curMultiChannel))]
        fftChann1 = fftpack.fft(singleChann1)
        fftChann2 = fftpack.fft(singleChann2)
        fftOrigin = fftpack.fft(curOrigiChannel)
        fftOriginr = - fftOrigin.conjugate()
        temp1 = np.argmax((np.abs(fftpack.ifft(fftChann1*fftOriginr)))[:sampleRate])
        temp2 = np.argmax((np.abs(fftpack.ifft(fftChann2*fftOriginr)))[:sampleRate])
        print('current samples:', i, '\tdelay1:', temp1, '\tdelay2:', temp2)
        delay1.append( temp1 )
        delay2.append( temp2 )
        del temp1,temp2
    return delay1, delay2

def plotdelay(wave1, wave2, sampleRate, sec):
    delay1, delay2 = framedelay(wave1, wave2, sampleRate, sec)
    plt.figure(1)
    plt.subplot(211)
    plt.plot(samp, delay1, 'b', samp, delay2, 'r')
    plt.subplot(212)
    diffDelay = list(map(operator.sub, delay1, delay2))
    plt.plot(samp, diffDelay)
    plt.show()

def wavedelay(wave1, wave2, sampleRate, sec):
    delay1, delay2 = framedelay(wave1, wave2, sampleRate, sec)
    print('framedelay.end.')
    cnt = Counter()
    for delay in delay1:
        cnt[delay] += 1
        print(cnt.most_common(1)[0][0])
    return cnt.most_common(1)[0][0]
