import os
import re
import soundfile as sf
import numpy as np


monoPath = '/seagate2t/rec_jan12/orig'
stereoPath = '/seagate2t/rec_jan12/exp1'
savePath = '/seagate2t/simon/kawaii/data'

if not os.path.exists(os.path.join(savePath, 'stereo')):
    os.makedirs(os.path.join(savePath, 'stereo'))
if not os.path.exists(os.path.join(savePath, 'mono')):
    os.makedirs(os.path.join(savePath, 'mono'))

for root, rooms, files in os.walk(stereoPath):
    for room in rooms:
        print('# one of the rooms looks like: ', room)
        if not os.path.exists(os.path.join(savePath, 'stereo', room)):
            os.makedirs(os.path.join(savePath, 'stereo', room))
        for subroot, subdirs, subfiles in os.walk(os.path.join(stereoPath, room)):
            for f in subfiles:
                print('####################################################')
                print('# now working on %s.' % f)
                soundwave, sr = sf.read(os.path.join(stereoPath, room, f))
                assert sr == 16000
                monoName = re.sub('.*_', 'combined_', f)
                print('# anechonic file name generated: %s' % monoName)
                monoWave, sr = sf.read(os.path.join(monoPath, monoName))
                assert sr == 16000
                if not len(soundwave) == len(monoWave):
                    print('# warning: wave length error')
                    print('# stereo:', len(soundwave), 'mono', len(monoWave))
                    if len(soundwave) < len(monoWave):
                        soundwave = np.append(soundwave, np.zeros(len(monoWave)-len(soundwave)))
                        print('# warning: stereo was appended w/ zeros.')
                    else:
                        monoWave = np.append(monoWave, np.zeros(len(soundwave)-len(monoWave)))
                        print('# warning: mono was appended w/ zeros.')
                assert len(soundwave) == len(monoWave)
                sf.write(os.path.join(savePath, 'mono', monoName), monoWave, sr)
                sf.write(os.path.join(savePath, 'stereo', room, monoName), soundwave, sr)
