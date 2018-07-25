

from nibabel.nifti1 import load as loadnii
from nibabel.freesurfer.mghformat import load as loadmgz
import csv
import os
from os import listdir, chdir
from os.path import join, isfile, basename, split
from string import Template
mainDir = '/media/richard/camcan/bin/hcp-tractography/mrtrix3-python'
mrtrixBin ='/usr/local/mrtrix3/bin'
afniBin='/usr/lib/afni/bin'
fslBin='/usr/share/fsl/5.0/bin/'

#sys.path.append(mainDir)
#sys.path.append(mrtrixBin)
#sys.path.append(afniBin)

os.environ['PATH'] = os.environ['PATH'] + ':' + afniBin
os.environ['PATH'] = os.environ['PATH'] + ':' + mrtrixBin
os.environ['PATH'] = os.environ['PATH'] + ':' + mainDir
os.environ['PATH'] = os.environ['PATH'] + ':' + mainDir + '/bin'
os.environ['PATH'] = os.environ['PATH'] + ':' + fslBin


os.chdir(mainDir)

# from warpLoc import warp
from nodeParc import mrtrixLUTParc, assignStreamlines, gmFix, nii2mif, dumpNifti, nodeParc2,\
    createReg, applyReg
# from intersectROI import
# from prepareParcellation import
from genConnectome import getConnMat, reduceConn


##TODO
#  dt_recon
#  trac-all
#

#align_epi_anat.py -anat mri/norm.nii.gz -epi diffusion/nodif_brain.nii.gz -epi_base 0 -suffix _al2dti -giant_move -epi_strip 3dAutomask -epi2anat -tshift off -volreg_method 3dAllineate
#align_epi_anat.py -anat mri/norm.nii.gz -epi diffusion/nodif_brain.nii.gz -suffix _al2dti -giant_move -epi2anat -tshift off -volreg_method 3dAllineate

#####   nodeParcellation

mainDir   = '/media/richard/camcan/Projects/SpeechTBT/data.11mrtrix'
subs = [ f for f in listdir(mainDir) if 'MR' in f ]
#sub = subs[6]

### Transform nodif_brain to DTI-space

for sub in subs:
    #register

    subPath=join('/media/richard/camcan/Projects/SpeechTBT/data.11mrtrix',sub)
    #b0='diffusion/nodif.nii.gz'
    #reg='reg/nodif2brain.reg'
    #bbregDTI(subPath, b0, reg)

    # targFile    =join(subPath, 'mri',       'norm.nii.gz')
    # movFile     =join(subPath, 'diffusion', 'nodif_brain.nii.gz')
    # o           =join(subPath, 'reg',       'nodif_brain2norm.nii.gz')
    # reg         =join(subPath, 'reg',       'nodif_brain2norm.aff12.1D')
    #
    # createReg(subPath, movFile, targFile, o, reg)
    #
    # targFile    =join(subPath, 'mri',       'norm.nii.gz')
    # movFile     =join(subPath, 'diffusion', 'data.nii.gz')
    # reg         =join(subPath, 'reg',       'nodif_brain2norm.aff12.1D')
    # o           =join(subPath, 'diffusion', 'data.norm.nii.gz')
    # applyReg(subPath, movFile, targFile, o, reg, warp='srs') #Inv=True
    #
    #
    # targFile    =join(subPath, 'mri',       'norm.nii.gz')
    # movFile     =join(subPath, 'diffusion', 'no.nii.gz')
    # reg         =join(subPath, 'reg',       'nodif_brain2norm.aff12.1D')
    # o           =join(subPath, 'diffusion', 'data.norm.nii.gz')
    # applyReg(subPath, movFile, targFile, o, reg, warp='srs') #Inv=True

    targFile    =join(subPath, 'diffusion', 'nodif_brain.nii.gz')
    movFile     =join(subPath, 'mri',       'norm.nii.gz')
    o           =join(subPath, 'mri',       'norm.nodif_brain.nii.gz')
    masterFile  = movFile
    #reg         =join(subPath, 'reg',       'nodif_brain2norm.aff12.1D')
    #applyReg(subPath, movFile, targFile, o, reg, warp='srs', Inv=True)

    # fix INV!!!!
    reg         =join(subPath, 'reg',       'norm2nodif_brain.aff12.1D')
    applyReg(subPath, movFile, targFile, masterFile, o, reg, warp='srs')

