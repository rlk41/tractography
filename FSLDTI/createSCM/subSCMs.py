#!/usr/bin/python

import numpy as np
import matplotlib.pyplot
import os
from numpy import genfromtxt



class subSCMs(object):
    def __init__(self, subID, subsDir, lists):

        self.subsDir        = subsDir
        self.subID          = subID
        self.subDir         = os.path.join(self.subsDir, self.subID)

        #self.lists          = lists
        self.conn           = {}
        self.N              = 0
    def createLists(self):


    def createConn(self):
        for roi in processed_seed_list:
            matrix_file = dataDir +'MR'+subNum+'/results/' + roi.replace('.gz','').replace('/isilon/scratch/rlk41/data03/MR1106/rois','') + '/matrix_seeds_to_all_targets'     #matrix_template.format(roi=roi.replace('.gz',''))
            waytotal_file = os.path.join(matrix_file.replace('matrix_seeds_to_all_targets',''), 'waytotal')
            rois.append(roi)
            try:
                conn[idx, :] = collapse_probtrack_results(waytotal_file, matrix_file)
            except OSError:
                pass
            idx += 1


        return self.conn

    def createConnOut(self, list):

        mask = np.zeros(self.N, dtype=int)
        mask[list] = 1

        connOut = self.conn[np.ix_(list, list)]

        return connOut


    def plot(self, connOut):

        # will plot connOut

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
