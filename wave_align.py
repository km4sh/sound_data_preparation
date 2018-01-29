import os
import numpy as np
import soundfile as sf
from scipy import fftpack, signal
from channeldelay import wavedelay

os.chdir('/home/simon/Music/rec_jan25/')
pdata = []
count = 1
filenames = [f for f in os.listdir('.') if os.path.isfile(f)]
for filename in [f for f in filenames if f.endswith(".wav")]:
    oriWave, oriSampleRate = sf.read(os.path.join('.', filename))
    print('fileopened:', os.path.join('.',filename))
    recWave, recSampleRate = sf.read(os.path.join('.', 'rec_file/rec_'+filename))
    print('fileopened:', os.path.join('.', 'rec_file/rec_'+filename))
    delay = wavedelay(oriWave, recWave, oriSampleRate, 60)
    recWave = recWave[delay:]
    oriWave = oriWave[:len(recWave)]
    sf.write('aligned_'+filename, oriWave, oriSampleRate)
    sf.write('aligned_rec_'+filename, recWave, recSampleRate)
    print('aligning complete! file:', filename)