## Transform ROIs to DTI-space
# sub = subs[1]
for sub in subs:

    subPath     =join('/media/richard/camcan/Projects/SpeechTBT/data.11mrtrix',sub)


    locROI_Dir              =join(mainDir, sub, 'mask.localizer.MNI.MNI152_T1_1mm_brain2brain')
    locROI_Paths            =[join(locROI_Dir, f) for f in listdir(locROI_Dir) if isfile(join(locROI_Dir, f))]

    # r = locROI_Paths[0]
    for r in locROI_Paths:


        oName = basename(r).replace('.nii.gz','.norm2nodif.nii.gz')
        targFile    = join(subPath, 'diffusion', 'nodif_brain.nii.gz')
        movFile     = r
        o           = join(subPath, 'mask.localizer.MNI.MNI152_T1_1mm_brain2brain.norm2nodif_brain',   oName)
        masterFile  = movFile
        reg         = join(subPath, 'reg',       'norm2nodif_brain.aff12.1D')
        head, tail = split(o)
        if not os.path.isdir(head):
            os.mkdir(head)
        try:
            applyReg(subPath, movFile, targFile, masterFile, o, reg, warp='srs', thr=0.05)
        except:
            print("failed: {}".format(movFile))
            continue

# transform aud_rsa ROI
for sub in subs:
    mainDir     = '/media/richard/camcan/Projects/SpeechTBT/'
    locROI_Dir  = join(mainDir, 'data.04mask.localizer.sri_slice')
    roiPaths     = [join(locROI_Dir, f) for f in listdir(locROI_Dir) if isfile(join(locROI_Dir, f)) if 'aud_RSA' in f ]
    subPath     = join('/media/richard/camcan/Projects/SpeechTBT/data.11mrtrix',sub)

    # r = roiPaths[0]
    for r in roiPaths:

        try:
            outName     = basename(r).replace('.nii','.MNI152_T1_1mm_brain2brain.nii.gz')
            targFile    = '/usr/share/fsl/data/standard/MNI152_T1_1mm_brain.nii.gz'
            movFile     = r
            o           = join(subPath, 'mask.localizer.MNI.MNI152_T1_1mm_brain2brain', outName)
            masterFile  = join(subPath, 'mri', 'brain.nii.gz')
            reg         = join(subPath, 'reg', 'MNI152_T1_1mm_brain2brain.mat.aff12.1D')
            head, tail  = split(o)


            applyReg(subPath, movFile, targFile, masterFile, o, reg, warp='srs', thr=0.05)


            outName     = basename(outName).replace('.nii.gz','.norm2nodif.nii.gz')
            targFile    = join(subPath, 'diffusion', 'nodif_brain.nii.gz')
            oHead, oTail= split(o)
            movFile     = join("{}.bin".format(oHead), oTail.replace('.nii.gz','.bin.nii.gz'))
            o           = join(subPath, 'mask.localizer.MNI.MNI152_T1_1mm_brain2brain.norm2nodif_brain', outName)
            masterFile  = join(subPath, 'mri', 'norm.nodif_brain.nii.gz')
            reg         = join(subPath, 'reg', 'norm2nodif_brain.aff12.1D')
            head, tail  = split(o)


            applyReg(subPath, movFile, targFile, masterFile, o, reg, warp='srs', thr=0.05)
        except:
            print("failed: {}".format(movFile))
            continue

# transform WM.seg.mgz
for sub in subs:

    subPath     = join('/media/richard/camcan/Projects/SpeechTBT/data.11mrtrix',sub)
    movFile   = join(subPath, 'mri', 'wm.seg.mgz')
    
    outFile     = basename(inputPath).replace('.nii.gz','.norm2nodif.nii.gz')
    targFile    = join(subPath, 'diffusion', 'nodif_brain.nii.gz')
    
    outPath     = join(subPath, 'mri',   outFile)
    masterFile  = movFile
    reg         = join(subPath, 'reg',       'norm2nodif_brain.aff12.1D')
    head, tail  = split(outPath)
    if not os.path.isdir(head):
        os.mkdir(head)
    try:
        movFile2=movFile.replace('.mgz','.nii.gz')
        mrconvert(movFile, movFile2)
        applyReg(subPath, movFile2, targFile, movFile2, outPath, reg, warp='srs')
    except:
        print("failed: {}".format(movFile))
        continue



