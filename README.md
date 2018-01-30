# sound_data_preparation tools
sound_data_preparation for recording.
**under construction...**
## file list
- channel_correlation.py

  calculate the correlation between a mono signal and a recored stereo signal. you may extend the number of channel as you want,but notice the relationship of the two channel you wanna calculate.
- channeldelay.py
  
  just like the `channel_correlation.py` above, but has defined some functions you can use outside.
- combine_wav.py
  
  combine mini wav file into a big wav file(1 hour as default.).
  *it will search all *.wav file in the folder mentioned. but not recursively*
- rec_robot.m
  
  a robot can put next wav file in the folder into `recording_single.m` to record that. output file is associate with the original file and saved in a subfold named `rec_file`. 
- recording_single.m

  a function which is able to play a original wav file in and record from a USB soundcard. it is written as **Roland OCTA-CAPTURE**. well, if you have set your sound device as default in your system, you can still just delete the `device name` configuration.
- search_all_wav.py
  
  just a subfunction of `wave_align.py` and `combine_wav.py`. i was writting that for a test.
- wave_align.py

  call some `channeldelay.py` functions and align the input mono and stereo waveforms.
- wave_check.py

  call some `channeldelay.py` functions and output the correlations.
