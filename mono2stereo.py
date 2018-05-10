import os
import re
import soundfile as sf
import numpy as np
from shutil import copyfile

workSpace = '/seagate2t/rec_jan12/exp1grp1'
savePath = '/seagate2t/rec_jan12/'
origPath = '/seagate2t/rec_jan12/orig'
copyPath = '/seagate2t/rec_jan12/exp1'

if not os.path.exists(os.path.join(copyPath, 'mono')):
    os.makedirs(os.path.join(copyPath, 'mono'))
if not os.path.exists(os.path.join(copyPath, 'stereo')):
    os.makedirs(os.path.join(copyPath, 'stereo'))

for dirPath, dirNames, fileNames in os.walk(workSpace):
    rooms = list(set([re.sub('_.*', '', d) for d in dirNames]))
    for dirName in dirNames:
        room = re.sub('_.*', '', dirName)
        if not os.path.exists(os.path.join(savePath, 'exp1', room)):
            os.makedirs(os.path.join(savePath, 'exp1', room))
        for root, dirs, files in os.walk(os.path.join(workSpace, dirName)):
            print(root, dirName)
            files = set([re.sub('_.{4}[0-9].wav', '', f) for f in files])
            for f in files:
                ch1, sr = sf.read(os.path.join(workSpace, dirName, f+'_conv1.wav'))
                ch2, sr = sf.read(os.path.join(workSpace, dirName, f+'_conv2.wav'))
                stereo = np.vstack((ch1,ch2)).T
                sf.write(os.path.join(savePath, 'exp1', room, str(rooms.index(room))+'_'+f+'.wav'), stereo, sr)
                print('#',os.path.join(savePath, 'exp1', room, str(rooms.index(room))+'_'+f+'.wav'), 'written.')
                copyfile(os.path.join(savePath, 'exp1', room, str(rooms.index(room))+'_'+f+'.wav'), os.path.join(copyPath, 'stereo', str(rooms.index(room))+'_'+f+'.wav'))
                copyfile(os.path.join(origPath, f+'.wav'), os.path.join(copyPath, 'mono', str(rooms.index(room))+'_'+f+'.wav'))
                print('#',os.path.join(savePath, 'exp1', room, str(rooms.index(room))+'_'+f+'.wav'), 'copied to mono and stereo folders.')
                del ch1, ch2, stereo