failed = []
#sub = subs[0]
for sub in subs:

    HCPMask                 = join(mainDir, sub , 'HCP-MMP1.nii.gz')
    LUTtemplate             = join(mainDir, 'Template_primeParc')
    LUTtemplate_cum_sorted  = join(mainDir, 'Template_primeParc_cumulative_sorted')

    locROI_Dir              = join(mainDir, sub, 'mask.localizer.MNI.MNI152_T1_1mm_brain2brain.norm2nodif_brain.bin')
    locROI_Paths            = [join(locROI_Dir, f) for f in listdir(locROI_Dir)
                               if isfile(join(locROI_Dir, f))]

    nodeParcPrimeFile       = join(mainDir, sub, "{}_{}".format(basename(locROI_Dir), 'primeParc'))
    nodeParcLUTFile         = join(mainDir, sub, "{}_{}".format(basename(locROI_Dir), 'LUTParc'))
    nodeParcFile            = join(mainDir, sub, "{}_{}".format(basename(locROI_Dir), 'Parc'))
    nodeParcFileNIFTI       = join(mainDir, sub, "{}_{}".format(basename(locROI_Dir), 'Parc.nii.gz'))
    nodeParcFileMIF         = join(mainDir, sub, "{}_{}".format(basename(locROI_Dir), 'Parc.mif'))
    nodeParcFileFix         = join(mainDir, sub, "{}_{}".format(basename(locROI_Dir), 'ParcFix'))

    wmParc                  = join(mainDir, sub, "mri/wm.seg.mgz")

    sift                    = join(mainDir, sub, 'mrtrix3', '10M_SIFT.tck')
    try:
        nodeParc2(locROI_Paths, nodeParcPrimeFile, LUTtemplate)
    except:
        print("failed: {}".format(nodeParcPrimeFile))
        failed.append(nodeParcPrimeFile)
        continue
print(failed)

create_cumPrimeLUT(LUTtemplate)

for sub in subs:

    HCPMask             =join(mainDir, sub , 'HCP-MMP1.nii.gz')
    LUTtemplate = join(mainDir, 'Template_primeParc')
    LUTtemplate_cum_sorted = join(mainDir, 'Template_primeParc_cumulative_sorted')

    locROI_Dir          =join(mainDir, sub, 'mask.localizer.MNI.MNI152_T1_1mm_brain2brain.norm2nodif_brain.bin')
    locROI_Paths        =[join(locROI_Dir, f) for f in listdir(locROI_Dir) if isfile(join(locROI_Dir, f))]

    nodeParcPrimeFile   = join(mainDir, sub, "{}_{}".format(basename(locROI_Dir), 'primeParc'))
    nodeParcLUTFile     = join(mainDir, sub, "{}_{}".format(basename(locROI_Dir), 'LUTParc'))
    nodeParcFile        = join(mainDir, sub, "{}_{}".format(basename(locROI_Dir), 'Parc'))
    nodeParcFileNIFTI   = join(mainDir, sub, "{}_{}".format(basename(locROI_Dir), 'Parc.nii.gz'))
    nodeParcFileMIF     = join(mainDir, sub, "{}_{}".format(basename(locROI_Dir), 'Parc.mif'))
    nodeParcFileFix     = join(mainDir, sub, "{}_{}".format(basename(locROI_Dir), 'ParcFix'))

    # this should be xfm to nodif
    wmParc              = join(mainDir, sub, "mri/wm.seg.mgz")
    sift = join(mainDir, sub, 'mrtrix3', '10M_SIFT.tck')


    mrtrixLUTParc2(nodeParcPrimeFile, LUTtemplate_cum_sorted, nodeParcFile)

    #####   assignStreamlines
    dumpNifti(nodeParcFile, wmParc, search=0)
    assignStreamlines(sift, "{}.nii.gz".format(nodeParcFileFix))


