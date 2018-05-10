import os
import re
import h5py
import soundfile as sf
import numpy as np

stereoPath = '/seagate2t/rec_jan12/room/'
monoPath = '/seagate2t/rec_jan12/orig/'

os.chdir('/seagate2t/rec_jan12/')


def prepareData(monoPath=monoPath, stereoPath=stereoPath):
    mono = h5py.File('abc.hdf5', 'w', libver='latest')
    stereo = h5py.File('def.hdf5', 'w', libver='latest')

    for root, dirs, files in os.walk(monoPath):
        for wav in files:
            soundwave, sr = sf.read(os.path.join(monoPath, wav))
            assert sr == 16000
            curdset = mono.create_dataset(wav, data=soundwave)
    for root, dirs, files in os.walk(stereoPath):
        for wav in files:
            soundwave, sr = sf.read(os.path.join(stereoPath, wav))
            assert sr == 16000
            curdset = stereo.create_dataset(wav, data=soundwave)
            volume = re.findall('[0-9]{2,3}', wav)
            monoName = re.sub('[0-9]{2,3}', 'combined', wav)
            print('#', wav, volume, monoName)
            curdset.attrs.create('volume', int(volume[0]), dtype=int)
            curdset.attrs.create('mono', monoName, dtype=h5py.special_dtype(vlen=str))
            try:
                assert stereo[wav].shape[0] == mono[stereo[wav].attrs['mono']].shape[0]
            except:
                print(stereo[wav].shape[0], mono[stereo[wav].attrs['mono']].shape[0])
                exit()
    stereo.swmr_mode = True
    mono.swmr_mode = True
    stereo.flush()
    stereo.close()
    mono.flush()
    mono.close()
if __name__ == '__main__':
    prepareData()
