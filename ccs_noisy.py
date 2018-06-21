import os
import h5py
import glob
import time
import numpy as np
import soundfile as sf
from vad import VAD
from functools import reduce
from math import hypot

filePath = '/seagate2t/simon/kawaii/data/orig'
noisePath = '/seagate2t/simon/kawaii/data/busesnoise.wav'
origPath = '/seagate2t/simon/kawaii/data/clean_ood.hdf5'
savePath = '/seagate2t/simon/kawaii/data/noisy_ood.hdf5'
rirPath = '/seagate2t/simon/kawaii/rir_conv/ood.h5'
filePathes = glob.glob(filePath+'/**/*.wav', recursive=True)

rirSet = h5py.File(rirPath, 'r')
origFile = h5py.File(origPath, 'w', libver='latest', swmr=True)
saveFile = h5py.File(savePath, 'w', libver='latest', swmr=True)
noise, sampleRate = sf.read(noisePath)
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
        theta = np.arccos(vector[2]/distance)
        rho = hypot(vector[0], vector[1])
        phi = np.arctan(vector[1]/vector[0])
        z = vector[2]

        curRoom = saveFile.create_group(str(roomSize))
        print('|{0:>15}|{1:<30.2f}|'.format('volume', volume))
        print('|{0:>15}|{1:<30.2f}|'.format('angle', angle))
        print('|{0:>15}|{1:<30.2f}|'.format('distance', distance))
        print('|{0:>15}|{1:<30.2f}|'.format('noise angle', noiseAngle))
        print('|{0:>15}|{1:<30.2f}|'.format('ccs rho', rho))
        print('|{0:>15}|{1:<30.2f}|'.format('', phi))
        print('|{0:>15}|{1:<30.2f}|'.format('', z))
        print('+{0:->15}+{1:-<30}+'.format('-', '-'))
        for wavPath in filePathes:
            t = time.time()
            head, fileName = os.path.split(wavPath)

            clean, sr = sf.read(wavPath)
            maxi = max(abs(clean))
            clean = [samp*(0.7/maxi) for samp in clean]                     # magnitude normalization.

            noiseExt = np.resize(noise, len(clean))

            magWave = np.mean(np.square(clean))

            print('|{0:>15}|{1:<30}|'.format('file name', fileName))
            print('|{0:>15}|{1:<30}|'.format('conv', 'start'))

            fakeMic1 = np.convolve(conv1, clean)
            fakeMic2 = np.convolve(conv2, clean)

            noiseMic1 = np.convolve(nConv1, noiseExt)
            noiseMic2 = np.convolve(nConv2, noiseExt)

            print('|{0:>15}|{1:<30}|'.format('conv', 'finished'))

            magFakeMic = np.mean(np.square(fakeMic1))
            magNoiseMic = np.mean(np.square(noiseMic1))

            print('+{0:->15}+{1:-<30}+'.format('-', '-'))
            for snr in [3, 6, 15, 20]:
                scale = magFakeMic/(magNoiseMic*(10**(snr/10)))
                noiseMic1 = [p*scale for p in noiseMic1]
                noiseMic2 = [p*scale for p in noiseMic2]
                channel1 = np.asarray(fakeMic1) + np.asarray(noiseMic1)
                channel2 = np.asarray(fakeMic2) + np.asarray(noiseMic2)
                stereo = np.vstack((channel1, channel2)).T
                print('|{0:>15}|{1:<30.4f}|'.format('scale', scale))
                print('|{0:>15}|{1:<30}|'.format('snr '+str(snr), 'rebuild finished'))
                print('+{0:->15}+{1:-<30}+'.format('-', '-'))
                flag = 0
                curDset = curRoom.create_dataset(fileName+str(snr), data=stereo)
                curDset.attrs.create('mono', fileName, dtype=h5py.special_dtype(vlen=str))
                curDset.attrs.create('volume', volume, dtype=float)
                curDset.attrs.create('angle', angle, dtype=float)
                curDset.attrs.create('distance', distance, dtype=float)
                curDset.attrs.create('rho', rho, dtype=float)
                curDset.attrs.create('phi', phi, dtype=float)
                curDset.attrs.create('z', z, dtype=float)
                curDset.attrs.create('theta', theta, dtype=float)
                curDset.attrs.create('snr', snr, dtype=float)
                curDset.attrs.create('mp1', rir.attrs['mp1'], dtype=h5py.special_dtype(vlen=str))
                curDset.attrs.create('mp2', rir.attrs['mp2'], dtype=h5py.special_dtype(vlen=str))
                curDset.attrs.create('sp', rir.attrs['sp'], dtype=h5py.special_dtype(vlen=str))
                curDset.attrs.create('roomsize', rir.attrs['roomsize'], dtype=h5py.special_dtype(vlen=str))
                curDset.attrs.create('noise angle', noiseAngle, dtype=float)
                flag = 1
            try:
                assert origFile[curDset.attrs['mono']].shape[0] == stereo.shape[0]
            except AssertionError:
                try:
                    clean.extend(np.zeros(stereo.shape[0] - len(clean)))
                    origFile[curDset.attrs['mono']] = clean
                except:
                    import ipdb; ipdb.set_trace()
            except:
                clean.extend(np.zeros(stereo.shape[0] - len(clean)))
                origFile.create_dataset(fileName, data=clean)
                assert origFile[curDset.attrs['mono']].shape[0] == stereo.shape[0]
            t = time.time() - t
            print('|{0:>15}|{1:<30.2f}|'.format('time', t))
            print('+{0:->15}+{1:-<30}+'.format('-', '-'))
    except KeyboardInterrupt:
        if(flag == 0):
            del curRoom[fileName]
            print('|{0:>15}|{1:<30.2f}|'.format(fileName, 'dSet deleted'))
            print('+{0:->15}+{1:-<30}+'.format('-', '-'))
        if(list(curRoom.keys())==[]):
            del saveFile[str(roomSize)]
            print('|{0:>15}|{1:<30.2f}|'.format(str(roomSize), 'room deleted'))
            print('+{0:->15}+{1:-<30}+'.format('-', '-'))
        break
saveFile.swmr_mode = True
saveFile.flush()
saveFile.close()
origFile.close()
print('+{0:->15}-{1:-<30}+'.format(' all ', ' finished '))
