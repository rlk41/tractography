
#!/bin/bash
#$ -cwd
#$ -j y
#$ -m e -M rlk41@georgetown.edu
#$ -l h_rt=300:00:00
#$ -l h_vmem=5G




# Set up proper modules.
. /etc/profile

#python2 v python3 may conflict fsl fs 
module load anaconda3
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

#subPaths=$1
#subID=$(basename ${subPaths[$SGE_TASK_ID-1]})

subID=$1
inDir='/isilon/scratch/rlk41/data03'
outDir='/isilon/scratch/rlk41/test2-mrtrix'

#echo "Task ID: $SGE_TASK_ID"
echo "SubID: $subID"
echo "inDir: $inDir" 
echo "outDir: $outDir" 


bash /home/rlk41/bin/mrtrix3-bash/mrtrix3.sh \
--subNum     "$subID" \
--subsDir    "$outDir" \
--bvals      "$inDir/$subID/diffusion/bvals" \
--bvecs      "$inDir/$subID/diffusion/bvecs" \
--data       "$inDir/$subID/diffusion/data.nii.gz" \
--nodif      "$inDir/$subID/diffusion/nodif_brain_mask.nii.gz" \
--aparc_aseg "$inDir/$subID/mri/aparc.a2009s+aseg.nii.gz" \
--T1         "$inDir/$subID/mri/T1.nii.gz" \
--fsdefault  "/share/apps/mrtrix/mrtrix3/share/mrtrix3/labelconvert/fs_default.txt"  \
--FScolorLUT "/share/apps/freesurfer/6.0.0/FreeSurferColorLUT.txt"










exit 0

# declare -a m=("MR1103" "MR1106" "MR1126" "MR1134" "MR1135" "MR1136" "MR1137" "MR1139" "MR1140" "MR1142" "MR1144" "MR1145" "MR1146" "MR1150" "MR1151" "MR1153" "MR1154" "MR1155")
# for i in ${m[@]}; do qsub -pe smp 20 /home/rlk41/bin/mrtrix3-bash/jb_mrtrix_bash.sh $i; done 

# qsub -pe smp 20 /home/rlk41/bin/mrtrix3-bash/jb_mrtrix_bash.sh MR1103
