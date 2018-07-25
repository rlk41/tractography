
from os import listdir
from os.path import join, split, isfile, basename

mainDir   = '/media/richard/camcan/Projects/SpeechTBT/data.11mrtrix'
subs = [ f for f in listdir(mainDir) if 'MR' in f ]
#sub = subs[6]

sub = 'MR1103'


for sub in subs:
    mainDir     = '/media/richard/camcan/Projects/SpeechTBT/data.11mrtrix'
    subPath     = join('/media/richard/camcan/Projects/SpeechTBT/data.11mrtrix',sub)

    locROI_Dir  = join(subPath, 'tmaps', 'raw')
    roiPaths    = [join(locROI_Dir, f) for f in listdir(locROI_Dir) if isfile(join(locROI_Dir, f)) if 'MNI' not in f and 'nii' in f]

    # r = roiPaths[0]
    for r in roiPaths:

        try:
            targFile    = join(subPath, 'mri','brain.nii.gz')
            movFile     = r
            outName     = basename(r).replace('.nii','.MNI152_T1_1mm_brain2brain.nii.gz')
            o           = join(subPath, 'tmaps', outName)
            masterFile  = join(subPath, 'mri', 'brain.nii.gz')
            reg         = join(subPath, 'reg', 'MNI152_T1_1mm_brain2brain.mat.aff12.1D')
            head, tail  = split(o)


            applyReg(subPath, movFile, targFile, masterFile, o, reg)


        except:
            print("failed: {}".format(movFile))
            continue