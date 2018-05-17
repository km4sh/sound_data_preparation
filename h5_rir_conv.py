import os
import h5py
import glob
import time
import numpy as np
import soundfile as sf
from functools import reduce
from math import hypot

filePath = '/seagate2t/simon/kawaii/data/orig'
savePath = '/seagate2t/simon/kawaii/data/fix_conv.hdf5'
origResave = '/seagate2t/simon/kawaii/data/fix_orig.hdf5'
rirPath = '/seagate2t/simon/kawaii/data/rir_fixed.h5'

filePathes = glob.glob(filePath+'/**/*.wav', recursive=True)

count = 0
rirSet = h5py.File(rirPath, 'r')
saveFile = h5py.File(savePath, 'w', libver='latest')
origFile = h5py.File(origResave, 'w', libver='latest')

rirKey = list(rirSet.keys())
print('+{0:->15}+{1:-<30}+'.format('-', '-'))
for room in rirKey:
    try:
        print('|{0:>15}|{1:<30}|'.format('room', room))
        rir = rirSet[room]
        conv1 = rir[:,0]
        conv2 = rir[:,1]
        mic1 = np.asarray([float(t) for t in rir.attrs['mic1'].split()])
        mic2 = np.asarray([float(t) for t in rir.attrs['mic2'].split()])
        source = np.asarray([float(t) for t in rir.attrs['source_p'].split()])
        roomSize = np.asarray([float(t) for t in rir.attrs['L'].split()])
        volume = reduce(lambda x, y: x*y, roomSize)
        angle = float(rir.attrs['angle'])
        distance = reduce(lambda x, y: hypot(x, y), source - (mic1 + mic2)/2)
        curRoom = saveFile.create_group(str(roomSize))
        print('|{0:>15}|{1:<30.2f}|'.format('volume', volume))
        print('|{0:>15}|{1:<30.2f}|'.format('angle', angle))
        print('|{0:>15}|{1:<30.2f}|'.format('distance', distance))
        print('+{0:->15}+{1:-<30}+'.format('-', '-'))
        for wavPath in filePathes:
            t = time.time()
            head, fileName = os.path.split(wavPath)
            print('|{0:>15}|{1:<30}|'.format('file name', fileName))
            clean, sr = sf.read(wavPath)
            magWave = sum([abs(p) for p in clean])/len(clean)
            print('|{0:>15} {1:<30}|'.format('conv', 'start'))
            fakeMic1 = np.convolve(conv1, clean)
            fakeMic2 = np.convolve(conv2, clean)
            print('|{0:>15} {1:<30}|'.format('conv', 'finished'))
            magFakeMic1 = sum([abs(p) for p in fakeMic1])/len(fakeMic1)
            magFakeMic2 = sum([abs(p) for p in fakeMic2])/len(fakeMic2)
            fakeMic1 = [p*(magWave/magFakeMic1) for p in fakeMic1]
            fakeMic2 = [p*(magWave/magFakeMic2) for p in fakeMic2]
            stereo = np.vstack((fakeMic1, fakeMic2)).T
            print('|{0:>15}|{1:<30}|'.format('rebuild', 'finished'))
            print('+{0:->15}+{1:-<30}+'.format('-', '-'))
            mono = np.append(clean, np.zeros(len(stereo) - len(clean)))
            assert len(stereo) == len(mono)
            try:
                origFile[fileName]
            except:
                curOrig = origFile.create_dataset(fileName, data=mono)
                print('|{0:>15}|{1:<30}|'.format('orig hdf5', fileName+' set'))
            curDset = curRoom.create_dataset(fileName, data=stereo)
            curDset.attrs.create('mono', fileName, dtype=h5py.special_dtype(vlen=str))
            curDset.attrs.create('volume', volume, dtype=float)
            curDset.attrs.create('angle', angle, dtype=float)
            curDset.attrs.create('distance', distance, dtype=float)
            t = time.time() - t
            print('|{0:>15} {1:<30}|'.format(room, fileName+' done'))
            print('|{0:>15}|{1:<30.2f}|'.format('time', t))
            print('+{0:->15}+{1:-<30}+'.format('-', '-'))
    except KeyboardInterrupt:
        break
saveFile.swmr_mode = True
origFile.swmr_mode = True
saveFile.flush()
saveFile.close()
origFile.flush()
origFile.close()
print('finished.')
