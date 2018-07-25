#!/usr/bin/env bash

# /media/richard/camcan/bin/hcp-tractography/mrtrix3-python/warpLoc.sh '/home/richard/Desktop/test_annot' 'MR1103' 'MNI152_T1_1mm_brain' 'mri/brain.mgz' 'mask.localizer.papers'
# /media/richard/camcan/bin/hcp-tractography/mrtrix3-python/warpLoc.sh '/media/richard/camcan/Projects/SpeechTBT/data.10working' 'MR1103' 'MNI152_T1_1mm_brain' 'mri/brain.mgz' 'mask.localizer.MNI'
# for f in MR*; /media/richard/camcan/bin/hcp-tractography/mrtrix3-python/warpLoc.sh '/media/richard/camcan/Projects/SpeechTBT/data.11mrtrix' ${f} 'MNI152_T1_1mm_brain' 'mri/brain.mgz' 'data.04mask.localizer.sri_slice' & done
# for f in MR*; /media/richard/camcan/bin/hcp-tractography/mrtrix3-python/warpLoc.sh '/media/richard/camcan/Projects/SpeechTBT/data.11mrtrix' ${f} 'diffusion/nodif.nii.gz' 'mri/brain.mgz' 'data.04mask.localizer.sri_slice' & done

function warp_thresh()
{

3dAllineate                        \
-base            ${targFile}       \
-source          ${i}              \
-prefix          ${o}              \
-master          ${targFile}       \
-1Dmatrix_apply  ${matFile}        \
#-overwrite

fslmaths ${o}     \
-thr    0.05      \
-bin              \
${o%.nii.gz}.bin.nii.gz

rm ${o}
}


cd ${SUBJECTS_DIR}/${subject}

SUBJECTS_DIR=$1
subject=$2
standard=$3
targFile=$4
roiDir=$5

targFile=${SUBJECTS_DIR}/${subject}/${targFile}

targName=$(basename ${targFile})
targName=${targName%.mgz}
targName=${targName%.nii.gz}

logFile=${SUBJECTS_DIR}/${subject}/XFMlog_${standard}.txt
outDir=${SUBJECTS_DIR}/${subject}/$roiDir.${standard}2${targName}
movFile=/usr/share/fsl/data/standard/${standard}.nii.gz
movFile2=${standard}.rs.nii.gz

paramFile=${SUBJECTS_DIR}/${subject}/reg/${standard}2${targName}.param.aff12.1D
matFile=${SUBJECTS_DIR}/${subject}/reg/${standard}2${targName}.mat.aff12.1D

regFileI=reg/${targName}2${standard}.aff12.1D
preFile=${SUBJECTS_DIR}/${subject}/reg/${standard}2${targName}.nii.gz

echo 'OutDir:    ' ${outDir}
echo 'standard:  ' ${standard}
echo 'targFile:  ' ${targFile}
echo 'targName:  ' ${targName}
echo 'regFile:   ' ${matFile}
echo 'wd:        ' $(pwd)

mkdir ${outDir}
mkdir ${SUBJECTS_DIR}/${subject}/reg

if [[ ${targFile} == *.mgz ]]; then
mri_convert ${targFile} ${targFile%.mgz}.nii.gz
targFile=${targFile%.mgz}.nii.gz
fi

if [[ ! -f ${matFile} ]]; then

3dAllineate                       \
-base           ${targFile}       \
-source         ${movFile}        \
-prefix         ${preFile}        \
-master         ${targFile}       \
-1Dmatrix_save  ${matFile}        \
-1Dparam_save   ${paramFile}      \
-overwrite

fi



for f in ${SUBJECTS_DIR}/${subject}/${roiDir}/*; do

bo=${f##*/}
b=${bo%.nii*};
i=${f}
o=${outDir}/${b}.${targName}.nii.gz;


[[  ]]
echo 'IO: ' ${i} ${o};

warp_thresh &


done








#3dresample              \
#-master  ${targFile}     \
#-prefix  ${movFile2}           \
#-input   ${movFile}        \
#-overwrite
##





#mri_vol2vol          \
#--mov    ${i}        \
#--fstarg             \
#--interp nearest     \
#--reg    ${regFile}  \
#--o      ${o}




# 3dAllineate -input /usr/share/fsl/data/standard/MNI152_T1_1mm_brain.nii.gz -prefix test.brain.rs.nii.gz -base mri/brain.nii.gz -master mri/brain.nii.gz -1Dapply reg/MNI152_T1_1mm_brain2brain.aff12.1D



