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
origPath = '/seagate2t/simon/kawaii/data/show_orig.hdf5'
savePath = '/seagate2t/simon/kawaii/data/fix/fix_show_allsnr.hdf5'
rirPath = '/seagate2t/simon/kawaii/data/multi_sources/ms_rir.h5'
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
        theta = np.arccos(vector[2]/distance)*180/np.pi
        phi = np.arccos(vector[0]/(distance*np.sin(theta)))*180/np.pi
        curRoom = saveFile.create_group(str(roomSize))
        print('|{0:>15}|{1:<30.2f}|'.format('volume', volume))
        print('|{0:>15}|{1:<30.2f}|'.format('angle', angle))
        print('|{0:>15}|{1:<30.2f}|'.format('distance', distance))
        print('|{0:>15}|{1:<30.2f}|'.format('noise angle', noiseAngle))
        print('|{0:>15}|{1:<30.2f}|'.format('spherical', distance))
        print('|{0:>15}|{1:<30.2f}|'.format('', theta))
        print('|{0:>15}|{1:<30.2f}|'.format('', phi))
        print('+{0:->15}+{1:-<30}+'.format('-', '-'))
        for wavPath in filePathes:
            t = time.time()
            head, fileName = os.path.split(wavPath)

            clean, sr = sf.read(wavPath)
            maxi = max(abs(clean))
            clean = [samp*(1/maxi) for samp in clean]                     # magnitude normalization.

            noiseExt = np.resize(noise, len(clean))

            vad = VAD(np.asarray(clean[19960521:19960521+120*sr]), sr, threshold=0.95)
            ratio = list(vad).count(1)/len(vad)
            magWave = np.sum(np.square(clean))/(ratio*len(clean))
            # print(ratio, len(clean[19960521:19960521+120*sr]), len(vad), list(vad).count(1))
            print('|{0:>15}|{1:<30}|'.format('file name', fileName))
            print('|{0:>15}|{1:<30.4f}|'.format('vad ratio', ratio))
            print('|{0:>15}|{1:<30}|'.format('conv', 'start'))

            fakeMic1 = np.convolve(conv1, clean)
            fakeMic2 = np.convolve(conv2, clean)

            maxi = max(abs(fakeMic1))
            fakeMic1 = [samp*(1/maxi) for samp in fakeMic1]                     # magnitude normalization.
            maxi = max(abs(fakeMic2))
            fakeMic2 = [samp*(1/maxi) for samp in fakeMic2]                     # magnitude normalization.

            noiseMic1 = np.convolve(nConv1, noiseExt)
            noiseMic2 = np.convolve(nConv2, noiseExt)

            print('|{0:>15}|{1:<30}|'.format('conv', 'finished'))

            magFakeMic = np.sum(np.square(fakeMic1))/(ratio*len(fakeMic1))
            magNoiseMic = np.mean(np.square(noiseMic1))

            try:
                assert origFile[fileName].shape[0] == stereo.shape[0]
            except AssertionError:
                import ipdb; ipdb.set_trace()
            except:
                origFile.create_dataset(fileName, data=clean)

            for snr in [-6, -3, 0, 3, 6]:
                noiseMic1 = [p*(magFakeMic/(magNoiseMic*10**(snr/10))) for p in noiseMic1]
                noiseMic2 = [p*(magFakeMic/(magNoiseMic*10**(snr/10))) for p in noiseMic2]
                channel1 = np.asarray(fakeMic1) + np.asarray(noiseMic1)
                channel2 = np.asarray(fakeMic2) + np.asarray(noiseMic2)
                stereo = np.vstack((channel1, channel2)).T
                print('|{0:>15}|{1:<30}|'.format('snr '+str(snr), 'rebuild finished'))
                print('+{0:->15}+{1:-<30}+'.format('-', '-'))
                flag = 0
                curDset = curRoom.create_dataset(fileName+str(snr), data=stereo)
                curDset.attrs.create('mono', fileName, dtype=h5py.special_dtype(vlen=str))
                curDset.attrs.create('volume', volume, dtype=float)
                curDset.attrs.create('angle', angle, dtype=float)
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
