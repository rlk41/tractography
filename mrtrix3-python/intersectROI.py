import nibabel as nib
from nibabel.nifti1 import load, save
from nibabel.viewers import OrthoSlicer3D
import numpy as np
import csv
from os.path import join, isfile, exists, basename, split
from run_command import run_command
from os import listdir

# def replaceBin(Data, num):
#     Data[np.where(Data == 1)] = num
#     return Data


#     for unq in np.unique(g):
#         if unq > 1000:
#             unqCount = len(np.where(g == unq))
#             r = bin(g, unq, fill)
#             aff  = locROI_Load.affine
#             head = locROI_Load.header
#             glLabel = '{}_{}_{}'.format(label, unq)
#             saveNifti(r, aff, head, outDir, '{}_{}.unq'.format(fill,label,unq))



def intersect(a, b, new):
    # need to automate expansion of primes
    #c = np.zeros(hcp_Data.shape, dtype=int)

    head, tail  = split(new)

    a_Load  = load(a)
    b_Load  = load(b)

    a_Data  = a_Load.get_data()
    b_Data  = b_Load.get_data()

    a_Data[np.where(a_Data != 0)] = 3
    b_Data[np.where(b_Data != 0)] = 7

    a_Data[np.where(a_Data == 0)] = 1
    b_Data[np.where(b_Data == 0)] = 1

    c_Data = a_Data*b_Data

    unq = np.unique(c_Data)
    i = 1
    #u = 3
    for u in unq:
        if u != 1:
            out   = bin(c_Data, u, 1)
            aff   = a_Load.affine
            header  = a_Load.header
            label = '{}_{}'.format(tail,int(u))

            saveNifti(out, aff, header, head, label)

def buildParcellation(roiDir, outPath):

    head, tail  = split(outPath)
    rois        = [join(roiDir, f) for f in listdir(roiDir) if isfile(join(roiDir, f))]

    m       = load(rois[0])
    aff     = m.affine
    header  = m.header

    m_Data  = m.get_data()


    complete    = np.empty(m_Data.shape, dtype=int)
    labLUT      = []
    numLUT      = []
    f = 1
    for a in rois:

        a_head, a_tail = split(a)
        print(a)
        a_Load  = load(a)
        a_Data  = a_Load.get_data()
        o = bin(a_Data, 1, f)
        print(np.unique(o))
        complete += o

        f+=1

        #numLUT.append(f)
        labLUT.append(a_tail)


    numLUT = np.unique(complete)
    print('{} Values: {}'.format(len(numLUT), numLUT))

    saveNifti(complete, aff, header, head, tail)

    csvPath = join(head, tail)
    with open(csvPath, 'w', newline='\n') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(labLUT)):
            spamwriter.writerow([numLUT[i], labLUT[i]])


def dump(Data, ROI):
    ROI = np.array(ROI, dtype=bool)
    g = np.zeros(ROI.shape, dtype=int)
    g[np.where(ROI == 1)] = Data[np.where(ROI != 0)]
    return g

def bin(Data, search, fill):
    g = np.zeros(Data.shape, dtype=int)
    g[np.where(Data == search)] = fill
    return g

def saveNifti(g, aff, head, path, label):
    img = nib.Nifti1Image(g, affine=aff, header=head)
    nib.save(img, join(path,'{}.nii.gz'.format(label)))































































# Comented out moved to top.py

