import os
import re
import soundfile as sf
import numpy as np

workSpace = '/seagate2t/rec_jan12/exp1grp1'
savePath = '/seagate2t/rec_jan12/'
os.chdir(workSpace)

for dirPath, dirNames, fileNames in os.walk(workSpace):
    for dirName in dirNames:
        room = re.sub('_.*', '', dirName)
        if not os.path.exists(os.path.join(savePath, 'exp1', room)):
            os.makedirs(os.path.join(savePath, 'exp1', room))
        for root, dirs, files in os.walk(dirName):
            files = set([re.sub('_.{4}[0-9].wav', '', f) for f in files])
            for f in files:
                ch1, sr = sf.read(os.path.join(workSpace, dirName, f+'_conv1.wav'))
                ch2, sr = sf.read(os.path.join(workSpace, dirName, f+'_conv2.wav'))
                stereo = np.vstack((ch1,ch2)).T
                sf.write(os.path.join(savePath, 'exp1', room, f+'.wav'), stereo, sr)
                print('#',os.path.join(savePath, 'exp1', room, f+'.wav'), 'written.')
                del ch1, ch2, stereo
