import os
import re
from shutil import copyfile

workSpace = '/seagate2t/rec_jan12/exp1grp1'
savePath = '/seagate2t/rec_jan12/'
origPath = '/seagate2t/rec_jan12/orig'
copyPath = '/seagate2t/rec_jan12/exp1'

if not os.path.exists(os.path.join(savePath, 'mono')):
    os.makedirs(os.path.join(savePath, 'mono'))
if not os.path.exists(os.path.join(savePath, 'stereo')):
    os.makedirs(os.path.join(savePath, 'stereo'))

for dirPath, dirNames, fileNames in os.walk(workSpace):
    rooms = list(set([re.sub('_.*', '', d) for d in dirNames]))
    for dirName in dirNames:
        room = re.sub('_.*', '', dirName)
        for root, dirs, files in os.walk(os.path.join(workSpace, dirName)):
            files = set([re.sub('_.{4}[0-9].wav', '', f) for f in files])
            for f in files:
                print(f)
                copyfile(os.path.join(savePath, 'exp1', room, str(rooms.index(room))+'_'+f+'.wav'), os.path.join(copyPath, 'mono', str(rooms.index(room))+'_'+f+'.wav'))
                copyfile(os.path.join(origPath, f+'.wav'), os.path.join(copyPath, 'stereo', str(rooms.index(room))+'_'+f+'.wav'))


