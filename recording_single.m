function recording_single(filename)
    audioFrameLength = 1024;
    fWave = dsp.AudioFileReader(filename,'SamplesPerFrame',audioFrameLength);
    fPlayer  = dsp.AudioPlayer('DeviceName','3-4 (OCTA-CAPTURE)','SampleRate', fs);
    audioRec = dsp.AudioRecorder(...
        'DeviceName', ...
        '1-2 (OCTA-CAPTURE)',...
        'SampleRate', fs, ...
        'NumChannels', 2,...
        'OutputDataType','double',...
        'QueueDuration', 2,...
        'SamplesPerFrame', audioFrameLength);
    fWriter = dsp.AudioFileWriter(...
        '.\data\test-MicroArrayData.wav',...
        'FileFormat','wav',...
        'SampleRate',fs);
    while (~isDone(fWave))
        fPlayer(fWave);
    end
    release(fWave);
    release(fPlayer);
    release(audioRec);
    release(fWriter);
    disp('Recording complete');
end