
import os
import sys
import subprocess
import datetime
from string import Template
import shutil
import argparse


#not used... but can be for downloading subject list hcp_1200.txt
#def get_hcp1200_subjects(awsbin):
#    print('Downloading Subject List for HCP_1200')
#    t = Template('$aws s3 ls s3://hcp-openaccess/HCP_1200/')
#    c=t.substitute(aws=awsbin)
#    output, error = run_command(c)
#    return(output, error)


class mrtrix3(object):
    def __init__(self, subNum, subsDir, bvals, bvecs, T1, nodif, data, aparc_aseg, fsdefault, FScolorLUT):

        self.arg_bvals          = bvals
        self.arg_bvecs          = bvecs
        self.arg_T1             = T1
        self.arg_nodif          = nodif
        self.arg_data           = data
        self.arg_aparc_aseg     = aparc_aseg
        self.arg_fsdefault      = fsdefault
        self.arg_FScolorLUT     = FScolorLUT

        self.subID              = subNum
        self.startTime          = datetime.datetime.now()
        self.laststep_time      = datetime.datetime.now()

        self.fsdefault          = self.arg_fsdefault   #'/usr/local/mrtrix3/share/mrtrix3/labelconvert/fs_default.txt'
        self.FScolorLUT         = self.arg_FScolorLUT  #'/media/richard/camcan/pipelines/dti_MRtrix3_pipeline/FreeSurferColorLUT.txt'


        # directories
        self.subsDir            = subsDir
        self.subDir             = os.path.join(self.subsDir, self.subID)
        self.T1wDir             = os.path.join(self.subDir, 'mri')
        self.diffDir            = os.path.join(self.subDir, 'diffusion')
        self.mrtrix3Dir         = os.path.join(self.subDir, 'mrtrix3')
        self.mifDir             = os.path.join(self.subDir, 'mrtrix3', 'mifs')

        # environment, PATHs, where is mrtrix, fsl installed
        # need for Popen
        self.env                = {}

        # log file
        self.log_file           = os.path.join(self.subDir, 'log.txt')

        # raw files to download from HCP
        self.T1                 = os.path.join(self.subDir, 'mri', 'T1.nii.gz')
        self.aparc_aseg         = os.path.join(self.subDir, 'mri', 'aparc+aseg.nii.gz')
        self.nodif_brain_mask   = os.path.join(self.subDir, 'diffusion', 'nodif_brain_mask.nii.gz')
        self.data               = os.path.join(self.subDir, 'diffusion', 'data.nii.gz')
        self.bvals              = os.path.join(self.subDir, 'diffusion', 'bvals')
        self.bvecs              = os.path.join(self.subDir, 'diffusion', 'bvecs')

        # files to be created
        self._5TT               = os.path.join(self.subDir, 'mrtrix3', 'mifs', '5TT.mif')
        self._vis               = os.path.join(self.subDir, 'mrtrix3', 'mifs', 'viz.mif')
        self._nodesmif          = os.path.join(self.subDir, 'mrtrix3', 'mifs', 'nodes.mif')
        self._nodes_fixSGM      = os.path.join(self.subDir, 'mrtrix3', 'mifs', 'nodes_fixSGM.mif')
        self._DWI               = os.path.join(self.subDir, 'mrtrix3', 'mifs', 'DWI.mif')
        self._meanb0            = os.path.join(self.subDir, 'mrtrix3', 'mifs', 'meanb0.mif')
        self._RF_vox            = os.path.join(self.subDir, 'mrtrix3', 'mifs', 'RF_voxels.mif')
        self._WM_FODs           = os.path.join(self.subDir, 'mrtrix3', 'mifs', 'WM_FODs.mif')
        self._RF_WM             = os.path.join(self.subDir, 'mrtrix3', 'mifs', 'RF_WM.txt')
        self._RF_GM             = os.path.join(self.subDir, 'mrtrix3', 'mifs', 'RF_GM.txt')
        self._RF_CSF            = os.path.join(self.subDir, 'mrtrix3', 'mifs', 'RF_CSF.txt')
        self._GM                = os.path.join(self.subDir, 'mrtrix3', 'mifs', 'GM.mif')
        self._CSF               = os.path.join(self.subDir, 'mrtrix3', 'mifs', 'CSF.mif')
        self._tissueRGB         = os.path.join(self.subDir, 'mrtrix3', 'mifs', 'tissueRGB.mif')

        self._100M              = os.path.join(self.subDir, 'mrtrix3', '100M.tck')
        self._10M_SIFT          = os.path.join(self.subDir, 'mrtrix3', '10M_SIFT.tck')

        self._connectome        = os.path.join(self.subDir, 'connectome.csv')

        #completed steps
        self.download_status            = 0
        self._5ttgen_status             = 0
        self._5tt2vis_status            = 0
        self._labelconvert_status       = 0
        self._labelsgmfix_status        = 0
        self._mrconvert1_status         = 0
        self._dwiextract_status         = 0
        self._dwi2response_status       = 0
        self._dwi2fod_status            = 0
        self._mrconvert2_status         = 0
        self._tckgen_status             = 0
        self._tcksift_status            = 0
        self._tck2connectome_status     = 0


    def run_command(self, command):
        p = subprocess.Popen(command.split(), stdout=subprocess.PIPE, env=self.env)
        output, error = p.communicate()
        return(output,error)

    def print_time(self):
        now_time                = datetime.datetime.now()
        total_time              = now_time - self.startTime
        laststep_totaltime      = now_time - self.laststep_time
        self.laststep_time      = now_time

        self.log('Total Time: {} \nLast Step:  {}'.format(total_time, laststep_totaltime) )

    # not currently used
    def which_location(self, file):
        command = 'which ' + file
        p = subprocess.Popen(command.split(), stdout=subprocess.PIPE, env=self.env)
        output, error = p.communicate()
        return output[0]

    def log(self, text):
        try:
            text = text.splitlines()
            for line in text:
                print(line)
                with open(self.log_file, 'a') as file:
                    file.write('{}\n'.format(line))
        except:
            print(text)


    def checkenv(self):
        self.print_time()

        self.log('Loading $PATH from environment')

        self.env = os.environ.copy()

        #self.env["PATH"]            = "/home/richard/anaconda3/bin:"    + self.env["PATH"]
        #self.env["PATH"]            = "/usr/local/freesurfer/bin:"      + self.env["PATH"]
        #self.env["PATH"]            = "/usr/share/fsl/5.0/bin:"         + self.env["PATH"]
        #self.env["PATH"]            = "/usr/local/mrtrix3/bin:"         + self.env["PATH"]

        #self.env["PATH"]            = "/usr/local/mrtrix3/lib:"         + self.env["PATH"]
        #self.env["LD_LIBRARY_PATH"] = "/usr/lib/fsl/5.0:"               #+ self.env["LD_LIBRARY_PATH"]

        #self.env["FSLDIR"]          = "/usr/share/fsl/5.0"
        #self.env["FSLOUTPUTTYPE"]   = "NIFTI_GZ"

        #self.fsdefault              = '/usr/local/mrtrix3/share/mrtrix3/labelconvert/fs_default.txt'
        #self.FScolorLUT             = '/media/richard/camcan/pipelines/dti_MRtrix3_pipeline/FreeSurferColorLUT.txt'
        self.fsdefault              = self.arg_fsdefault   #'/usr/local/mrtrix3/share/mrtrix3/labelconvert/fs_default.txt'
        self.FScolorLUT             = self.arg_FScolorLUT  #'/media/richard/camcan/pipelines/dti_MRtrix3_pipeline/FreeSurferColorLUT.txt'


    def initdir(self, force=False):
        # create directories if don't exist

        # if force we delete all directories for subject and recreate

        self.print_time()

        if force and os.path.exists(self.subDir):
            self.log('Deleting and remaking directory for: {}'.format(self.subID))
            shutil.rmtree(self.subDir)
        else:
            self.log('Creating Directories for Subject: {}'.format(self.subID))


        if not os.path.exists(self.subDir):
            os.makedirs(self.subDir)
            self.log('Created Dir: {}'.format(self.subDir))
        else:
            self.log('Exists: {}'.format(self.subDir))

        if not os.path.exists(self.T1wDir):
            os.makedirs(self.T1wDir)
            self.log('Created Dir: {}'.format(self.T1wDir))
        else:
            self.log('Exists: {}'.format(self.T1wDir))

        if not os.path.exists(self.diffDir):
            os.makedirs(self.diffDir)
            self.log('Created Dir: {}'.format(self.diffDir))
        else:
            self.log('Exists: {}'.format(self.diffDir))

        if not os.path.exists(self.mrtrix3Dir):
            os.makedirs(self.mrtrix3Dir)
            self.log('Created Dir:  {}'.format(self.mrtrix3Dir))
        else:
            self.log('Exists: {}'.format(self.mrtrix3Dir))

        if not os.path.exists(self.mifDir):
            os.makedirs(self.mifDir)
            self.log('Created Dir: {}'.format(self.mifDir))
        else:
            self.log('Exists: {}'.format(self.mifDir))



    def getFiles_local(self, force=False):
        from shutil import copyfile


        self.print_time()
        self.log('Setting Files for Subject: '.format(self.subID))

        if force:
            self.log('Forcing Copy...')


        # bvals
        if not os.path.isfile(self.bvals) or force:
            self.log('Force: {} Copying: {}'.format(force, self.bvals))
            copyfile(self.arg_bvals, self.bvals)

        else:
            self.log('Exists: '.format(self.bvals))

        # bvecs
        if not os.path.isfile(self.bvecs)or force:
            self.log('Force: {} Copying: {}'.format(force, self.bvecs))
            copyfile(self.arg_bvecs, self.bvecs)


        else:
            self.log('Exists: '.format(self.bvecs))

        # data.nii.gz
        if not os.path.isfile(self.data)or force:
            self.log('Force: {} Copying: {}'.format(force, self.data))
            copyfile(self.arg_data, self.data)

        else:
            self.log('Exists: '.format(self.data))

        # nodif_brain_mask
        if not os.path.isfile(self.nodif_brain_mask) or force:
            self.log('Force: {} Copying: {}'.format(force, self.nodif_brain_mask))
            copyfile(self.arg_nodif, self.nodif_brain_mask)

        else:
            self.log('Exists: '.format(self.nodif_brain_mask))

        # T1
        if not os.path.isfile(self.T1) or force:
            self.log('Force: {} Copying: {}'.format(force, self.T1))
            copyfile(self.arg_T1, self.T1)

        else:
            self.log('Exists: '.format(self.T1))

        # aparc+aseg
        if not os.path.isfile(self.aparc_aseg) or force:
            self.log('Force: {} Copying: {}'.format(force, self.aparc_aseg))
            copyfile(self.arg_aparc_aseg, self.aparc_aseg)


        else:
            self.log('Exists: '.format(self.aparc_aseg))

        self.download_status = 1


    def getFiles_aws(self, force=False):
        # requires you to have run "aws configure" and provided
        # AccessKey and SecretAccessKey

        self.print_time()
        self.log('Downloading Files for Subject: '.format(self.subID))

        if force:
            self.log('Forcing Downloads...')

        t = Template('aws s3 cp s3://hcp-openaccess/HCP_1200/$sub$fromLoc $toLoc')

        # bvals
        if not os.path.isfile(self.bvals) or force:
            self.log('Force: {} Downloading: {}'.format(force, self.bvals))
            c=t.substitute(sub=self.subID, fromLoc='/T1w/Diffusion/bvals', toLoc=self.bvals)
            output, error = self.run_command(c)
            self.log(output)
            self.log(error)

        else:
            self.log('Exists: '.format(self.bvals))

        # bvecs
        if not os.path.isfile(self.bvecs)or force:
            self.log('Force: {} Downloading: {}'.format(force, self.bvecs))
            c=t.substitute(sub=self.subID, fromLoc='/T1w/Diffusion/bvecs', toLoc=self.bvecs)
            output, error = self.run_command(c)
            self.log(output)
            self.log(error)

        else:
            self.log('Exists: '.format(self.bvecs))

        # data.nii.gz
        if not os.path.isfile(self.data)or force:
            self.log('Force: {} Downloading: {}'.format(force, self.data))
            c=t.substitute(sub=self.subID, fromLoc='/T1w/Diffusion/data.nii.gz', toLoc=self.data)
            output, error = self.run_command(c)
            self.log(output)
            self.log(error)

        else:
            self.log('Exists: '.format(self.data))

        # nodif_brain_mask
        if not os.path.isfile(self.nodif_brain_mask) or force:
            self.log('Force: {} Downloading: {}'.format(force, self.nodif_brain_mask))
            c=t.substitute(sub=self.subID, fromLoc='/T1w/Diffusion/nodif_brain_mask.nii.gz', toLoc=self.nodif_brain_mask)
            output, error = self.run_command(c)
            self.log(output)
            self.log(error)

        else:
            self.log('Exists: '.format(self.nodif_brain_mask))

        # acpc
        if not os.path.isfile(self.T1) or force:
            self.log('Force: {} Downloading: {}'.format(force, self.T1))
            c=t.substitute(sub=self.subID, fromLoc='/T1w/T1w_acpc_dc_restore_brain.nii.gz', toLoc=self.T1)
            output, error = self.run_command(c)
            self.log(output)
            self.log(error)

        else:
            self.log('Exists: '.format(self.T1))

        # aparc+aseg
        if not os.path.isfile(self.aparc_aseg) or force:
            self.log('Force: {} Downloading: {}'.format(force, self.aparc_aseg))
            c=t.substitute(sub=self.subID, fromLoc='/T1w/aparc+aseg.nii.gz', toLoc=self.aparc_aseg)
            output, error = self.run_command(c)
            self.log(output)
            self.log(error)

        else:
            self.log('Exists: '.format(self.aparc_aseg))

        self.download_status = 1

    def _5ttgen(self):
        self.print_time()
        os.chdir(self.mrtrix3Dir)
        self.log('Running _5ttgen: ')
        #t = Template('5ttgen fsl $acpc $_5TT')
        t = Template('5ttgen fsl $acpc $_5TT -premasked')
        c=t.substitute(acpc=self.T1, _5TT=self._5TT)
        output, error = self.run_command(c)
        self.log(output)
        self.log(error)
        return output, error

    def _5tt2vis(self):
        self.print_time()
        os.chdir(self.mrtrix3Dir)
        self.log('Running _5tt2vis: ')
        t = Template('5tt2vis $_5TT $_vis')
        c=t.substitute(_5TT=self._5TT, _vis=self._vis)
        output, error = self.run_command(c)
        self.log(output)
        self.log(error)
        return output, error

    def _labelconvert(self):
        self.print_time()
        os.chdir(self.mrtrix3Dir)
        self.log('Running _labelconvert: ')
        t = Template('labelconvert $_aparc_aseg $_FScolorLUT $_fsdefault $_nodesmif')
        c=t.substitute(_aparc_aseg=self.aparc_aseg, _FScolorLUT=self.FScolorLUT, _fsdefault=self.fsdefault, _nodesmif=self._nodesmif)
        output, error = self.run_command(c)
        self.log(output)
        self.log(error)
        return output, error

    def _labelsgmfix(self):
        self.print_time()
        os.chdir(self.mrtrix3Dir)
        self.log('Running _labelsgmfix: ')
        t = Template('labelsgmfix $_nodesmif $_acpc $_fsdefault $_nodes_fixSGM -premasked')
        c=t.substitute(_nodesmif=self._nodesmif, _acpc=self.T1, _fsdefault=self.fsdefault, _nodes_fixSGM=self._nodes_fixSGM)
        output, error = self.run_command(c)
        self.log(output)
        self.log(error)
        return output, error

    def _mrconvert1(self):
        self.print_time()
        os.chdir(self.mrtrix3Dir)
        self.log('Running _mrconvert1: ')
        t = Template('mrconvert $_data $_DWI -fslgrad $_bvecs $_bvals -datatype float32 -stride 0,0,0,1')
        c=t.substitute(_data=self.data, _DWI=self._DWI, _bvecs=self.bvecs, _bvals=self.bvals)
        output, error = self.run_command(c)
        self.log(output)
        self.log(error)
        return output, error

    def _dwiextract(self):
        self.print_time()
        os.chdir(self.mrtrix3Dir)
        self.log('Running _dwiextract: ')
        t = Template('dwiextract $_DWI - -bzero | mrmath - mean $_meanb0 -axis 3')
        c=t.substitute(_DWI=self._DWI, _meanb0=self._meanb0)
        output, error = self.run_command(c)
        self.log(output)
        self.log(error)
        return output, error

    def _dwi2response(self):
        self.print_time()
        os.chdir(self.mrtrix3Dir)
        self.log('Running _dwi2response: ')
        #t = Template('dwi2response msmt_5tt $_DWI $_5TT $_RF_WM $_RF_GM $_RF_CSF -voxels $_RF_vox')
        t = Template('dwi2response dhollander $_DWI $_RF_WM $_RF_GM $_RF_CSF -voxels $_RF_vox')

        c=t.substitute(_DWI=self._DWI, _5TT=self._5TT, _RF_WM=self._RF_WM, _RF_GM=self._RF_GM, _RF_CSF=self._RF_CSF, _RF_vox=self._RF_vox)
        output, error = self.run_command(c)
        self.log(output)
        self.log(error)
        return output, error

    def _dwi2fod(self):
        self.print_time()
        os.chdir(self.mrtrix3Dir)
        self.log('Running _dwi2fod: ')
        t = Template('dwi2fod msmt_csd $_DWI $_RF_WM $_WM_FODs $_RF_GM $_GM $_RF_CSF $_CSF -mask $_nodif')
        c=t.substitute(_DWI=self._DWI, _RF_WM=self._RF_WM, _WM_FODs=self._WM_FODs, _RF_GM=self._RF_GM, _GM=self._GM, _RF_CSF=self._RF_CSF, _CSF=self._CSF, _nodif=self.nodif_brain_mask)
        output, error = self.run_command(c)
        self.log(output)
        self.log(error)
        return output, error

    def _mrconvert2(self):
        self.print_time()
        os.chdir(self.mrtrix3Dir)
        self.log('Running _mrconvert2: ')
        t = Template('mrconvert $_WM_FODs - -coord 3 0 | mrcat $_CSF $_GM - $_tissueRGB -axis 3')
        c=t.substitute(_WM_FODs=self._WM_FODs, _CSF=self._CSF, _GM=self._GM, _tissueRGB=self._tissueRGB)
        output, error = self.run_command(c)
        self.log(output)
        self.log(error)
        return output, error

    def _tckgen(self):
        self.print_time()
        os.chdir(self.mrtrix3Dir)
        self.log('Running _tckgen: ')
        t = Template('tckgen $_WM_FODs $_100M -act $_5TT -backtrack -crop_at_gmwmi -seed_dynamic $_WM_FODs -maxlength 250 -select 100M -cutoff 0.06')
        c=t.substitute(_WM_FODs=self._WM_FODs, _100M=self._100M, _5TT=self._5TT)
        output, error = self.run_command(c)
        self.log(output)
        self.log(error)
        return output, error

    def _tcksift(self):
        self.print_time()
        os.chdir(self.mrtrix3Dir)
        self.log('Running _tcksift: ')
        t = Template('tcksift $_100M $_WM_FODs $_10M_SIFT -act $_5TT -term_number 10M')
        c=t.substitute(_100M=self._100M, _WM_FODs=self._WM_FODs, _10M_SIFT=self._10M_SIFT, _5TT=self._5TT)
        output, error = self.run_command(c)
        self.log(output)
        self.log(error)
        return output, error

    def _tck2connectome(self):
        self.print_time()
        os.chdir(self.mrtrix3Dir)
        self.log('Running _tck2connectome: ')
        t = Template('tck2connectome $_10M_SIFT $_nodes_fixSGM $_connectome')
        c=t.substitute(_10M_SIFT=self._10M_SIFT, _nodes_fixSGM=self._nodes_fixSGM, _connectome=self._connectome)
        output, error = self.run_command(c)
        self.log(output)
        self.log(error)
        return output, error

    def print_status(self):
        print('self.download_status {}'.format(self.download_status))
        print('self._5ttgen_status {}'.format(self._5ttgen_status))
        print('self._5tt2vis_status {}'.format(self._5tt2vis_status))
        print('self._labelconvert_status {}'.format(self._labelconvert_status))
        print('self._labelsgmfix_status {}'.format(self._labelsgmfix_status))
        print('self._mrconvert1_status {}'.format(self._mrconvert1_status))
        print('self._dwiextract_status {}'.format(self._dwiextract_status))
        print('self._dwi2response_status {}'.format(self._dwi2response_status))
        print('self._dwi2fod_status {}'.format(self._dwi2fod_status))
        print('self._mrconvert2_status {}'.format(self._mrconvert2_status))
        print('self._tckgen_status {}'.format(self._tckgen_status))
        print('self._tcksift_status {}'.format(self._tcksift_status))
        print('self._tck2connectome_status {}'.format(self._tck2connectome_status))




    # need better flow mgmt
    def run_mrtrix3(self):
        while True:

            self.print_status()

            if self.download_status:
                [o,e] = self._5ttgen()
                print('out: '.format(o))
                print('e: '.format(e))
                if not e:
                    self._5ttgen_status  = 1
                    self.download_status = 0
                    self.log("_5ttgen Status: {}".format(self._5ttgen_status))

                else:
                    self.log("_5ttgen Status: {}".format(self._5ttgen_status))
                    self.log('FAILED')
                    break



            if self._5ttgen_status:
                [o, e] = self._5tt2vis()
                print('out: '.format(o))
                print('e: '.format(e))
                if not e:
                    self._5tt2vis_status = 1
                    self._5ttgen_status  = 0
                    self.log("_5tt2vis Status: {}".format(self._5tt2vis_status))

                else:
                    self.log("_5tt2vis Status: {}".format(self._5tt2vis_status))
                    self.log('FAILED')
                    break


            # if self._5tt2vis_status:
            #     try:
            #         self._labelconvert()
            #         self._labelconvert_status = 1
            #     except:
            #         self.log(sys.exc_info()[0])
            #         raise
            #     self.log("_labelconvert Status: {}".format(self._labelconvert_status))
            # else:
            #     self.log('broke')
            #     break
            #
            # if self._labelconvert_status:
            #     try:
            #         self._labelsgmfix()
            #         self._labelsgmfix_status = 1
            #     except:
            #         self.log(sys.exc_info()[0])
            #         raise
            #     self.log("_labelsgmfix Status: {}".format(self._labelsgmfix_status))
            # else:
            #     self.log('broke')
            #     break

            if self._5tt2vis_status:
                [o,e] = self._mrconvert1()
                print('out: '.format(o))
                print('e: '.format(e))
                if not e:
                    self._mrconvert1_status = 1
                    self._5tt2vis_status    = 0
                    self.log("_mrconvert1 Status: {}".format(self._mrconvert1_status))
                else:
                    self.log("_mrconvert1 Status: {}".format(self._mrconvert1_status))
                    self.log('FAILED')
                    break



            if self._mrconvert1_status:
                [o,e] =  self._dwiextract()
                print('out: '.format(o))
                print('e: '.format(e))
                if not e:
                    self._dwiextract_status = 1
                    self._mrconvert1_status = 0
                    self.log("_dwiextract Status: {}".format(self._dwiextract_status))
                else:
                    self.log("_dwiextract Status: {}".format(self._dwiextract_status))
                    self.log('FAILED')
                    break



            if self._dwiextract_status:
                [o,e] = self._dwi2response()
                print('out: '.format(o))
                print('e: '.format(e))
                if not e:
                    self._dwi2response_status = 1
                    self._dwiextract_status   = 0
                    self.log("_dwi2response Status: {}".format(self._dwi2response_status))
                else:
                    self.log("_dwi2response Status: {}".format(self._dwi2response_status))
                    self.log('FAILED')
                    break




            if self._dwi2response_status:
                [o,e] = self._dwi2fod()
                print('out: '.format(o))
                print('e: '.format(e))
                if not e:
                    self._dwi2fod_status = 1
                    self._dwi2response_status = 0
                    self.log("_dwi2fod Status: {}".format(self._dwi2fod_status))
                else:
                    self.log("_dwi2fod Status: {}".format(self._dwi2fod_status))
                    self.log('FAILED')
                    break




            if self._dwi2fod_status:
                [o,e] = self._mrconvert2()
                print('out: '.format(o))
                print('e: '.format(e))
                if not e:
                    self._mrconvert2_status = 1
                    self._dwi2fod_status    = 0
                    self.log("_mrconvert2 Status: {}".format(self._mrconvert2_status))
                else:
                    self.log("_mrconvert2 Status: {}".format(self._mrconvert2_status))
                    self.log('FAILED')
                    break




            if self._mrconvert2_status:
                [o,e] = self._tckgen()
                print('out: '.format(o))
                print('e: '.format(e))
                if not e:
                    self._tckgen_status = 1
                    self._mrconvert2_status = 0
                    self.log("_tckgen Status: {}".format(self._tckgen_status))
                else:
                    self.log("_tckgen Status: {}".format(self._tckgen_status))
                    self.log('FAILED')
                    break




            if self._tckgen_status:
                [o,e] = self._tcksift()
                print('out: '.format(o))
                print('e: '.format(e))
                if not e:
                    self._tcksift_status = 1
                    self._tckgen_status  = 0
                    self.log("_tcksift Status: {}".format(self._tcksift_status))
                else:
                    self.log("_tcksift Status: {}".format(self._tcksift_status))
                    self.log('FAILED')
                    break




            if self._tcksift_status:
                [o,e] = self._tck2connectome()
                print('out: '.format(o))
                print('e: '.format(e))
                if not e:
                    self._tck2connectome_status = 1
                    self._tcksift_status        = 0
                    self.log("_tck2connectome Status: {}".format(self._tck2connectome_status))
                else:
                    self.log("_tck2connectome Status: {}".format(self._tck2connectome_status))
                    self.log('FAILED')
                    break


            else:


                self.log('Exit')
                self.print_time()
                break

