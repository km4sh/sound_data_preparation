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
saveFile = h5py.File(savePath, 'a', libver='latest')
origFile = h5py.File(origResave, 'a', libver='latest')

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
    angle = (np.arccos(np.clip(np.dot(vector1, vector2), -1.0, 1.0)) / (2 * np.pi)) * 360
    distance = reduce(lambda x, y: hypot(x, y), source - (mic1 + mic2)/2)
    curRoom = saveFile[str(roomSize)]
    print('|{0:>15}|{1:<30.2f}|'.format('volume', volume))
    print('|{0:>15}|{1:<30.2f}|'.format('angle', angle))
    print('|{0:>15}|{1:<30.2f}|'.format('distance', distance))
    print('+{0:->15}+{1:-<30}+'.format('-', '-'))
    for wavPath in filePathes:
        head, fileName = os.path.split(wavPath)
        print('|{0:>15}|{1:<30}|'.format('file name', fileName))
        print('+{0:->15}+{1:-<30}+'.format('-', '-'))
        assert volume == curRoom[fileName].attrs['volume']
        assert fileName == curRoom[fileName].attrs['mono']
        assert distance == curRoom[fileName].attrs['distance']
        print('|{0:>15}|{1:<30.2f}|'.format('orig angle', curRoom[fileName].attrs['angle']))
        curRoom[fileName].attrs['angle'] = angle
        print('|{0:>15}|{1:<30.2f}|'.format('modi angle', curRoom[fileName].attrs['angle']))
        print('+{0:->15}+{1:-<30}+'.format('-', '-'))
saveFile.swmr_mode = True
origFile.swmr_mode = True
saveFile.flush()
saveFile.close()
origFile.flush()
origFile.close()


    