for sub in subs:
    try:
        LUTtemplate = join(mainDir, 'Template_primeParc')
        LUTtemplate_cum_sorted = join(mainDir, 'Template_primeParc_cumulative_sorted')

        inConnFile  = join(mainDir, sub, 'mask.localizer.MNI.MNI152_T1_1mm_brain2brain.norm2nodif_brain.bin_ParcFix_Conn')
        outConnFile = join(mainDir, sub, 'mask.localizer.MNI.MNI152_T1_1mm_brain2brain.norm2nodif_brain.bin_ParcFix_Conn_reduced')
        LUTsub      = join(mainDir, sub, 'mask.localizer.MNI.MNI152_T1_1mm_brain2brain.norm2nodif_brain.bin_Parc')
        connOutDir  = join(mainDir, 'connMats')

        reduceConn(inConnFile, LUTsub, LUTtemplate, outConnFile)

        getConnMat(outConnFile, LUTtemplate, connOutDir, title='Localizer Tract Count')

    except:
        print("sub failed: {}".format(sub))



outFileName = 'mask.localizer.MNI.MNI152_T1_1mm_brain2brain.norm2nodif_brain.bin_ParcFix_Conn_reduced'
subMats = [join(mainDir, f, outFileName) for f in subs if isfile(join(mainDir, f, outFileName))]
getStats(subMats, connOutDir, LUTtemplate)

binaryPlot(subMats, connOutDir, LUTtemplate, 'gnuplot', thresh=0)
binaryPlot(subMats, connOutDir, LUTtemplate, 'gnuplot', thresh=5)
binaryPlot(subMats, connOutDir, LUTtemplate, 'gnuplot', thresh=10)
binaryPlot(subMats, connOutDir, LUTtemplate, 'gnuplot', thresh=15)
binaryPlot(subMats, connOutDir, LUTtemplate, 'gnuplot', thresh=20)
binaryPlot(subMats, connOutDir, LUTtemplate, 'gnuplot', thresh=30)
binaryPlot(subMats, connOutDir, LUTtemplate, 'gnuplot', thresh=50)

































#####   getConnMat

# mainDir     = '/home/richard/Desktop/test_annot/MR1103'
# connFile    = join(mainDir, 'connectome_Glasser-Localizer_bin_fix.csv')
# LUT         = join(mainDir, 'mask.localizer-Glasser.bin.fix', 'Glasser-Localizer.bin.fix')
#
# getConnMat(connFile, LUT)


# from intersectROI.py
#
# mainDir             ='/home/richard/Desktop/test_annot'
#
# HCPMask             =join(mainDir, 'out3', 'MR1103', 'HCP-MMP1.nii.gz')
#
# locROI_Dir          =join(mainDir, 'MR1103', 'mask.localizer.MNI152_T1_1mm_brain2brain')
# locROI_Names        =[f for f in listdir(locROI_Dir) if isfile(join(locROI_Dir, f))]
# locROI_Paths        =[join(locROI_Dir, f) for f in listdir(locROI_Dir) if isfile(join(locROI_Dir, f))]
#
# glasserROI_Dir      =join(mainDir, 'out3', 'MR1103', 'masks')
# glasserROI_Names    =[f for f in listdir(glasserROI_Dir) if isfile(join(glasserROI_Dir, f))]
# glasserROI_Paths    =[join(glasserROI_Dir, f) for f in listdir(glasserROI_Dir) if isfile(join(glasserROI_Dir, f))]
#
# nodeParcFile        =join(mainDir, 'MR1103','nodeParcPrime')
#
# outDir              =join(mainDir, 'MR1103', 'mask.localizer-Glasser')
# outDir2             =join(mainDir, 'MR1103', 'mask.localizer-Glasser.bin')
# outDir3             =join(mainDir, 'MR1103', 'mask.localizer-Glasser.bin.papers')
#
# outPath             =[join(outDir, f) for f in locROI_Names]
#


#####   MRview

mainDir             ='/home/richard/Desktop/test_annot'
slFile              =join(mainDir, 'MR1103_streamline-mask.csv')

#roiAll          =['/'.join([roiDir,f]) for f in os.listdir(roiDir) if isfile(join(roiDir, f))]
#streamlinesAll  =['/'.join([streamlineDir,f]) for f in os.listdir(streamlineDir) if isfile(join(streamlineDir, f))]

