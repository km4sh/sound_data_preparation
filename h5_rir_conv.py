import os
import h5py
import glob
import time
import numpy as np
import soundfile as sf
from functools import reduce
from math import hypot

filePath = '/seagate2t/simon/kawaii/data/orig'
savePath = '/seagate2t/simon/kawaii/data/h5conved.hdf5'
origResave = '/seagate2t/simon/kawaii/data/h5orig.hdf5'
rirPath = '/seagate2t/simon/kawaii/data/rir.hdf5'

filePathes = glob.glob(filePath+'/**/*.wav', recursive=True)

rirSet = h5py.File(rirPath, 'r')
saveFile = h5py.File(savePath, 'w', libver='latest')
origFile = h5py.File(origResave, 'w', libver='latest')

rirKey = list(rirSet.keys())
print('+{0:->15}+{1:-<30}+'.format('-', '-'))
for room in rirKey:
    print('|{0:>15}|{1:<30}|'.format('room', room))
    rir = rirSet[room]
    conv1 = rir[:,0]
    conv2 = rir[:,1]
    mic1 = np.asarray([float(t) for t in rir.attrs['mic1(m)'].split()])
    mic2 = np.asarray([float(t) for t in rir.attrs['mic2(m)'].split()])
    source = np.asarray([float(t) for t in rir.attrs['source_p(m)'].split()])
    roomSize = np.asarray([float(t) for t in rir.attrs['L(m)'].split()])
    volume = reduce(lambda x, y: x*y, roomSize)
    vector1 = mic1 - (mic1+mic2)/2
    vector2 = source - (mic1+mic2)/2
    angle = np.arccos(np.clip(np.dot(vector1, vector2), -1.0, 1.0))
    distance = reduce(lambda x, y: hypot(x, y), source - (mic1 + mic2)/2)
    curRoom = saveFile.create_group(str(roomSize))
    print('|{0:>15}|{1:<30.2f}|'.format('volume', volume))
    print('|{0:>15}|{1:<30.2f}|'.format('angle', angle))
    print('|{0:>15}|{1:<30.2f}|'.format('distance', distance))
    print('+{0:->15}+{1:-<30}+'.format('-', '-'))
    for wavPath in filePathes:
        head, fileName = os.path.split(wavPath)
        print('|{0:>15}|{1:<30}|'.format('file name', fileName))
        clean, sr = sf.read(wavPath)
        magWave = sum([abs(p) for p in clean])/len(clean)
        t = time.time()
        print('|{0:>15}|{1:<30}|'.format('conv>', 'start'))
        fakeMic1 = np.convolve(conv1, clean)
        fakeMic2 = np.convolve(conv2, clean)
        t = time.time() - t
        print('|{0:>15}|{1:<30.2f}|'.format('conv<', t))
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
            print('|{0:>15}|{1:<30}|'.format('orig hdf5', fileName))
            print('+{0:->15}+{1:-<30}+'.format('-', '-'))
        curDset = curRoom.create_dataset(fileName, data=stereo)
        curDset.attrs.create('mono', fileName, dtype=h5py.special_dtype(vlen=str))
        curDset.attrs.create('volume', volume, dtype=float)
        curDset.attrs.create('angle', angle, dtype=float)
        curDset.attrs.create('distance', distance, dtype=float)
        print('|{0:>15}|{1:<30}|'.format('conv hdf5', 'finished'))
        print('+{0:->15}+{1:-<30}+'.format('-', '-'))
saveFile.swmr_mode = True
origFile.swmr_mode = True
saveFile.flush()
saveFile.close()
origFile.flush()
origFile.close()


    