#
# mainDir         ='/home/richard/Desktop/test_annot'
# glasserROI_Dir  =join(mainDir, 'out3', 'MR1103', 'masks')
# locROI_Dir      =join(mainDir, 'MR1103', 'mask.localizer.MNI152_T1_1mm_brain2brain')
# outDir          =join(mainDir, 'MR1103', 'mask.localizer-Glasser')
# outDir2         =join(mainDir, 'MR1103', 'mask.localizer-Glasser.bin')
#
# HCPMask         =join(mainDir, 'out3', 'MR1103', 'HCP-MMP1.nii.gz')
#
# locROI_Name      =[f for f in os.listdir(locROI_Dir) if isfile(join(locROI_Dir, f))]
# glasserROI_Name  =[f for f in os.listdir(glasserROI_Dir) if isfile(join(glasserROI_Dir, f))]
#
# locROI_Path      =[join(locROI_Dir, f) for f in os.listdir(locROI_Dir) if isfile(join(locROI_Dir, f))]
# glasserROI_Path  =[join(glasserROI_Dir, f) for f in os.listdir(glasserROI_Dir) if isfile(join(glasserROI_Dir, f))]
#
# outPath          =[join(outDir, f) for f in locROI_Name]
#
#
# hcpM         = load(HCPMask)
# hcp_Data     = hcpM.get_data()
# c    = 1
# fill = 1
#
# #create LUT for mrtrix
# # tocsv = []
# # tocsv.append(['fill', 'label', 'unq', 'unqCount'])
# #
# # complete = np.zeros(hcp_Data.shape, dtype=int)
# #
# #useUnq = False
# #
# # for lab in range(len(locROI_Name)):
# #     locROI_Load  = load(locROI_Path[lab])
# #     locROI_Data  = locROI_Load.get_data()
# #     label        = locROI_Name[lab].split('.')[0]
# #     g            = dump(hcp_Data, locROI_Load.get_data())
# #
# #     nonUnq = np.zeros(hcp_Data.shape, dtype=int)
# #
# #     for unq in np.unique(g):
# #         if unq > 1000:
# #             unqCount = len(np.where(g == unq))
# #             r = bin(g, unq, fill)
# #             aff  = locROI_Load.affine
# #             head = locROI_Load.header
# #             glLabel = '{}_{}_{}'.format(label, unq)
# #             saveNifti(r, aff, head, outDir, '{}_{}.unq'.format(fill,label,unq))
# #             tocsv.append([fill, glLabel, label, unq, unqCount])
# #             if useUnq:
# #                 fill += 1
# #             complete += r
# #             nonUnq   += r
# #
# #     saveNifti(nonUnq, aff, head, outDir, '{}_{}.unq'.format(fill,label))
# #
# # fill += 1
#
# tocsv = []
# tocsv.append(['fill', 'label'])
#
# complete = np.zeros(hcp_Data.shape, dtype=int)
#
#
#
# for lab in range(len(locROI_Name)):
#     locROI_Load  = load(locROI_Path[lab])
#     locROI_Data  = locROI_Load.get_data()
#
#     aff  = locROI_Load.affine
#     head = locROI_Load.header
#
#     label       = locROI_Name[lab].split('.')[0]
#     glLabel     = '{}_{}'.format(lab+1, label)
#
#
#
#     r            = np.zeros(locROI_Data.shape, dtype=int)
#     g            = dump(hcp_Data, locROI_Load.get_data())
#
#     r[np.where(g > 1000)] = lab+1
#     rr           = bin(r, lab+1, 1)
#
#     saveNifti(rr, aff, head, outDir2, '{}_{}.bin'.format(lab+1,label))
#
#
#     tocsv.append([fill, glLabel, label])
#
#
#     complete += r
#
#
# aff  = hcpM.affine
# head = hcpM.header
# saveNifti(complete, aff, head, outDir2, 'Glasser-Localizer.bin')
#
# csvPath = join(mainDir, 'MR1103','Glasser-Localizer_bin_LUT')
# with open(csvPath, 'w', newline='\n') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter=' ',
#                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     for i in tocsv:
#         spamwriter.writerow(i)
#
#
#
#
#
# a=join(mainDir, 'MR1103','mask.localizer-Glasser.bin.fix','6_1103_TVSA.bin.nii.gz')
# b=join(mainDir, 'MR1103','mask.localizer-Glasser.bin.fix','11_1103_midTemp_from_word_contrast.bin.nii.gz')
# new=join(mainDir, 'MR1103','mask.localizer-Glasser.bin.fix','TVSA_midTemp_wC_Intersect')
# intersect(a,b,new)
#
# roiDir =join(mainDir, 'MR1103','mask.localizer-Glasser.bin.fix')
# outPath=join(roiDir, 'Glasser-Localizer.bin.fix')
# buildParcellation(roiDir, outPath)
#






















