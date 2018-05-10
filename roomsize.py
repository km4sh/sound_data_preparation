import os
import re
from shutil import copyfile
from functools import reduce

origPath = '/seagate2t/rec_jan12/exp1'
savePath = '/seagate2t/rec_jan12/room'

if not os.path.exists(savePath):
    os.makedirs(savePath)

for root, rooms, files in os.walk(origPath):
    print(rooms)
    for room in rooms:
        print(room)
        size = [float(s) for s in re.findall('[^,,]+', room)]
        volume = reduce(lambda x, y: x*y, size)
        for subroot, subdirs, subfiles in os.walk(os.path.join(origPath,room)):
            print(subfiles)
            for f in subfiles:
                fRe = re.sub('.*_',str(int(volume))+'_',f)
                #print(f, 'will be replaced by', fRe)
                os.rename(os.path.join(subroot, f), os.path.join(subroot, fRe))
                copyfile(os.path.join(subroot, fRe), os.path.join(savePath, fRe))

