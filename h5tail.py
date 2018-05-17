import os
import h5py

savePath = '/seagate2t/simon/kawaii/data/may14conv_all.hdf5'
origResave = '/seagate2t/simon/kawaii/data/may14orig_all.hdf5'

saveFile = h5py.File(savePath, 'w', libver='latest')
origFile = h5py.File(origResave, 'w', libver='latest')

saveFile.swmr_mode = True
origFile.swmr_mode = True
saveFile.flush()
saveFile.close()
origFile.flush()
origFile.close()