#SUBJECTS_DIR='/home/richard/Desktop/test_annot';
#subject='MR1103';
#standard='MNI152_T1_1mm';
#standard='MNI152_T1_1mm_brain';
#standard='MNI152_T1_1mm_brain_mask_dil';

#bbregister            \
#--s     ${subject}    \
#--mov   ${movFile}    \
#--reg   ${regFile}    \
#--t1                  \
#--init-fsl

#3dAllineate                     \
#-base mri/brain.nii.gz          \
#-input /usr/share/fsl/data/standard/MNI152_T1_1mm_brain.nii.gz \
#-prefix test_brain.nii.gz       \
#-master  mri/brain.nii.gz       \
#-1Dmatrix_save  test_mni_brain2brain



#
## warp MNI to native space
#
#SUBJECTS_DIR='/home/richard/Desktop/test_annot';
#subject='MR1103';
#
#bbregister \
#--s ${subject} \
#--mov /usr/share/fsl/data/standard/MNI152_T1_1mm.nii.gz \
#--reg mni2subT1.dat \
#--init-fsl \
#--t1
#
##--mov /usr/share/fsl/data/standard/MNI152lin_T1_2mm_brain.nii.gz \
#
## fsaverage to subjectspace
#
#for f in mask.localizer/*; do
#b=$(basename $f);
#i=mask.localizer/${b%.nii.gz}.nii.gz;
#o=mask.localizer.nativeT1/${b%.nii.gz}.nativeT1.nii.gz;
#
#echo ${i} ${o};
#
#mri_vol2vol \
#--mov ${i} \
#--fstarg \
#--interp nearest \
#--reg mni2subT1.dat \
#--o ${o}
#
##--reg mni2sub.dat \
#
#done















#
#
#
#
#
#3dresample -master HCP-MMP1.nii.gz \
#           -prefix iy_MR1103_20171120_001_020_Siemens_MPRAGE.rs2HCP.nii \
#            -input iy_MR1103_20171120_001_020_Siemens_MPRAGE.nii
#
#
#
#
#for f in mask.localizer/*; do
#b=$(basename $f);
#ba=${b%.nii.gz}.rs.nii.gz;
#bb=${ba%.rs.nii.gz}.rs.native.nii.gz;
#
#echo mask.localizer/${b} mask.localizer.native/${bb};
#
#3dresample -master HCP-MMP1.nii.gz \
#           -prefix mask.localizer.rs/${ba} \
#           -input mask.localizer/${b}
#
#3dNwarpApply -nwarp iy_MR1103_20171120_001_020_Siemens_MPRAGE.rs2HCP.nii \
#             -master HCP-MMP1.nii.gz \
#             -source mask.localizer.rs/${ba} \
#             -prefix mask.localizer.native/${bb};
#done
#
#
##--targ ${targ} \
##--inv
#
#
###### Masks to Subject Space
##targ=${SUBJECTS_DIR}/fsaverage/fsaverage.HCP-MMP1.nii.gz;
##SUBJECTS_DIR='/home/richard/Desktop/test_annot';
##subject='fsaverage';
## MNI to fsaverage
##for f in mask.localizer/*; do
##b=$(basename $f);
##i=mask.localizer/${b};
##o=mask.localizer.fsaverage/${b%.nii.gz}.fsaverage.nii.gz;
#
##echo ${i} ${o};
#
##mri_vol2vol \
##--mov ${i} \
##--interp nearest \
##--reg /usr/local/freesurfer/average/mni152.register.dat \
##--fstarg \
##--o ${o}
##done
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
#
#
#
#
#
#
#
#tkregister2 \
#--mov ${i} \
#--targ ${o} \
#--reg /usr/local/freesurfer/average/mni152.register.dat
#
###### HCP-MMP1 to MNI Space
#
##targ=${SUBJECTS_DIR}/fsaverage/fsaverage.HCP-MMP1.nii.gz;
#SUBJECTS_DIR='/home/richard/Desktop/test_annot';
#subject='fsaverage';
#
#f=HCP-MMP1.nii.gz;
#b=$(basename $f);
#
#o=mask.localizer.fsaverage/${b%.nii.gz}.fsaverage.nii.gz;
#
#mri_vol2vol \
#--mov ${i} \
#--o ${o} \
#--interp nearest \
#--reg /usr/local/freesurfer/average/mni152.register.dat \
#--fstarg
