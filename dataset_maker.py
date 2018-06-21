import os
import h5py
import glob
import time
import numpy as np
import soundfile as sf
import random
import string
from functools import reduce
from math import hypot
from math import isnan

cleanInput = '/seagate2t/simon/kawaii/data/orig'
noiseInput = '/seagate2t/simon/kawaii/data/busesnoise.wav'
labelOutput = '/seagate2t/simon/kawaii/data/jun13_orig.hdf5'
datasetOutput = '/seagate2t/simon/kawaii/data/jun13_noisy.hdf5'
rirInput = '/seagate2t/simon/kawaii/data/rir/ms_rir.h5'
previewPath = '/seagate2t/simon/kawaii/data/preview/'

cleanInputes = glob.glob(cleanInput+'/**/*.wav', recursive=True)

rirSet = h5py.File(rirInput, 'r')
labelFile = h5py.File(labelOutput, 'w', libver='latest', swmr=True)
datasetFile = h5py.File(datasetOutput, 'w', libver='latest', swmr=True)
noise, sampleRate = sf.read(noiseInput)
lenNoise = len(noise)

print('+{0:->15}+{1:-<30}+'.format('-', '-'))


for room in list(rirSet.keys()):
    try:
        print('|{0:>15}|{1:<30}|'.format('room', room))
        rir = rirSet[room]['source1']
        noiseRir = rirSet[room]['source4']
        conv1 = rir[:,0]
        conv2 = rir[:,1]
        nConv1 = noiseRir[:,0]
        nConv2 = noiseRir[:,1]
        mic1 = np.asarray([float(t) for t in rir.attrs['mp1'].split()])
        mic2 = np.asarray([float(t) for t in rir.attrs['mp2'].split()])
        speaker = np.asarray([float(t) for t in rir.attrs['sp'].split()])
        roomSize = np.asarray([float(t) for t in rir.attrs['roomsize'].split()])
        noisePos = np.asarray([float(t) for t in noiseRir.attrs['sp'].split()])
        volume = reduce(lambda x, y: x*y, roomSize)
        angle = np.arccos(np.clip(np.dot(mic2 - mic1, speaker - mic1), -1.0, 1.0)) * 360 / (2 * np.pi)
        vector = speaker - (mic1 + mic2)/2
        noiseAngle = np.arccos(np.clip(np.dot(mic2 - mic1, noisePos - mic1), -1.0, 1.0)) * 360 / (2 * np.pi)
        distance = reduce(lambda x, y: hypot(x, y), vector)
        theta = np.arccos(vector[2]/distance)*180/np.pi
        phi = np.arccos(vector[0]/(distance*np.sin(theta)))*180/np.pi
        if(isnan(phi) or isnan(theta)):
            continue
        curRoom = datasetFile.create_group(str(roomSize))
        print('|{0:>15}|{1:<30.2f}|'.format('volume', volume))
        print('|{0:>15}|{1:<30.2f}|'.format('angle', angle))
        print('|{0:>15}|{1:<30.2f}|'.format('distance', distance))
        print('|{0:>15}|{1:<30.2f}|'.format('noise angle', noiseAngle))
        print('|{0:>15}|{1:<30.2f}|'.format('spherical', distance))
        print('|{0:>15}|{1:<30.2f}|'.format('', theta))
        print('|{0:>15}|{1:<30.2f}|'.format('', phi))
        print('+{0:->15}+{1:-<30}+'.format('-', '-'))

        for wavInput in cleanInputes:
            t = time.time()
            head, fileName = os.path.split(wavInput)
            clean, sr = sf.read(wavInput)
            clean = clean
            maxi = max(abs(clean))
            clean = [samp*(0.5/maxi) for samp in clean]                     # magnitude normalization.
            engClean = np.mean(np.square(clean))

            noiseExt = np.resize(noise, len(clean))

            print('|{0:>15}|{1:<30}|'.format('file name', fileName))
            print('|{0:>15}|{1:<30}|'.format('conv', 'start'))

            fakeMic1 = np.convolve(conv1, clean)
            fakeMic2 = np.convolve(conv2, clean)

            engFakeMic = np.mean(np.square(fakeMic1))
            scaleRatio = np.sqrt(engClean/engFakeMic)
            print('|{0:>15}|{1:<30.4f}|'.format('clean ratio', scaleRatio))

            fakeMic1 = [samp*scaleRatio for samp in fakeMic1]                     # magnitude normalization.
            fakeMic2 = [samp*scaleRatio for samp in fakeMic2]                     # magnitude normalization.

            noiseMic1 = np.convolve(nConv1, noiseExt)
            noiseMic2 = np.convolve(nConv2, noiseExt)
            engNoiseMic = np.mean(np.square(noiseMic1))

            print('|{0:>15}|{1:<30}|'.format('conv', 'finished'))

            for snr in [0]:
                snrScale = (engClean/(engNoiseMic*10**(10*(snr/3.8+0.6)/10)))
                scaledNoise1 = [p*snrScale for p in noiseMic1]
                scaledNoise2 = [p*snrScale for p in noiseMic2]
                channel1 = np.asarray(fakeMic1) + np.asarray(scaledNoise1)
                channel2 = np.asarray(fakeMic2) + np.asarray(scaledNoise2)
                stereo = np.vstack((channel1, channel2)).T
                print('+{0:->15}+{1:-<30}+'.format('-', '-'))
                print('|{0:>15}|{1:<30}|'.format('noisy ratio', snrScale))
                print('|{0:>15}|{1:<30}|'.format('snr '+str(snr), 'rebuild finished'))
                flag = 0
                salt = ''.join(random.sample(string.ascii_letters + string.digits, 16))
                print('|{0:>15}|{1:<30}|'.format('salt', salt))
                curDset = curRoom.create_dataset(salt, data=stereo)
                sf.write(previewPath+'label.wav', clean[:sr*5], sr)
                sf.write(previewPath+str(snr)+'noisy.wav', stereo[:sr*5], sr)
                curDset.attrs.create('mono', fileName, dtype=h5py.special_dtype(vlen=str))
                curDset.attrs.create('volume', theta, dtype=float)
                curDset.attrs.create('angle', phi, dtype=float)
                curDset.attrs.create('distance', distance, dtype=float)
                curDset.attrs.create('theta', theta, dtype=float)
                curDset.attrs.create('phi', phi, dtype=float)
                curDset.attrs.create('snr', snr, dtype=float)
                curDset.attrs.create('mp1', rir.attrs['mp1'], dtype=h5py.special_dtype(vlen=str))
                curDset.attrs.create('mp2', rir.attrs['mp2'], dtype=h5py.special_dtype(vlen=str))
                curDset.attrs.create('sp', rir.attrs['sp'], dtype=h5py.special_dtype(vlen=str))
                curDset.attrs.create('roomsize', rir.attrs['roomsize'], dtype=h5py.special_dtype(vlen=str))
                curDset.attrs.create('noise angle', noiseAngle, dtype=float)
                flag = 1
            try:
                assert labelFile[curDset.attrs['mono']].shape[0] == stereo.shape[0]
            except AssertionError:
                try:
                    clean.extend(np.zeros(stereo.shape[0] - len(clean)))
                    labelFile[curDset.attrs['mono']] = clean
                except:
                    import ipdb; ipdb.set_trace()
            except:
                clean.extend(np.zeros(stereo.shape[0] - len(clean)))
                labelFile.create_dataset(fileName, data=clean)
                assert labelFile[curDset.attrs['mono']].shape[0] == stereo.shape[0]
            t = time.time() - t
            print('+{0:->15}+{1:-<30}+'.format('-', '-'))
            print('|{0:>15}|{1:<30.2f}|'.format('time', t))
            print('+{0:->15}+{1:-<30}+'.format('-', '-'))
    except KeyboardInterrupt:
        if(flag == 0):
            del curRoom[fileName]
            print('|{0:>15}|{1:<30}|'.format(fileName, 'dSet deleted'))
            print('+{0:->15}+{1:-<30}+'.format('-', '-'))
        if(list(curRoom.keys())==[]):
            del datasetFile[str(roomSize)]
            print('|{0:>15}|{1:<30}|'.format(str(roomSize), 'room deleted'))
            print('+{0:->15}+{1:-<30}+'.format('-', '-'))
        break
datasetFile.swmr_mode = True
datasetFile.flush()
datasetFile.close()
labelFile.close()
print('+{0:->15}-{1:-<30}+'.format(' all ', ' finished '))
