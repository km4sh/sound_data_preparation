import os
import h5py
import glob
import re
import soundfile as sf

stereoPath = '/seagate2t/rec/stereo'
monoPath = '/seagate2t/rec/mono'
h5StereoPath = '/seagate2t/simon/kawaii/data/rec_stereo.hdf5'
h5MonoPath = '/seagate2t/simon/kawaii/data/rec_mono.hdf5'

monoFiles = glob.glob(monoPath+'/**/*.wav', recursive=True)
stereoFiles = glob.glob(stereoPath+'/**/*.wav', recursive=True)


mF = h5py.File(h5MonoPath, 'w', libver='latest')
sF = h5py.File(h5StereoPath, 'w', libver='latest')
t706 = sF.create_group('room:T706')

print('+{0:->15}+{1:-<50}+'.format('-', '-'))
for monoFile in monoFiles:
    mono, sr = sf.read(monoFile)
    head, monoFile = os.path.split(monoFile)
    curDset = mF.create_dataset(monoFile, data=mono)
    print('|{0:^15}|{1:^50}|'.format('mono', monoFile))
for stereoFile in stereoFiles:
    stereo, sr = sf.read(stereoFile)
    head, stereoFile = os.path.split(stereoFile)
    curDset = t706.create_dataset(stereoFile, data=stereo)
    monoName = re.sub(r'rec_','',stereoFile)
    curDset.attrs.create('mono', monoName, dtype=h5py.special_dtype(vlen=str))
    curDset.attrs.create('volume', 100, dtype=float)
    curDset.attrs.create('angle', 30., dtype=float)
    curDset.attrs.create('distance', 2.7, dtype=float)
    print('|{0:^15}|{1:^50}|'.format('stereo', stereoFile))
    print('|{0:^15}|{1:^50}|'.format('monoName', monoName))
sF.swmr_mode = True
mF.swmr_mode = True
sF.flush()
sF.close()
mF.flush()
mF.close()
print('+{0:->15}+{1:-<50}+'.format('-', '-'))

