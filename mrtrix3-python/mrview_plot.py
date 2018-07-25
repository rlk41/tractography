import csv
import os
import sys
import subprocess
from string import Template
import string
from os.path import join, isfile


def run_command(command):
    p = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = p.communicate()
    return(output,error)

def selectTracts(tracts, seed=None, target=None):
    from os.path import basename
    # if seed > target switch target = seed
    out, allS, allT, allFull = [], [], [], []
    for f in tracts:
        ff = basename(f)
        ff = ff.rstrip('.tck')
        ff = ff.split('-')
        allS.append(int(ff[0]))
        allT.append(int(ff[1]))
        allFull.append(f)
    unq_allS = sorted(list(set(allS)))
    unq_allT = sorted(list(set(allT)))
    if not seed:    seed   = unq_allS
    if not target:  target = unq_allT
    print('seed: {} taget: {}'.format(seed, target))
    for s in seed:
        for t in target:
            for a in range(len(allFull)):
                if s == allS[a] and t is allT[a]:
                    print('{}-{}     {}'.format(s, t, basename(allFull[a])))
                    out.append(allFull[a])
    return out

def plotMrview(img, tracts, rois):
    import itertools
    mTract = []
    for tract in tracts:
        mTract.append('-tractography.load')
        mTract.append(tract)
    mRoi = []
    for roi in rois:
        mRoi.append('-roi.load')
        mRoi.append(roi)
    mImg = ['-load', img]
    c = [['/usr/local/mrtrix3/bin/mrview'],
         ['-tractography.slab', '0'],
         ['-tractography.opacity','0.33'],
         ['-mode', '2'],
         mImg,
         mRoi,
         mTract]
    c = list(itertools.chain.from_iterable(c)).join(' ')
    output, error = run_command(c)

