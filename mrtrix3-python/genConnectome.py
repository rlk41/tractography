import csv
import  numpy as np
from    numpy import genfromtxt, savetxt
import  matplotlib.pyplot as plt
from os.path import split
from os.path import join
import  numpy as np
from    numpy import genfromtxt
import  matplotlib.pyplot as plt
import  matplotlib
from os.path import split, basename
from string import Template

def getLabels(LUT):
    import csv

    ls = []
    with open(LUT, newline='\n') as csvfile:
        l = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in l:
            if row:
                print(row)
                ls.append(row[2])

    return ls

def getPlt(M, labs, title, annotate=True, cmap='gist_ncar'):

    #M = genfromtxt(connFile, delimiter=' ')
    M = M + np.triu(M).T

    fig = plt.figure(figsize=(15,15))
    plt.clf()
    ax = fig.add_subplot(111)
    ax.set_aspect(1)
    #cmap = "plt.cm.{}".format(cmap)
    res = ax.imshow(M, cmap=cmap, #gist_ncar,
                    interpolation='nearest')

    width, height = M.shape
    cb = fig.colorbar(res)


    plt.xticks(range(width),  labs[:width], rotation=90)
    plt.yticks(range(height), labs[:height])
    plt.title(title)
    #plt.imshow()

    if annotate:
        for x in range(width):
            for y in range(height):
                ax.annotate(str(M[x][y]), xy=(y, x),
                            horizontalalignment='center',
                            verticalalignment='center',
                            fontsize=8)

    return plt


def getConnMat(connFile, LUTtemplate, outDir, title, annotate=True):

    head, tail = split(connFile)

    labs = getLabels(LUTtemplate)
    M = genfromtxt(connFile, delimiter=' ')
    plt = getPlt(M, labs, title, annotate)

    if not annotate:
        saveName = '{}.{}.png'.format(basename(split(connFile)[0]),title.replace(' ', '_'))  #tail.rstrip('.csv'))
    else:
        saveName = '{}.{}.annot.png'.format(basename(split(connFile)[0]),title.replace(' ', '_'))  #tail.rstrip('.csv'))

    plt.savefig(join(outDir, saveName), format='png')
    plt.close()
    return True




def reduceConn(inConnFile, LUTsub, LUTtemplate, outConnFile):

    labs   = getLabels(LUTtemplate)
    matLen = len(labs)

    temp_fill   = []
    temp_2fill  = []

    with open(LUTsub, 'rt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            if row:
                temp_fill.append(row[0])
                temp_2fill.append(row[2].split('_'))

    fill2fills  = dict(zip(np.array(temp_fill).astype(int), temp_2fill))

    M = genfromtxt(inConnFile, delimiter=' ', dtype=int)
    I = np.zeros_like(M, dtype=int)
    _x,_y = I.shape
    O = np.zeros([matLen,matLen])

    keys = fill2fills.keys()
    for k in keys:
        for f in fill2fills[k]:
            print("row {} to {}".format(k, f))
            k = int(k) - 1
            f = int(f) - 1
            #I[f,:] = M[k,:]
            I[:,f] = M[:,k] + I[:,f]

    II = np.triu(I) + np.tril(I).T
    O = II + np.triu(II).T
    O = II[0:matLen,0:matLen]
    np.fill_diagonal(O, 0)
    savetxt(outConnFile, O, delimiter=' ', newline='\n')

    return True


def getStats(subMats, outDir, LUTtemplate):

    labs = getLabels(LUTtemplate)

    
    mats = [ genfromtxt(m, delimiter=' ', dtype=float) for m in subMats ]


    M = np.stack(mats)


    aveM = np.mean(M, axis=0)
    avePlt = getPlt(aveM, labs, title='Tract Count Mean (Localizers)', cmap='gist_ncar')
    #saveName = '{}.annot.png'.format('TC_Mean_Localizers')
    avePlt.savefig(join(outDir, '{}.annot.png'.format('TC_Mean_Localizers')), format='png')
    avePlt.close()
    
    varM = np.var(M, axis=0)
    varPlt = getPlt(varM, labs, title='Tract Count Variance (Localizers)', annotate=False, cmap='gist_ncar')
    #saveName = '{}.annot.png'.format('TC_var_Localizers')
    varPlt.savefig(join(outDir, '{}.annot.png'.format('TC_var_Localizers')), format='png')
    varPlt.close()
    return True

def binaryPlot(subMats, outDir, LUTtemplate, cmap='gnuplot', label=False, thresh=0):

    labs = getLabels(LUTtemplate)

    mats = [ genfromtxt(m, delimiter=' ', dtype=float) for m in subMats ]

    M = np.stack(mats)
    
    M[np.where(M <= thresh)] = 0
    M[np.where(M > thresh)] = 1


    n=len(mats)
    aveM = np.mean(M, axis=0)
    avePlt = getPlt(aveM, labs, title='Percent of subjects with ROI connectivity (Localizers; n={}; thresh={})'.format(n, thresh), cmap=cmap)
    if not label: 
        label = 'percentConn-{}-thresh_{}'.format(basename(LUTtemplate), thresh)

    avePlt.savefig(join(outDir, '{}.annot.png'.format(label)), format='png')

    avePlt.close()
    return True



# mainDir     = '/home/richard/Desktop/test_annot/MR1103'
# connFile    = join(mainDir, 'connectome_Glasser-Localizer_bin_fix.csv')
# LUT         = join(mainDir, 'mask.localizer-Glasser.bin.fix', 'Glasser-Localizer.bin.fix')
#
# getConnMat(connFile, LUT)
#



# tck2connectome \
#     ./mrtrix3/10M_SIFT.tck \
#                     ./mask.localizer-Glasser.bin/nodes_Glasser-Localizer.mif \
#                     ./connectome_Glasser-Localizer_bin.csv -zero_diagonal \
#                 -out_assignments ./out_assign_Glasser-Localizer_bin -force