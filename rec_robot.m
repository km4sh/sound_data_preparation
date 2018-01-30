clear;
fileList = dir(fullfile('.\','*.wav'));
for i = 1:length(fileList)
    disp(strcat(fileList(i).name,' recording starts at'));
    disp(fix(clock));
    recording_single(strcat('.\',fileList(i).name), strcat('rec_file\rec_',fileList(i).name));
    disp(strcat(fileList(i).name,' recording ended at'));
    disp(fix(clock));
end

