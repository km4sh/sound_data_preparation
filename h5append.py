import h5py
import random
import string

file1 = '/seagate2t/simon/kawaii/data/fix/fix_noise_n10snr.hdf5'
file2 = '/seagate2t/simon/kawaii/data/fix/fix_noise2.hdf5'
savePath = '/seagate2t/simon/kawaii/data/fix_append.hdf5'
def appendFile(file1=file1, file2=file2, savePath=savePath):
    f1 = h5py.File(file1, 'r', libver='latest')
    f2 = h5py.File(file2, 'r', libver='latest')
    saveF = h5py.File(savePath, 'a', libver='latest')
    f1grp = list(f1.keys())
    f2grp = list(f2.keys())
    print('> file 1 opened.')
    for grp in f1grp:
        origGrp = f1[grp]
        print('> file 1 '+grp+' opened')
        try:
            curGrp = saveF[grp]
        except:
            curGrp = saveF.create_group(grp)
        for dSet in list(origGrp.keys()):
            origDset = origGrp[dSet]
            salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            curDset = curGrp.create_dataset(salt, data=origDset)
            curDset.attrs.create('mono', origDset.attrs['mono'], dtype=h5py.special_dtype(vlen=str))
            curDset.attrs.create('volume', origDset.attrs['volume'], dtype=float)
            curDset.attrs.create('angle', origDset.attrs['angle'], dtype=float)
            curDset.attrs.create('distance', origDset.attrs['distance'], dtype=float)
            print('> file 1 '+grp+' '+dSet+' appened as', salt)
    print('> file 2 opened.')
    for grp in f2grp:
        origGrp = f2[grp]
        print('> file 2 '+grp+' opened')
        try:
            curGrp = saveF[grp]
        except:
            curGrp = saveF.create_group(grp)
        for dSet in list(origGrp.keys()):
            origDset = origGrp[dSet]
            salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            curDset = curGrp.create_dataset(salt, data=origDset)
            curDset.attrs.create('mono', origDset.attrs['mono'], dtype=h5py.special_dtype(vlen=str))
            curDset.attrs.create('volume', origDset.attrs['volume'], dtype=float)
            curDset.attrs.create('angle', origDset.attrs['angle'], dtype=float)
            curDset.attrs.create('distance', origDset.attrs['distance'], dtype=float)
            print('> file 2 '+grp+' '+dSet+' appened as', salt)
    saveF.swmr_mode = True
    saveF.flush()
    saveF.close()
    f1.close()
    f2.close()
    print('> files appending finished')
if __name__ == '__main__':
    appendFile()
