
# run locally 
#
#subID='MR1106'
#inDir='/media/richard/camcan/pipelines/dti_MRtrix3_pipeline_SpeechTBT'
#outDir='/media/richard/camcan/pipelines/test'
#
#./media/richard/camcan/Projects/SpeechTBT/mrtrix3.sh \
#--subNum     "$subID" \
#--subsDir    "$outDir" \
#--bvals      "$inDir/$subID/diffusion/bvals" \
#--bvecs      "$inDir/$subID/diffusion/bvecs" \
#--data       "$inDir/$subID/diffusion/data.nii.gz" \
#--nodif      "$inDir/$subID/diffusion/nodif_brain_mask.nii.gz" \
#--aparc_aseg "$inDir/$subID/mri/aparc.a2009s+aseg.nii.gz" \
#--T1         "$inDir/$subID/mri/T1.nii.gz" \
#--fsdefault  "/usr/local/mrtrix3/share/mrtrix3/labelconvert/fs_default.txt"  \
#--FScolorLUT "/usr/local/freesurfer/FreeSurferColorLUT.txt"

#subID='MR1106'
#inDir='/isilon/scratch/rlk41/data03'
#outDir='/isilon/scratch/rlk41/test'
#
#subNum=     "$subID" 
#subsDir=    "$outDir" 
#bvals=      "$inDir/$subID/diffusion/bvals" 
#bvecs=      "$inDir/$subID/diffusion/bvecs" 
#arg_data=       "$inDir/$subID/diffusion/data.nii.gz" 
#arg_nodif=      "$inDir/$subID/diffusion/nodif_brain_mask.nii.gz" 
#arg_aparc_aseg= "$inDir/$subID/mri/aparc.a2009s+aseg.nii.gz"
#arg_T1=         "$inDir/$subID/mri/T1.nii.gz" 
#arg_fsdefault=  "/share/apps/mrtrix/mrtrix3/share/mrtrix3/labelconvert/fs_default.txt" 
#arg_FScolorLUT= "/share/apps/freesurfer/6.0.0/FreeSurferColorLUT.txt"



POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    --subNum)
    subNum="$2"
    shift # past argument
    shift # past value
    ;;
    --subsDir)
    arg_subsDir="$2"
    shift # past argument
    shift # past value
    ;;
    --bvals)
    arg_bvals="$2"
    shift # past argument
    shift # past value
    ;;
    --bvecs)
    arg_bvecs="$2"
    shift # past argument
    shift # past value
    ;;
    --data)
    arg_data="$2"
    shift # past argument
    shift # past value
    ;;
    --nodif)
    arg_nodif="$2"
    shift # past argument
    shift # past value
    ;;
    --aparc_aseg)
    arg_aparc_aseg="$2"
    shift # past argument
    shift # past value
    ;;
    --T1)
    arg_T1="$2"
    shift # past argument
    shift # past value
    ;;
    --fsdefault)
    arg_fsdefault="$2"
    shift # past argument
    shift # past value
    ;;
    --FScolorLUT)
    arg_FScolorLUT="$2"
    shift # past argument
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

#subNum="${subNum}"
#subsDir="${arg_subsDir}"
#bvals="${arg_bvals}"
#bvecs="${arg_bvecs}"
#data="${arg_data}"
#nodif="${arg_nodif}"
#aparc_aseg="${arg_aparc_aseg}"
#T1="${arg_T1}"
#fsdefault="${arg_fsdefault}"
#FScolorLUT="${arg_FScolorLUT}"

#subNum="${subNum}"
#echo subsDir    		= "${arg_subsDir}"
#echo bvals			= "${arg_bvals}"
#echo bvecs         		= "${arg_bvecs}"
#echo arg_data  			= "${arg_data}"
#echo arg_nodif   		= "${arg_nodif}"
#echo arg_aparc_aseg   		= "${arg_aparc_aseg}"
#echo arg_T1   			= "${arg_T1}"
#echo arg_fsdefault   		= "${arg_fsdefault}"
#echo arg_FScolorLUT   		= "${arg_FScolorLUT}"

