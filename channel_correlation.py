import numpy as np
import soundfile as sf


import operator
from scipy import fftpack, signal
from collections import Counter


multiChannel, sampleRate = sf.read('/seagate2t/rec/stereo/aligned_rec_combined_timit2.wav')
# origiChannel, originalSR = sf.read('/seagate2t/rec/mono/aligned_combined_timit2.wav')
samp = range(0, len(multiChannel)-(15*sampleRate), 15*sampleRate)
delay1 = []
delay2 = []
for i in samp:
    curMultiChannel = multiChannel[i:i+(30*sampleRate)]
#    curOrigiChannel = origiChannel[i:i+(30*sampleRate)]
    singleChann1 = [curMultiChannel[i][0] for i in range(len(curMultiChannel))]
    singleChann2 = [curMultiChannel[i][1] for i in range(len(curMultiChannel))]
    fftChann1 = fftpack.fft(singleChann1)
    fftChann2 = fftpack.fft(singleChann2)
    fftChann1r = - fftChann1.conjugate()
    fftChann2r = - fftChann2.conjugate()
#    fftOrigin = fftpack.fft(curOrigiChannel)
#    fftOriginr = - fftOrigin.conjugate()
    temp1 = np.argmax((np.abs(fftpack.ifft(fftChann1*fftChann2r)))[:sampleRate])
    temp2 = np.argmax((np.abs(fftpack.ifft(fftChann2*fftChann1r)))[:sampleRate])
    print('current samples:', i, '\tdelay1:', temp1, '\tdelay2:', temp2)
    delay1.append( temp1 )
    delay2.append( temp2 )
    del temp1,temp2

