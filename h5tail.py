import os
import h5py

savePath = '/seagate2t/simon/kawaii/data/fix_conv.hdf5'

saveFile = h5py.File(savePath, 'w', libver='latest')
rooms = list(saveFile.keys())
for room in rooms:
    curGrp = saveFile[room]
    if(list(curGrp.keys()) == []):
        del curGrp
        print('room deleted:', room)
saveFile.swmr_mode = True
saveFile.flush()
saveFile.close()