def main():

    # need a premasked option

    parser = argparse.ArgumentParser(description='LLNL DTI pipeline.')
    parser.add_argument('--subNum', type=str,
                        required=True,
                        help='subject number (ex. "100307")')

    parser.add_argument('--subsDir', type=str,
                        required=True,
                        help='directory to build the subject directories in')

    parser.add_argument('--bvals', type=str,
                        required=False,
                        help='location of bvals ')
    parser.add_argument('--bvecs', type=str,
                        required=False,
                        help='location of bvecs ')
    parser.add_argument('--data', type=str,
                        required=False,
                        help='location of data.nii.gz ')
    parser.add_argument('--nodif', type=str,
                        required=False,
                        help='location of nodif_brain_mask ')
    parser.add_argument('--T1', type=str,
                        required=False,
                        help='location of T1 ')
    parser.add_argument('--aparc_aseg', type=str,
                        required=False,
                        help='location of freesurfer aparc+aseg.nii.gz ')
    parser.add_argument('--fsdefault', type=str,
                        required=False,
                        help='location of fsdefault')
    parser.add_argument('--FScolorLUT', type=str,
                        required=False,
                        help='location of FScolorLUT')

    args = parser.parse_args()
    print(args)



    #subNum='100307'
    #subsDir='/media/richard/camcan/Projects/LLNL_DTI'

    #with open(os.path.join(subsDir,'HCP_1200.txt')) as file:
    #for line in file:
    #    log(line)
    #   file = file.read().splitlines()
    #    subNum = file[1]

    # python
    test = mrtrix3(args.subNum, args.subsDir,
                  args.bvals, args.bvecs, args.T1, args.nodif, args.data, args.aparc_aseg,
                  args.fsdefault, args.FScolorLUT)

    test.checkenv()
    test.initdir(force=False)
    test.getFiles_local(force=False)
    #test.getFiles_aws(force=True)
    test.run_mrtrix3()


    #test._5ttgen()
    #test._5tt2vis()
    #test._labelconvert()
    #test._labelsgmfix()
    #test._mrconvert1()
    #test._dwiextract()
    #test._dwi2response()
    #test._dwi2fod()
    #test._mrconvert2()
    #test._tckgen()
    #test._tcksift()
    #test._tck2connectome()
    #test.print_time()


if __name__ == '__main__':

    main()
