fsl_path = '/usr/share/fsl/5.0/';
setenv('FSLDIR',fsl_path)
setenv('FSLOUTPUTTYPE','NIFTI_GZ') %NIFTI_GZ
curpath = getenv('PATH');
setenv('PATH',sprintf('%s:%s',fullfile(fsl_path,'bin'),curpath));


fileName = '/media/richard/camcan/Projects/SpeechTBT/freesurfer/MR1106/probtrackx_commands.txt';
%fileID = fopen(fileName); 
lines = dataread('file', fileName, '%s', 'delimiter','\n'); 

N = 30; 
myCluster=parcluster('local'); 
myCluster.NumWorkers=N; 
parpool(myCluster,N)


parfor i = 1:length(lines)
    system(lines{i}); 
end 

