#!/usr/bin/env bash


subID=MR1103
inDir=/home/richard/Desktop/test_annot
outDir=${inDir}/${subID}_out


python '/media/richard/camcan/bin/hcp-tractography/mrtrix3-python/mrtrix3.py' \
--subNum     "$subID" \
--subsDir    "$outDir" \
--bvals      "$inDir/$subID/diffusion/bvals" \
--bvecs      "$inDir/$subID/diffusion/bvecs" \
--data       "$inDir/$subID/diffusion/data.nii.gz" \
--nodif      "$inDir/$subID/diffusion/nodif_brain_mask.nii.gz" \
--aparc_aseg "$inDir/$subID/HCP-MMP1.nii.gz" \
--T1         "$inDir/$subID/mri/T1w_acpc_dc_restore_brain.nii.gz" \
--fsdefault  "/usr/local/mrtrix3/share/mrtrix3/labelconvert/fs_default.txt"  \
--FScolorLUT "/home/richard/Desktop/HCP-MMP1_LUT.txt"


#### Prepare Parcellation

labelconvert HCP-MMP1.nii.gz /home/richard/Desktop/HCP-MMP1_LUT \
/home/richard/Desktop/HCP-MMP1_LUT_default \
./mrtrix3/mifs/nodes_HCP-MMP1.mif -force


labelsgmfix ./mrtrix3/mifs/nodes_HCP-MMP1.mif                  \
$inDir/$subID/mri/T1w_acpc_dc_restore_brain.nii.gz             \
/home/richard/Desktop/HCP-MMP1_LUT_default \
./mrtrix3/mifs/nodes_HCP-MMP1_fix.mif -premasked -force


tck2connectome ./mrtrix3/10M_SIFT.tck \
./mrtrix3/mifs/nodes_HCP-MMP1_fix.mif \
./connectome_HCP-MMP1 -out_assignments ./out_assign -force

##################
connectome2tck -exclusive -nodes 24,175,125,173,124,128,129,130,176,51,52,53,9,10,40,204,355,305,353,304,308,309,310,356,231,232,233,189,190,220 \
./mrtrix3/10M_SIFT.tck \
./out_assign \
./streamlines_exclusive_handpicked/HCP-MMP1_streamlines_exclusive_handpicked
#-exemplars ./mrtrix3/mifs/nodes_HCP-MMP1_fix.mif \

connectome2tck -exclusive \
./mrtrix3/10M_SIFT.tck \
./out_assign \
./streamlines_all/HCP-MMP1_all



A1,A4,A5,MBelt,PBelt     STSda,STSdp,STSvp,STSva,   1,2,3a,3b,FEF,24dd
24,175,125,173,124       128,129,130,176,           51,52,53,9,10,40
204,355,305,353,304      308,309,310,356,           231,232,233,189,190,220

24,175,125,173,124,128,129,130,176,51,52,53,9,10,40,204,355,305,353,304,308,309,310,356,231,232,233,189,190,220


137,133,330,148,176,151,128,130,208,40,129,286,173,144,115,320,116,331,106,289,167,317,107,105,125,99,132,220,109,138,95,177,150,139,136,117,188,8,149,55,163,145,113,147,124,276,102,235,319,18,234,175,157,104,100,347,212,168,112,24,174,114,108,25 \
1137,1133,2150,1148,1176,1151,1128,1130,2028,1040,1129,2106,1173,1144,1115,2140,1116,2151,1106,2109,1167,2137,1107,1105,1125,1099,1132,2040,1109,1138,1095,1177,1150,1139,1136,1117,2008,1008,1149,1055,1163,1145,1113,1147,1124,2096,1102,2055,2139,1018,2054,1175,1157,1104,1100,2167,2032,1168,1112,1024,1174,1114,1108,1025 \



for f in masks/*; do
b=$(basename $f);
i=masks/${b};
o=meshes/${b%.nii.gz}.obj;

echo ${i} ${o};

label2mesh ${i} ${o} -force

done



tckedit ./mrtrix3/10M_SIFT.tck -num 200000 ./mrtrix3/200K_SIFT.tck


fod2fixel ./mrtrix3/mifs/WM_FODs.mif \
./mrtrix3/fixel -afd afd.mif -disp dispersion.mif

mrthreshold ./mrtrix3/fixel/afd.mif -abs 0.1 ./mrtrix3/fixel/afd_mask.mif
mrstats -output mean -mask ./mrtrix3/fixel/afd_mask.mif ./mrtrix3/fixel/dispersion.mif


tckconvert tracks.tck track-[].txt

##########



labelconvert HCP-MMP1.nii.gz /home/richard/Desktop/HCP-MMP1_LUT \
/home/richard/Desktop/HCP-MMP1_LUT_default \
./mrtrix3/mifs/nodes_HCP-MMP12.mif -force


labelsgmfix ./mrtrix3/mifs/nodes_HCP-MMP12.mif                  \
$inDir/$subID/mri/T1w_acpc_dc_restore_brain.nii.gz             \
/home/richard/Desktop/HCP-MMP1_LUT_default2 \
./mrtrix3/mifs/nodes_HCP-MMP1_fix2.mif -premasked -force


tck2connectome ./mrtrix3/10M_SIFT.tck \
./mrtrix3/mifs/nodes_HCP-MMP1_fix2.mif \
./connectome_HCP-MMP12 -out_assignments ./out_assign2 -force

##################
connectome2tck -exclusive -nodes 24,175,125,173,124,128,129,130,176,51,52,53,9,10,40,204,355,305,353,304,308,309,310,356,231,232,233,189,190,220 \
./mrtrix3/10M_SIFT.tck \
./out_assign \
./streamlines_exclusive_handpicked/HCP-MMP1_streamlines_exclusive_handpicked
#-exemplars ./mrtrix3/mifs/nodes_HCP-MMP1_fix.mif \