roiDir              =join(mainDir, 'MR1103', 'mask.localizer-Glasser')
roisAll             =[f for f in listdir(roiDir) if isfile(join(roiDir, f))]
roisAllPath         =[join(roiDir, f) for f in roisAll]

tractDir            =join(mainDir, 'MR1103','streamlines_all_Glasser-Localizer')
tractsAll           =[f for f in listdir(tractDir) if isfile(join(tractDir, f))]
tractsAllPath       =[join(tractDir, f) for f in tractsAll]

img                 =join(mainDir, 'MR1103','mri','brain.nii.gz')

tracts              = tractsAllPath
rois                = roisAllPath



#1103_VWFA_mask_1019
sTracts = selectTracts(tracts, seed=range(1,4))
plotMrview(img, sTracts, rois)

#1103_IFG_mask_1075
sTracts = selectTracts(tracts, seed=range(4,11))
plotMrview(img, sTracts, rois)

#1103_VT_R_ant_parietal_2053
sTracts = selectTracts(tracts, seed=range(11,18))
plotMrview(img, sTracts, rois)

#1103_VT_L_supp_motor_test_1044
sTracts = selectTracts(tracts, seed=range(18,19))
plotMrview(img, sTracts, rois)

#TVSA
sTracts = selectTracts(tracts, seed=range(19,25))
plotMrview(img, sTracts, rois)

#TPC
sTracts = selectTracts(tracts, seed=range(25,31))
plotMrview(img, sTracts, rois)

#VT_L_S2
sTracts = selectTracts(tracts, seed=range(31,35))
plotMrview(img, sTracts, rois)

#VT_R_S2
sTracts = selectTracts(tracts, seed=range(35,42))
plotMrview(img, sTracts, rois)

#VT_L_insula
sTracts = selectTracts(tracts, seed=range(42,47))
plotMrview(img, sTracts, rois)

#midtemp from word contrast
sTracts = selectTracts(tracts, seed=range(47,53))
plotMrview(img, sTracts, rois)

#VT_L_ant_parietal
sTracts = selectTracts(tracts, seed=range(53,55))
plotMrview(img, sTracts, rois)

#pSTS
sTracts = selectTracts(tracts, seed=range(55,61))
plotMrview(img, sTracts, rois)

#VT_R_suppmotor
sTracts = selectTracts(tracts, seed=range(61,63))
plotMrview(img, sTracts, rois)

#VT_L_S1
sTracts = selectTracts(tracts, seed=range(63,65))
plotMrview(img, sTracts, rois)

#antTemp
sTracts = selectTracts(tracts, seed=range(65,69))
plotMrview(img, sTracts, rois)


# VT nad STS
seed   = [31,32,33,34,63,64]
target = [47,48,49,50,51,52,55,56,57,58,59,60,65,66,67,68]
all    = [31,32,33,34,63,64,47,48,49,50,51,52,55,56,57,58,59,60,65,66,67,68]
sTracts = selectTracts(tracts, seed=all, target=all)
plotMrview(img, sTracts, rois)







mainDir             ='/home/richard/Desktop/test_annot'
#slFile              =join(mainDir, 'MR1103_streamline-mask.csv')

#roiAll          =['/'.join([roiDir,f]) for f in os.listdir(roiDir) if isfile(join(roiDir, f))]
#streamlinesAll  =['/'.join([streamlineDir,f]) for f in os.listdir(streamlineDir) if isfile(join(streamlineDir, f))]

roiDir              =join(mainDir, 'MR1103', 'mask.localizer-Glasser.bin')
roisAll             =[f for f in os.listdir(roiDir) if isfile(join(roiDir, f))]
roisAllPath         =[join(roiDir, f) for f in roisAll]

tractDir            =join(mainDir, 'MR1103','streamlines_all_Glasser-Localizer_bin')
tractsAll           =[f for f in os.listdir(tractDir) if isfile(join(tractDir, f))]
tractsAllPath       =[join(tractDir, f) for f in tractsAll]

img                 =join(mainDir, 'MR1103','mri','brain.nii.gz')

tracts              = tractsAllPath
rois                = roisAllPath





sTracts = selectTracts(tracts, seed=[1])
plotMrview(img, sTracts, rois)










