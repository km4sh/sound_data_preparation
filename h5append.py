import os
import re
import h5py
import soundfile as sf
import numpy as np
from functools import reduce

file1 = '/seagate2t/simon/kawaii/data/fix_conv.hdf5'
file2 = '/seagate2t/simon/kawaii/data/rec_f1.hdf5'
savePath = '/seagate2t/simon/kawaii/data/fix_rec.hdf5'
def appendFile(monoPath=monoPath, f1Path=f1Path):
    f1 = h5py.File(file1, 'r', libver='latest')
    f2 = h5py.File(file2, 'r', libver='latest')

    f1.swmr_mode = True
    f2.swmr_mode = True
    f1.flush()
    f1.close()
    f2.flush()
    f2.close()

if __name__ == '__main__':
    appendFile()