#
# mainDir             ='/home/richard/Desktop/test_annot'
# slFile              =join(mainDir, 'MR1103_streamline-mask.csv')
#
# #roiAll          =['/'.join([roiDir,f]) for f in os.listdir(roiDir) if isfile(join(roiDir, f))]
# #streamlinesAll  =['/'.join([streamlineDir,f]) for f in os.listdir(streamlineDir) if isfile(join(streamlineDir, f))]
#
# roiDir              =join(mainDir, 'MR1103', 'mask.localizer-Glasser')
# roisAll             =[f for f in os.listdir(roiDir) if isfile(join(roiDir, f))]
# roisAllPath         =[join(roiDir, f) for f in roisAll]
#
# tractDir            =join(mainDir, 'MR1103','streamlines_all_Glasser-Localizer')
# tractsAll           =[f for f in os.listdir(tractDir) if isfile(join(tractDir, f))]
# tractsAllPath       =[join(tractDir, f) for f in tractsAll]
#
# img                 =join(mainDir, 'MR1103','mri','brain.nii.gz')
#
# tracts              = tractsAllPath
# rois                = roisAllPath
#
#
#
# #1103_VWFA_mask_1019
# sTracts = selectTracts(tracts, seed=range(1,4))
# plotMrview(img, sTracts, rois)
#
# #1103_IFG_mask_1075
# sTracts = selectTracts(tracts, seed=range(4,11))
# plotMrview(img, sTracts, rois)
#
# #1103_VT_R_ant_parietal_2053
# sTracts = selectTracts(tracts, seed=range(11,18))
# plotMrview(img, sTracts, rois)
#
# #1103_VT_L_supp_motor_test_1044
# sTracts = selectTracts(tracts, seed=range(18,19))
# plotMrview(img, sTracts, rois)
#
# #TVSA
# sTracts = selectTracts(tracts, seed=range(19,25))
# plotMrview(img, sTracts, rois)
#
# #TPC
# sTracts = selectTracts(tracts, seed=range(25,31))
# plotMrview(img, sTracts, rois)
#
# #VT_L_S2
# sTracts = selectTracts(tracts, seed=range(31,35))
# plotMrview(img, sTracts, rois)
#
# #VT_R_S2
# sTracts = selectTracts(tracts, seed=range(35,42))
# plotMrview(img, sTracts, rois)
#
# #VT_L_insula
# sTracts = selectTracts(tracts, seed=range(42,47))
# plotMrview(img, sTracts, rois)
#
# #midtemp from word contrast
# sTracts = selectTracts(tracts, seed=range(47,53))
# plotMrview(img, sTracts, rois)
#
# #VT_L_ant_parietal
# sTracts = selectTracts(tracts, seed=range(53,55))
# plotMrview(img, sTracts, rois)
#
# #pSTS
# sTracts = selectTracts(tracts, seed=range(55,61))
# plotMrview(img, sTracts, rois)
#
# #VT_R_suppmotor
# sTracts = selectTracts(tracts, seed=range(61,63))
# plotMrview(img, sTracts, rois)
#
# #VT_L_S1
# sTracts = selectTracts(tracts, seed=range(63,65))
# plotMrview(img, sTracts, rois)
#
# #antTemp
# sTracts = selectTracts(tracts, seed=range(65,69))
# plotMrview(img, sTracts, rois)
#
#
# # VT nad STS
# seed   = [31,32,33,34,63,64]
# target = [47,48,49,50,51,52,55,56,57,58,59,60,65,66,67,68]
# all    = [31,32,33,34,63,64,47,48,49,50,51,52,55,56,57,58,59,60,65,66,67,68]
# sTracts = selectTracts(tracts, seed=all, target=all)
# plotMrview(img, sTracts, rois)
#
#
#
#
#
#
#
# mainDir             ='/home/richard/Desktop/test_annot'
# #slFile              =join(mainDir, 'MR1103_streamline-mask.csv')
#
# #roiAll          =['/'.join([roiDir,f]) for f in os.listdir(roiDir) if isfile(join(roiDir, f))]
# #streamlinesAll  =['/'.join([streamlineDir,f]) for f in os.listdir(streamlineDir) if isfile(join(streamlineDir, f))]
#
# roiDir              =join(mainDir, 'MR1103', 'mask.localizer-Glasser.bin')
# roisAll             =[f for f in os.listdir(roiDir) if isfile(join(roiDir, f))]
# roisAllPath         =[join(roiDir, f) for f in roisAll]
#
# tractDir            =join(mainDir, 'MR1103','streamlines_all_Glasser-Localizer_bin')
# tractsAll           =[f for f in os.listdir(tractDir) if isfile(join(tractDir, f))]
# tractsAllPath       =[join(tractDir, f) for f in tractsAll]
#
# img                 =join(mainDir, 'MR1103','mri','brain.nii.gz')
#
# tracts              = tractsAllPath
# rois                = roisAllPath
#
#
#
#
#
# sTracts = selectTracts(tracts, seed=[1])
# plotMrview(img, sTracts, rois)
#
#
#
#
#
#
#
#
#
#






#mrview -load /home/richard/Desktop/test_annot/MR1103/mri/orig.nii.gz -tractography.load /home/richard/Desktop/test_annot/MR1103/streamlines_all/HCP-MMP1_all197-234.tck -tractography.load /home/richard/Desktop/test_annot/MR1103/streamlines_all/HCP-MMP1_all221-252.tck




# roiNamesKeep=[]
# slNamesKeep=[]
#
# with open(slFile) as csvfile:
#     reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#     next(reader, None)
#     for row in reader:
#         roiNamesKeep.append('-overlay.load {}/{}.nii.gz'.format(roiDir, row[1]))
#         slNamesKeep.append(row[4])
#
# slFilesKeep = ['-tractography.load {}/{}'.format(slDir, fff) for f in slNamesKeep for ff in slNamesKeep for fff in slNameAll if 'HCP-MMP1_all{}-{}.tck'.format(f, ff) in fff]
#
# #join(slDir, fff)
#
# roiNamesKeepa=roiNamesKeep[1]
# slFilesKeepa=slFilesKeep[1]

