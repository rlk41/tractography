import os
from os.path import join, split

def resample_3dallineate(input, master, output):
    t = Template('3dAllineate -input $_input -master $_master '
                 '-prefix $_output -final wsinc5 -1Dparam_apply "1D: 12@0" ')
    c=t.substitute(_input=input, _master=master, _output=output)
    return run_command(c)

dir = '/home/richard/Desktop/Untitled_Folder'

mask1 = '1153_test_bet_raimage_35_thresh.nii'
mask2 = 'brainmask.T1.nii'

subPath = '/media/richard/camcan/Projects/SpeechTBT/data.11mrtrix/MR1153'
mov = join(dir,'fmri.resampled.brainmask.nii')
targ = join(dir,'brainmask.T1.nii')
o = join(dir,'fmri.resampled.brainmask_to_brainmask.T1.nii')
reg = join(dir, 'fMRI2T1.aff12.1D')


createReg(subPath,mov, targ, o, reg)

mov = join(dir,'fmri.nii')
o = join(dir,'fmri.T1.nii')

applyReg(subPath, mov, targ, targ, o, reg, Inv=False, warp='srs', thr=False, bin=False, final=False, overwrite=True)


input = join(dir, 'fmri.nii')
output = join(dir, 'fmri.resampled.nii')
master= join(dir, mask2)
resample_3dallineate(input, master, output)



'/home/richard/Desktop/Untitled_Folder/fmri.nii' '/home/richard/Desktop/Untitled_Folder/fmri.resampled.nii'



3dAllineate -input fmri.nii -master brainmask.T1.nii -prefix fmri.T1.nii -final wsinc5 -1Dparam_apply '1D: 12@0'\'