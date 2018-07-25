

def _mrconvert2(self):
    self.print_time()
    os.chdir(self.mrtrix3Dir)
    self.log('Running _mrconvert2: ')
    t = Template('mrconvert $_WM_FODs - -coord 3 0 | mrcat $_CSF $_GM - $_tissueRGB -axis 3')
    c=t.substitute(_WM_FODs=self._WM_FODs, _CSF=self._CSF, _GM=self._GM, _tissueRGB=self._tissueRGB)
    output, error = self.run_command(c)
    self.log(output)
    self.log(error)



# Glasser
# if directly from python node, convert to mif
mrconvert Glasser-Localizer.nii.gz nodes_Glasser-Localizer.mif

tck2connectome \
    ./mrtrix3/10M_SIFT.tck \
    ./mrtrix3/mifs/nodes_Glasser-Localizer.mif \
    ./connectome_Glasser-Localizer -out_assignments \
    ./out_assign_Glasser-Localizer -force

connectome2tck \
    ./mrtrix3/10M_SIFT.tck \
    ./out_assign_Glasser-Localizer \
    ./streamlines_all_Glasser-Localizer/


# Glasser.bin
# if directly from python node, convert to mif
mrconvert mask.localizer-Glasser.bin/Glasser-Localizer.bin.nii.gz \
    mask.localizer-Glasser.bin/nodes_Glasser-Localizer.mif

tck2connectome \
    ./mrtrix3/10M_SIFT.tck \
    ./mask.localizer-Glasser.bin/nodes_Glasser-Localizer.mif \
    ./connectome_Glasser-Localizer_bin.csv -zero_diagonal \
    -out_assignments ./out_assign_Glasser-Localizer_bin -force

connectome2tck \
    ./mrtrix3/10M_SIFT.tck \
                    ./out_assign_Glasser-Localizer_bin \
                    ./streamlines_all_Glasser-Localizer_bin/



# Glasser.bin.fix
# if directly from python node, convert to mif
mrconvert mask.localizer-Glasser.bin.fix/Glasser-Localizer.bin.fix.nii.gz \
    mask.localizer-Glasser.bin.fix/nodes_Glasser-Localizer.bin.fix.mif

tck2connectome \
    ./mrtrix3/10M_SIFT.tck \
                    ./mask.localizer-Glasser.bin.fix/nodes_Glasser-Localizer.bin.fix.mif \
                    ./connectome_Glasser-Localizer_bin_fix.csv -zero_diagonal \
                -out_assignments ./out_assign_Glasser-Localizer_bin_fix -force

connectome2tck \
    ./mrtrix3/10M_SIFT.tck \
                    ./out_assign_Glasser-Localizer_bin \
                    ./streamlines_all_Glasser-Localizer_bin/

