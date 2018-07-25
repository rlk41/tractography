import numpy as np
#import matplotlib as mpl
import matplotlib.pyplot
#import matplotlib.pyplot as plt
#plt = mpl.pyplot
import os
from numpy import genfromtxt
from createSCM.readTable import readTable



dataDir='/home/richard/Desktop/data03/'
tbl = 'Group_seg150_BAindexing_setA.txt'

subNums=['1103','1106','1135','1136','1137','1140']
roiTbl = readTable(tbl)

for subNum in subNums:
    subID='MR' + subNum
    print('Running: ' + subID)

    os.chdir(dataDir + subID)


###
    processed_seed_list =   [ os.path.basename(s)
                            for s in open('rois.txt').read().split('\n')
                            if s]

    all         = [i for i in range(len(processed_seed_list)) if processed_seed_list[i]]
    localizer   = [i for i in range(len(processed_seed_list)) if processed_seed_list[i].startswith(subNum)]
    shen2013    = [i for i in range(len(processed_seed_list)) if not processed_seed_list[i].startswith(subNum)]
    #sts         = [i for i in range(len(processed_seed_list)) if not processed_seed_list[i].startswith(subNum)]

    lists = [all, localizer, shen2013]
    listNames = ['Shen2013 and Localizer', 'Localizer', 'Shen2013']


### create SCM class


    N = len(processed_seed_list)
    conn = np.zeros((N, N))
    rois=[]
    idx = 0


    #test.createConn()

     for roi in processed_seed_list:
         matrix_file = dataDir +'MR'+subNum+'/results/' + roi.replace('.gz','').replace('/isilon/scratch/rlk41/data03/MR1106/rois','') + '/matrix_seeds_to_all_targets'     #matrix_template.format(roi=roi.replace('.gz',''))
         waytotal_file = os.path.join(matrix_file.replace('matrix_seeds_to_all_targets',''), 'waytotal')
         rois.append(roi)
         try:
             conn[idx, :] = collapse_probtrack_results(waytotal_file, matrix_file)
         except OSError:
             pass
         idx += 1

    allConnOut = test.createConnOut(all)
    locConnOut = test.createConnOut(localizer)
    shen2013ConnOut = test.createConnOut(shen2013)



for i in range(len(lists)):

        mask = np.zeros(N, dtype=int)
        mask[lists[i]] = 1

        connOut = conn[np.ix_(lists[i],lists[i])]


        # figure plotting
        fig = matplotlib.pyplot.figure(figsize=(12, 9), dpi=100,)
        ax = fig.add_subplot(111)
        cax = ax.matshow(connOut, interpolation='nearest', )
        cax.set_cmap('hot')

        if listNames[i] == 'Localizer':
            labs = [processed_seed_list[ll].replace(subNum+'_','').replace('.niinodif.thresh.bin.nii.gz','') for ll in lists[i] ]
            matplotlib.pyplot.xticks(range(len(lists[i])), labs, rotation='vertical', fontsize=10)
            matplotlib.pyplot.yticks(range(len(lists[i])), labs, rotation='horizontal', fontsize=10)        # axes labels

        matplotlib.pyplot.xlabel('Target ROI', fontsize=15)
        matplotlib.pyplot.ylabel('Seed ROI', fontsize=15)

        cbar = fig.colorbar(cax)

        fig.savefig(dataDir+'MR' + subNum + '/connectome_fsl_'+listNames[i]+'.png')
        fig.savefig(dataDir+'/plots/' + 'MR'+subNum + '_connectome_fsl_'+listNames[i]+'.png')
