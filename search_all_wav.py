import os

os.chdir('/home/simon/Music/dataset')

for dirpath, dirnames, filenames in os.walk("."):
    for filename in [f for f in filenames if f.endswith(".wav")]:
        print (os.path.join(dirpath, filename))