subID="${subNum}"
mainDir="${arg_subsDir}"
_fsdefault="${arg_fsdefault}"
_FScolorLUT="${arg_FScolorLUT}"



tmpDir="${mainDir}"/"${subID}"; 		
mkdir "${tmpDir}"; 
mkdir "${tmpDir}"/"${mrtrix3}"; 

cd "${tmpDir}"; 


_acpc=$tmpDir'/T1.nii.gz';
_aparc_aseg=$tmpDir'/aparc.a2009s+aseg.nii.gz';
_nodif=$tmpDir'/nodif_brain_mask.nii.gz';
_data=$tmpDir'/data.nii.gz';
_bvals=$tmpDir'/bvals';
_bvecs=$tmpDir'/bvecs';



cp "${arg_bvals}" 	"${_bvals}"
cp "${arg_bvecs}" 	"${_bvecs}"
cp "${arg_data}"	"${_data}"
cp "${arg_nodif}"	"${_nodif}"
cp "${arg_aparc_aseg}"	"${_aparc_aseg}"
cp "${arg_T1}"		"${_acpc}"




_5TT=$tmpDir'/mrtrix3/5TT.mif';
_vis=$tmpDir'/mrtrix3/viz.mif';
_nodesmif=$tmpDir'/mrtrix3/nodes.mif';
_nodes_fixSGM=$tmpDir'/mrtrix3/nodes_fixSGM.mif';
_DWI=$tmpDir'/mrtrix3/DWI.mif';
_meanb0=$tmpDir'/mrtrix3/meanb0.mif'; 
_RF_vox=$tmpDir'/mrtrix3/RF_voxels.mif';
_WM_FODs=$tmpDir'/mrtrix3/WM_FODs.mif';

_RF_WM=$tmpDir'/mrtrix3/RF_WM.txt';
_RF_GM=$tmpDir'/mrtrix3/RF_GM.txt'; 
_RF_CSF=$tmpDir'/mrtrix3/RF_CSF.txt'; 
_GM=$tmpDir'/mrtrix3/GM.mif';
_CSF=$tmpDir'/mrtrix3/CSF.mif';
_tissueRGB=$tmpDir'/mrtrix3/tissueRGB.mif';
_100M=$tmpDir'/mrtrix3/100M.tck';
_10M_SIFT=$tmpDir'/mrtrix3/10M_SIFT.tck'; 

_connectome=$tmpDir'/connectome.csv';


5ttgen fsl $_acpc $_5TT -premasked
5tt2vis $_5TT $_vis;
#mrview $_vis;
labelconvert $_aparc_aseg $_FScolorLUT $_fsdefault $_nodesmif
labelsgmfix $_nodesmif $_acpc $_fsdefault $_nodes_fixSGM -premasked
mrconvert $_data $_DWI -fslgrad $_bvecs $_bvals -datatype float32 -stride 0,0,0,1
dwiextract $_DWI - -bzero | mrmath - mean $_meanb0 -axis 3

dwi2response msmt_5tt $_DWI $_5TT $_RF_WM $_RF_GM $_RF_CSF -voxels $_RF_vox 
#couldnt check 5tt 
#mrview $_meanb0 -overlay.load $_RF_vox -overlay.opacity 0.5
dwi2fod msmt_csd $_DWI $_RF_WM $_WM_FODs $_RF_GM $_GM $_RF_CSF $_CSF -mask $_nodif

mrconvert $_WM_FODs - -coord 3 0 | mrcat $_CSF $_GM - $_tissueRGB -axis 3
#mrview $_tissueRGB -odf.load_sh $_WM_FODs

tckgen $_WM_FODs $_100M -act $_5TT -backtrack -crop_at_gmwmi -seed_dynamic $_WM_FODs -maxlength 250 -select 100M -cutoff 0.06

tcksift $_100M $_WM_FODs $_10M_SIFT -act $_5TT -term_number 10M

#adjust for RAM 
#mrresize WM_FODs.mif FOD_downsampled.mif -scale 0.5 -interp sinc
#tckedit 100M.tck 50M.tck -number 50M

tck2connectome $_10M_SIFT $_nodes_fixSGM $_connectome