# def dump(Data, ROI, fill=False, search=False, thr=False, uthr=False):
#
#     if not thr: thr = np.max(Data) + 1
#     if not uthr: thr = np.min(Data) - 1
#
#     ROI = np.array(ROI, dtype=bool)
#     ROI[np.where(ROI == 1)] = Data[np.where(ROI == 1)]
#
#
#     g = np.zeros(ROI.shape)
#
#     if search or thr or uthr:
#         g[np.where(ROI == search and ROI > thr and ROI < uthr)] = \
#             ROI[np.where(ROI == search and ROI > thr and ROI < uthr)]
#
#
#     else:
#         g[np.where(Data[ROI] == search)] = fill
#
#     if fill:
#         if unique:
#


#saveNifti(g, header, '/home/richard/Desktop/test_annot', 'test-py-dump')



# def dump(Data, ROI, label, seedNum=1, unique=True):
#     ROI = np.array(ROI, dtype=bool)
#     n = seedNum
#
#     if unique:
#         unq = np.unique(Data[ROI])
#         for u in unq:
#             if u > 1000:
#                 g = np.zeros(ROI.shape)
#                 g[np.where(Data[ROI] == u)] = n
#                 n += 1
#
#     if not unique:
#         g = np.zeros(ROI.shape)
#         g[np.where(Data[ROI] > 1000)] = n
#         n += 1
#
#     return
#






# def saveNifits(niftis, path, label):
#     for n in niftis:
#         lab =
#         img = nib.Nifti1Image(niftis[n])
#         nib.save(img, os.path.join(path,'{}{}.nii.gz'.format(label,lab)))







#
# locNum = 1
# glaNum = 1
#
# for f in range(len(locROI_Name)):
#
#
#
#     unq = np.unique(locROI_Data)
#     LUT[f] = [locNum, glaNum, label]
#
#
# Data = replaceBin(Data, num, label)
#
#
#
#
#
#
#
#
#
# OrthoSlicer3D(data).show()
#
#
# if not exists(outDir):
#     os.makedirs(outDir)
#     print('Created Dir: {}'.format(outDir))
# else:
#     print('Exists: {}'.format(outDir))
#
#
#
# for r in range(len(locROI_Path)):
#     c = '/usr/lib/afni/bin/3dmask_tool -input {} {} -prefix {} -frac 1.0 -overwrite'.format(HCPMask, locROI_Path[r], outPath[r])
#     print('{} \n{}'.format(basename(locROI_Path[r]), basename(outPath[r])))
#     print(c)
#     run_command(c)
#
#
#
# 3dmaskdump -input HCP
#

#
#
# slFilesKeep = ['-tractography.load {}/{}'.format(slDir, fff) for f in slNamesKeep for ff in slNamesKeep for fff in slNameAll if 'HCP-MMP1_all{}-{}.tck'.format(f, ff) in fff]
#
# #join(slDir, fff)
#
# roiNamesKeepa=roiNamesKeep[1]
# slFilesKeepa=slFilesKeep[1]
#
# mrview = {
#     'img'           : '-load {}/{}'.format(mainDir, 'MR1103/mri/orig.nii.gz'),
#     'rois'          : join(roiNamesKeepa),
#     'cmap'          : 'jet',
#     'ROIopacity'    : '1',
#     'tracks'        : join(slFilesKeepa),
#     'slab'          : '1'
# }
#
#
#
#
# c = ['/usr/local/mrtrix3/bin/mrview',
#      mrview['img'],
#      mrview['tracks'],
#      mrview['rois'],
#
#      ]
#
#
# #'-tractography.slab',          mrview['slab']
# #'-overlay.interpolation_off',
# #'-overlay.colourmap',          mrview['cmap'],
# #'-roi.opacity',                mrview['ROIopacity'],
#
#
#
# cc=' '.join(c)
# c=c.split(' ')
#
# output, error = run_command(c)
#
# ' '.join(c).split(' ')
#
#
#
# #mrview -load /home/richard/Desktop/test_annot/MR1103/mri/orig.nii.gz -tractography.load /home/richard/Desktop/test_annot/MR1103/streamlines_all/HCP-MMP1_all197-234.tck -tractography.load /home/richard/Desktop/test_annot/MR1103/streamlines_all/HCP-MMP1_all221-252.tck
#
#
#









