import soundfile as sf

ori, srOri = sf.read('/seagate2t/rec_jan12/2.8_2.8_2.3+2.8_2.9_2.3/combined_timit1_conv2.wav')
ori = ori[1:30*srOri]
fake, srFake = sf.read('/seagate2t/rec_jan12/combined_timit1.wav')
fake = ori[1:30*srFake]
sf.write('/seagate2t/rec_jan12/orig.wav', ori, srOri)
sf.write('/seagate2t/rec_jan12/fake.wav', fake, srFake)

