import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

import operator
from scipy import fftpack, signal
from collections import Counter


multiChannel, sampleRate = sf.read('/home/simon/Music/rec_jan25/rec_file/rec_combined_vctk1.wav')
origiChannel, originalSR = sf.read('/home/simon/Music/rec_jan25/combined_vctk1.wav')
samp = range(0, len(multiChannel)-(200*sampleRate), 200*sampleRate)
delay1 = []
delay2 = []
for i in samp:
    curMultiChannel = multiChannel[i:i+(50*sampleRate)]
    curOrigiChannel = origiChannel[i:i+(50*sampleRate)]
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


plt.figure(1)
plt.subplot(211)
plt.plot(samp, delay1, 'b', samp, delay2, 'r')
plt.subplot(212)
diffDelay = list(map(operator.sub, delay1, delay2))
plt.plot(samp, diffDelay)
plt.show()
cnt = Counter()
for delay in delay1:
    cnt[delay] += 1
print(cnt.most_common(1)[0][0])

# def wavedelay(file1, file2, 50):
#     delay = framedelay(file1, file2, 50)
#     cnt = Counter()
#     for delay in delay:
#         cnt[delay] += 1
#     return cnt.most_common(1)[0][0]
