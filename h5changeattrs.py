import os
import h5py
import glob
import time
import numpy as np
import soundfile as sf
from functools import reduce
from math import hypot

savePath = '/seagate2t/simon/kawaii/data/fix/fix_final.hdf5'
rirPath = '/seagate2t/simon/kawaii/data/multi_sources/ms_rir.h5'

rirSet = h5py.File(rirPath, 'r')
saveFile = h5py.File(savePath, 'a', libver='latest', swmr=True)

print('+{0:->15}+{1:-<30}+'.format('-', '-'))

for room in list(rirSet.keys()):
    try:
        print('|{0:>15}|{1:<30}|'.format('room', room))
        rir = rirSet[room]['source1']
        noiseRir = rirSet[room]['source4']
        mic1 = np.asarray([float(t) for t in rir.attrs['mp1'].split()])
        mic2 = np.asarray([float(t) for t in rir.attrs['mp2'].split()])
        source = np.asarray([float(t) for t in rir.attrs['sp'].split()])
        roomSize = np.asarray([float(t) for t in rir.attrs['roomsize'].split()])
        noisePos = np.asarray([float(t) for t in noiseRir.attrs['sp'].split()])
        noiseAngle = np.arccos(np.clip(np.dot(mic2 - mic1, noisePos - mic1), -1.0, 1.0)) * 360 / (2 * np.pi)
        print('+{0:->15}+{1:-<30}+'.format('-', '-'))
        curRoom = saveFile[str(roomSize)]
        for dSet in list(curRoom.keys()):
            curDset = curRoom[dSet]
            try:
                del curDset.attrs['mp1']
                del curDset.attrs['mp2']
                del curDset.attrs['sp']
                del curDset.attrs['roomsize']
                del curDset.attrs['noise angle']
                print('|{0:>15}|{1:<30}|'.format('some attrs', ' deleted'))
            except:
                pass
            curDset.attrs.create('mp1', rir.attrs['mp1'], dtype=h5py.special_dtype(vlen=str))
            curDset.attrs.create('mp2', rir.attrs['mp2'], dtype=h5py.special_dtype(vlen=str))
            curDset.attrs.create('sp', rir.attrs['sp'], dtype=h5py.special_dtype(vlen=str))
            curDset.attrs.create('roomsize', rir.attrs['roomsize'], dtype=h5py.special_dtype(vlen=str))
            curDset.attrs.create('noise angle', noiseAngle, dtype=float)
            print('|{0:>15}|{1:<30}|'.format('some attrs', ' rebuilded'))
            print('+{0:->15}+{1:-<30}+'.format('-', '-'))
    except:
        break
saveFile.swmr_mode = True
saveFile.flush()
saveFile.close()
print('+{0:->15}-{1:-<30}+'.format(' all ', ' finished '))
