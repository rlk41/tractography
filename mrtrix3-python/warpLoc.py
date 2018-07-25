from run_command import run_command
from os.path import join
from string import Template
from os import listdir
from os.path import isfile, join

def warp(subDir, sub, movFile, targFile, roiDir, outDir):

    matFile
    preFile

    roiFiles = [f for f in listdir(roiDir) if isfile(join(roiDir, f))]




    T1=Template("3dAllineate -base $_base -source $_source -prefix $_preFile -master $_base -1Dmatrix_save $_matFile -overwrite")\
    T1=T1.substitute(_base=targFile, _source=movFile, _pre=preFile, _matFile=matFile)

    for f in roiFiles:
        T2="3dAllineate -base  -source -prefix -master -1Dmatrix_apply -overwrite".format()

        T3="fslmaths {} -thr 0.05  -bin  {}".format()

        T4="rm {}".format()



    out, error = run_command(T)


    t = Template('dwi2fod msmt_csd $_DWI $_RF_WM $_WM_FODs $_RF_GM $_GM $_RF_CSF $_CSF -mask $_nodif')
    c=t.substitute(_DWI=self._DWI, _RF_WM=self._RF_WM, _WM_FODs=self._WM_FODs, _RF_GM=self._RF_GM, _GM=self._GM, _RF_CSF=self._RF_CSF, _CSF=self._CSF, _nodif=self.nodif_brain_mask)
    output, error = self.run_command(c)