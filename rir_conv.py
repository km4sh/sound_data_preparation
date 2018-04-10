import os
import numpy as np
import soundfile as sf

filePath = '/seagate2t/rec_jan12'
convPath = '/home/zhumy/simon/rir_conv/audio_h_Group2'
expName = 'exp1grp2'
filenames = [f for f in os.listdir(filePath)]
convnames = [c for c in os.listdir(convPath)]
print(convnames)
print(filenames)
for convname in [c for c in convnames if c.endswith('.wav')]:
    if not os.path.exists(os.path.join(filePath,expName,convname.rstrip('.wav'))):
        os.makedirs(os.path.join(filePath,expName,convname.rstrip('.wav')))
for filename in [f for f in filenames if f.endswith('.wav')]:
    wave, wavesr = sf.read(os.path.join(filePath, filename))
    magWave = sum([abs(p) for p in wave])/len(wave)
    print('#', filename, 'loaded.')
    print('# The magnitude of original wave is ', magWave)
    for convname in [c for c in convnames if c.endswith('.wav')]:
        if not os.path.exists(os.path.join(filePath,expName,convname.rstrip('.wav'),filename.rstrip('.wav')+'_conv1.wav')):
            conv, convsr = sf.read(os.path.join(convPath, convname))
            convCh1 = [conv[i][0] for i in range(len(conv))]
            convCh2 = [conv[i][1] for i in range(len(conv))]
            print('##', convname, 'loaded.')
            print('## now convolving...')
            fakeMic1 = np.convolve(convCh1, wave)
            fakeMic2 = np.convolve(convCh2, wave)
            magFakeMic1 = sum([abs(p) for p in fakeMic1])/len(fakeMic1)
            magFakeMic2 = sum([abs(p) for p in fakeMic2])/len(fakeMic2)
            print('## the magnitude of fakeMic1 is ', magFakeMic1)
            print('## the magnitude of fakeMic2 is ', magFakeMic2)
            print('## now rebuilding the magnitude...')
            fakeMic1 = [p*(magWave/magFakeMic1) for p in fakeMic1]
            fakeMic2 = [p*(magWave/magFakeMic2) for p in fakeMic2]
            sf.write(os.path.join(filePath,expName,convname.rstrip('.wav'),filename.rstrip('.wav')+'_conv1.wav'), fakeMic1, wavesr)
            sf.write(os.path.join(filePath,expName,convname.rstrip('.wav'),filename.rstrip('.wav')+'_conv2.wav'), fakeMic2, wavesr)
            print('##', filename, convname, 'convolution compelete.')

