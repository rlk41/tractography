#!/usr/bin/env bash


# Run your mrtrix job
#inDir='/media/richard/camcan/Projects/SpeechTBT/data.10working'
#outDir='/media/richard/camcan/Projects/SpeechTBT/data.11mrtrix'


#for f in MR*; do /media/richard/camcan/Projects/SpeechTBT/mrtrix3-python/local_mrtrix_python.sh ${f} ${inDir} ${outDir}; done



subID=$1
inDir=$2
outDir=$3

echo "SubID: $subID"
echo "inDir: $inDir"
echo "outDir: $outDir"


python '/media/richard/camcan/bin/hcp-tractography/mrtrix3-python/mrtrix3.py' \
--subNum     "$subID" \
--subsDir    "$outDir" \
--bvals      "$inDir/$subID/diffusion/bvals" \
--bvecs      "$inDir/$subID/diffusion/bvecs" \
--data       "$inDir/$subID/diffusion/data.nii.gz" \
--nodif      "$inDir/$subID/diffusion/nodif_brain_mask.nii.gz" \
--aparc_aseg "$inDir/$subID/mri/aparc.a2009s+aseg.nii.gz" \
--T1         "$inDir/$subID/mri/T1.nii.gz" \
--fsdefault  "/usr/local/mrtrix3/share/mrtrix3/labelconvert/fs_default.txt"  \
--FScolorLUT "/usr/local/freesurfer/FreeSurferColorLUT.txt"




exit 0