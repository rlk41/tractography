#!/usr/bin/env bash


SUBJECTS_DIR='/home/richard/Desktop/test_annot';
subject='fsaverage';

mri_aparc2aseg --s ${subject} --o fsaverage.HCP-MMP1.nii.gz  --annot HCP-MMP1

