import os
import re
import h5py
import soundfile as sf
import numpy as np
from functools import reduce

stereoPath = '/seagate2t/simon/kawaii/data/stereo'
monoPath = '/seagate2t/simon/kawaii/data/mono'
os.chdir('/seagate2t/simon/kawaii/Beamforming-Net/')

def prepareData(monoPath=monoPath, stereoPath=stereoPath):
    mono = h5py.File('mono.hdf5', 'w', libver='latest')
    stereo = h5py.File('stereo.hdf5', 'w', libver='latest')
    print('# hdf5 files were created.')
    for root, dirs, files in os.walk(monoPath):
        for wav in files:
            soundwave, sr = sf.read(os.path.join(monoPath, wav))
            assert sr == 16000
            curDset = mono.create_dataset(wav, data=soundwave)
            print('# mono dataset %s created.' % curDset.name)
    for root, rooms, files in os.walk(stereoPath):
        [print('# one of the rooms looks like: ', r) for r in rooms]
        for room in rooms:
            curRoom = stereo.create_group(room)
            print('# group %s was created.' % curRoom.name)
            size = [float(s) for s in re.findall('[^,,]+', room)]
            length, width, height = size
            volume = reduce(lambda x, y: x*y, size)
            for subroot, subdirs, subfiles in os.walk(os.path.join(stereoPath, room)):
                for f in subfiles:
                    print('\n#####################################################################################################')
                    print('# now working on %s.' % f)
                    soundwave, sr = sf.read(os.path.join(stereoPath, room, f))
                    assert sr == 16000
                    monoName = f
                    print('# anechonic file name generated: %s' % monoName)
                    if not len(soundwave) == mono[monoName].shape[0]:
                        print('# warning: wave length error')
                        print('# stereo:', len(soundwave), 'mono', mono[monoName].shape[0])
                        if len(soundwave) < mono[monoName].shape[0]:
                            soundwave = np.append(soundwave, np.zeros(mono[monoName].shape[0]-len(soundwave)))
                            curDset = curRoom.create_dataset(f, data=soundwave)
                            print('# warning: stereo was appended w/ zeros.')
                        else:
                            soundwave = soundwave[0:mono[monoName].shape[0]]
                            curDset = curName.create_dataset(f, data=soundwave)
                            print('# warning: stereo was cutted as same as mono. but, is that really right?')
                            print('# warning: really? you mean it?')
                    else:
                        curDset = curRoom.create_dataset(f, data=soundwave)
                    print('# file:', f, '\tsize:', length, width, height, '\tanechonic file: ', monoName)
                    curDset.attrs.create('length', length, dtype=float)
                    curDset.attrs.create('width', width, dtype=float)
                    curDset.attrs.create('height', height, dtype=float)
                    curDset.attrs.create('volume', volume, dtype=float)
                    curDset.attrs.create('mono', monoName, dtype=h5py.special_dtype(vlen=str))
                    assert curRoom[f].shape[0] == mono[curRoom[f].attrs['mono']].shape[0]
                    print('# stereo dataset %s created.' % curDset.name)
    stereo.swmr_mode = True
    mono.swmr_mode = True
    stereo.flush()
    stereo.close()
    mono.flush()
    mono.close()

if __name__ == '__main__':
    prepareData()
