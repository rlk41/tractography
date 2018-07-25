import numpy as np
import matplotlib as mpl
import matplotlib.pyplot
plt = mpl.pyplot
import nibabel
import os
import csv
from numpy import genfromtxt

subID='MR1106'
subNum='1106'
os.chdir('/home/richard/Desktop/freesurfer2/'+ subID)

def collapse_probtrack_results(waytotal_file, matrix_file):
    with open(waytotal_file) as f:
        waytotal = int(f.read())
    data = genfromtxt(matrix_file, delimiter='  ')
    ds = data.sum(axis=0)
    collapsed = data.sum(axis=0) / waytotal * 100.

    print(matrix_file)
    print(ds)
    print(collapsed)


    return collapsed

matrix_template = '/home/richard/Desktop/freesurfer2/MR'+ subNum + '/results/' + subNum + '_{roi}/matrix_seeds_to_all_targets'
processed_seed_list = [s.replace('gz.resampled.inflate_GM+tlrc.nii','').replace('/isilon/scratch/rlk41/freesurfer2/MR' + subNum +  '/rois/' + subNum + '_', '')
    for s in open('rois.txt').read().split('\n')
    if s]
#print(processed_seed_list)
N = len(processed_seed_list)
conn = np.zeros((N, N))
rois=[]
idx = 0
for roi in processed_seed_list:
    print(roi)
    matrix_file = matrix_template.format(roi=roi.replace('.gz',''))
    print('matrix file: ', matrix_file)
    seed_directory = os.path.dirname('rois')
    #print(seed_directory)
    roi = os.path.basename(seed_directory).replace('.nii.gz', '')
    waytotal_file = os.path.join(matrix_file.replace('matrix_seeds_to_all_targets',''), 'waytotal')
    print("waytotal file: ", waytotal_file)
    rois.append(roi)
    try:
        # if this particular seed hasn't finished processing, you can still
        # build the matrix by catching OSErrors that pop up from trying
        # to open the non-existent files
        conn[idx, :] = collapse_probtrack_results(waytotal_file, matrix_file)
    except OSError:
        pass
    idx += 1

print(conn)

# figure plotting
fig = matplotlib.pyplot.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(conn, interpolation='nearest', )
cax.set_cmap('hot')
#caxes = cax.get_axes()

# set number of ticks
#caxes.set_xticks(range(len(new_order)))
#caxes.set_yticks(range(len(new_order)))

# label the ticks
#caxes.set_xticklabels(new_order, rotation=90)
#caxes.set_yticklabels(new_order, rotation=0)

# axes labels
#caxes.set_xlabel('Target ROI', fontsize=20)
#caxes.set_ylabel('Seed ROI', fontsize=20)

# Colorbar
cbar = fig.colorbar(cax)
#cbar.set_label('% of streamlines from seed to target', rotation=-90, fontsize=20)

# title text
#title_text = ax.set_title('Structural Connectivity with Freesurfer Labels & ProbtrackX2',
#    fontsize=26)
#title_text.set_position((.5, 1.10))

fig.show()
fig.savefig('/home/richard/Desktop/freesurfer2/MR' + subNum + '/connectome_fsl.png')

