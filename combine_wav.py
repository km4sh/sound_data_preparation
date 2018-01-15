import os
import soundfile as sf
import numpy as np

os.chdir('/home/simon/Music/dataset')

data = []
duration = 0
count = 1
for dirPath, dirNames, fileNames in os.walk("."):
    for fileName in [f for f in fileNames if f.endswith(".wav")]:
        curWave, sampleRate = sf.read(os.path.join(dirPath, fileName))
        duration += len(curWave)/sampleRate
        print('combined file: ', os.path.join(dirPath, fileName, '\t\t total time:', str(duration)))
        data.extend(curWave)
    if(duration > 3600):
        print('WAVE', count, 'COMBINED COMPLETE')
        sf.write('combined_timit'+str(count)+'.wav', data, sampleRate)
        count += 1
        data = []
        duration = 0
        print('combined_timit'+str(count)+'.wav'+'writed ##')
print('WAVE', count, 'COMBINED COMPLETE')
sf.write('combined_timit'+str(count)+'.wav', data, sampleRate)
print('combined_timit'+str(count)+'.wav'+'writed ##')
