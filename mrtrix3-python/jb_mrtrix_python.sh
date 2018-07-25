
#!/bin/bash
#$ -cwd
#$ -j y
#$ -m e -M rlk41@georgetown.edu
#$ -l h_rt=300:00:00
#$ -l h_vmem=3G




# Set up proper modules.
. /etc/profile

#python2 v python3 may conflict fsl fs 
module load anaconda2
module load mrtrix3
module load fsl
module load freesurfer
module list


# In case the job is for the smp PE
if [ ! $NSLOTS ]; then
  NSLOTS=1
fi

export OMP_NUM_LIMIT=$NSLOTS
 
echo "Got $NSLOTS slots running on" `hostname`


# Run your mrtrix job
#inDir='/isilon/scratch/rlk41/data03'
#outDir='/isilon/scratch/rlk41/test2-mrtrix'
#subPaths=$1
#subID=$(basename ${subPaths[$SGE_TASK_ID-1]})

subID=$1
inDir=$2
outDir=$3

echo "SubID: $subID"
echo "inDir: $inDir" 
echo "outDir: $outDir" 


python '/home/rlk41/bin/mrtrix3-python/mrtrix3.py' \
--subNum     "$subID" \
--subsDir    "$outDir" \
--bvals      "$inDir/$subID/diffusion/bvals" \
--bvecs      "$inDir/$subID/diffusion/bvecs" \
--data       "$inDir/$subID/diffusion/data.nii.gz" \
--nodif      "$inDir/$subID/diffusion/nodif_brain_mask.nii.gz" \
--aparc_aseg "$inDir/$subID/mri/aparc.a2009s+aseg.nii.gz" \
--T1         "$inDir/$subID/mri/norm.dti.nii.gz" \
--fsdefault  "/share/apps/mrtrix/mrtrix3/share/mrtrix3/labelconvert/fs_default.txt"  \
--FScolorLUT "/share/apps/freesurfer/6.0.0/FreeSurferColorLUT.txt"


#--T1         "$inDir/$subID/mri/T1.nii.gz" \


exit 0

# inDir='/isilon/scratch/rlk41/speechTBT'
# outDir='/isilon/scratch/rlk41/speechTBT-mrtrix'
# declare -a m=("MR1103" "MR1106" "MR1108" "MR1112" "MR1126" "MR1133" "MR1134" "MR1135" "MR1136" "MR1137" "MR1139" "MR1140" "MR1141" "MR1142" "MR1144" "MR1145" "MR1146" "MR1150" "MR1151" "MR1153" "MR1154" "MR1155" "MR1157" "MR1162")
# declare -a m=("MR1106" "MR1108" "MR1112" "MR1126" "MR1133" "MR1134" "MR1135" "MR1136" "MR1137" "MR1139" "MR1140" "MR1141" "MR1142" "MR1144" "MR1145" "MR1146" "MR1150" "MR1151" "MR1153" "MR1154" "MR1155" "MR1157" "MR1162")
# for i in ${m[@]}; do qsub -pe smp 20 /home/rlk41/bin/mrtrix3-python/jb_mrtrix_python.sh $i $inDir $outDir; done

#qsub -pe smp 20 /home/rlk41/bin/mrtrix3-python/jb_mrtrix_python.sh MR1103 ${inDir} ${outDir}




# qdel 131406 131405