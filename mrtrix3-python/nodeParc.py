import nibabel as nib
from nibabel.nifti1 import load, save
from nibabel.nifti1 import load as loadnii
from nibabel.freesurfer.mghformat import load as loadmgz
import numpy as np
import csv
from os.path import join, isfile, exists, basename, split
import os
from os import listdir
#from run_command import run_command
from string import Template

def bbregDTI(subPath, b0, reg):
    subsDir, sub = split(subPath)
    set_subsDir(subsDir)
    t = Template('/usr/local/freesurfer/bin/bbregister --s $_sub --mov $_b0 --dti --reg $_reg --init-fsl')
    c=t.substitute(_sub=sub, _b0=b0, _reg=reg)
    return run_command(c)

def bbregDTIinv(subPath, b0, reg):
    subsDir, sub = split(subPath)
    set_subsDir(subsDir)
    t = Template('/usr/local/freesurfer/bin/bbregister --s $_sub --mov $_b0 --dti --reg $_reg --init-fsl --inv')
    c=t.substitute(_sub=sub, _b0=b0, _reg=reg)
    return run_command(c)


def set_subsDir(subsDir):
    #t=Template('export SUBJECTS_DIR=$_subsDir')
    #c=t.substitute(_subsDir=subsDir)
    os.environ['SUBJECTS_DIR'] = subsDir
    return True

def niiCheck(file):
    if not isfile(file):
        mgz = file.replace('.nii.gz','.mgz')
        if isfile(mgz):
            mrconvert(mgz, file)

    return True


def createReg(subPath, movFile, targFile, o, reg):
    subsDir, sub = split(subPath)
    set_subsDir(subsDir)

    niiCheck(movFile)
    niiCheck(targFile)

    t=Template('3dAllineate -base $_targFile -source $_movFile -prefix $_o -master $_targFile -1Dmatrix_save $_reg -overwrite')
    c=t.substitute(_targFile=targFile , _movFile=movFile, _o=o, _reg=reg)
    print("targFile: {}".format(targFile))
    print("movFile:  {}".format(movFile))
    print("output:   {}".format(o))
    print("reg:      {}".format(reg))

    output, error = run_command(c)
    print("output:   ".format(output))
    print("error:    ".format(error))
    return output, error



def applyReg(subPath, movFile, targFile, masterFile, o, reg, Inv=False, warp=False, thr=False, bin=True, final=False, overwrite=True):
    subsDir, sub = split(subPath)
    set_subsDir(subsDir)

    niiCheck(movFile)

    # not working
    if Inv:
        tail, head = split(reg)
        regI = head.replace('.aff12.1D','').split('2')
        regI = "{}/{}2{}.aff12.1D".format(tail, regI[1], regI[0])
        t=Template('cat_matvec -ONELINE $_reg -I')
        c=t.substitute(_reg=reg, _regI=regI)
        output, error = run_command(c)
        print(output)
        print("Fwd:    {}".format(reg))
        print("Inv:    {}".format(regI))
        reg = regI
        print("Using   {}".format(reg))
    #
    # if warp:
    #     t=Template('3dAllineate -base $_targFile -source $_movFile -prefix $_o -master $_masterFile -1Dmatrix_apply $_reg -warp $_warp -overwrite')
    #     c=t.substitute(_targFile=targFile , _movFile=movFile, _o=o, _reg=reg, _warp=warp, _masterFile=masterFile)
    #     print("Warp:   {}".format(warp))
    #
    # else:
    #     t=Template('3dAllineate -base $_targFile -source $_movFile -prefix $_o -master $_masterFile -1Dmatrix_apply $_reg -overwrite')
    #     c=t.substitute(_targFile=targFile , _movFile=movFile, _o=o, _reg=reg, _masterFile=masterFile)

    t_string='3dAllineate -base $_targFile -source $_movFile -prefix $_o -master $_masterFile -1Dmatrix_apply $_reg'

    if warp:
        t_string += ' -warp $_warp'
        print("Warp:   {}".format(warp))

    if final:
        t_string += ' -final $_final'
        print("final:   {}".format(final))

    if overwrite:
        t_string += ' -overwrite'
        print("overwrite:   {}".format(overwrite))

    t=Template(t_string)
    c=t.substitute(_targFile=targFile , _movFile=movFile, _o=o, _reg=reg, _warp=warp, _masterFile=masterFile,
                   _final=final)

    print("targFile: {}".format(targFile))
    print("movFile:  {}".format(movFile))
    print("output:   {}".format(o))
    print("reg:      {}".format(reg))
    print("command:  {}".format(c))

    output, error = run_command(c)
    print("output:   ".format(output))
    print("error:    ".format(error))

    if thr:
        head, tail = split(o)
        head = "{}.bin".format(head)
        if not exists(head):
            os.mkdir(head)
        tail = tail.replace('nii.gz','bin.nii.gz')
        thresh(o, out=join(head,tail), thr=thr, bin=bin)
        print("threshholded")
    return output, error

# def applyThresh(i, o, thr=0.05 ):
#     #t=Template("fslmaths $_i -thr $_thr -bin $_o")
#     #c=t.substitute(_i=i , _o=o, _thr=thr)
#     #output, error = run_command(c)
#     print("output:   ".format(output))
#     print("error:    ".format(error))
#     return output, error

def applyThresh(i, o, thr=0.05 ):
    #t=Template("fslmaths $_i -thr $_thr -bin $_o")
    #c=t.substitute(_i=i , _o=o, _thr=thr)
    #output, error = run_command(c)
    print("output:   ".format(output))
    print("error:    ".format(error))
    return output, error

def nodeParc2(inFiles, outFile, LUT):

    print('Runnning nodeParc')
    head, tail  = split(outFile)

    m               = load(inFiles[0])
    aff, header     = m.affine, m.header
    complete        = np.ones(m.get_data().shape, dtype=int)

    labLUT, numLUT      = [], []

    rowsOut = []

    with open(LUT, 'rt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            if row:
                for path in inFiles:
                         if row[2] in path:

                            a = path
                            a_head, a_tail = split(a)
                            a_Load  = load(a)
                            a_Data  = a_Load.get_data()

                            o = bin(a_Data, 1, row[1])
                            o[np.where(o == 0)] = 1

                            complete = complete * o

                            numLUT.append(row[1])
                            labLUT.append(row[2])

                            print('{}      {}     {}'.format(row[1], row[2], a_tail))


    complete[np.where(complete == 1)] = 0
    saveNifti(complete, aff, header, head, tail)
    nc = np.unique(complete)
    print('{} Values: {}'.format(len(numLUT), numLUT))
    print('{} Values: {}'.format(len(nc), nc))

    csvPath = join(head, tail)
    with open(csvPath, 'w', newline='\n') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for r in rowsOut:
            spamwriter.writerow([r])


    csvPath = "{}_cumulative".format(LUT)
    with open(csvPath, 'a', newline='\n') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for r in nc:
            spamwriter.writerow([r])

    return True

def nodeParc(inFiles, outFile):

    print('Runnning nodeParc')
    head, tail  = split(outFile)

    m               = load(inFiles[0])
    aff, header     = m.affine, m.header
    complete        = np.ones(m.get_data().shape, dtype=int)

    labLUT, numLUT      = [], []

    f = next_prime(2)

    for a in inFiles:

        a_head, a_tail = split(a)
        a_Load  = load(a)
        a_Data  = a_Load.get_data()

        o = bin(a_Data, 1, f)
        o[np.where(o == 0)] = 1

        complete = complete * o

        numLUT.append(f)
        labLUT.append(a_tail)

        print('f         {} a_tail  {}'.format(f, a_tail))

        f = next_prime(f)


    complete[np.where(complete == 1)] = 0
    saveNifti(complete, aff, header, head, tail)

    print('{} Values: {}'.format(len(numLUT), numLUT))
    print('{} Values: {}'.format(len(np.unique(complete)), np.unique(complete)))

    csvPath = join(head, tail)
    with open(csvPath, 'w', newline='\n') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(labLUT)):
            spamwriter.writerow([numLUT[i], labLUT[i]])


    return True

def create_cumPrimeLUT(LUTtemplate):
    LUTtemplate     = LUTtemplate
    LUTcum          = "{}{}".format(LUTtemplate,'_cumulative')
    LUTtemplatecum  = "{}{}".format(LUTcum,'_sorted')



    temp_fill   = []
    temp_primes = []
    temp_labs   = []
    with open(LUTtemplate, 'rt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            if row:
                temp_fill.append(row[0])
                temp_primes.append(row[1])
                temp_labs.append(row[2])
    cum_primes  = []
    with open(LUTcum, 'rt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            if row:
                cum_primes.append(row[0])



    unq_cum_primes = np.sort(np.unique(cum_primes).astype(int))
    temp_primes = np.array(temp_primes).astype(int)

    prime2lab  = dict(zip(temp_primes, temp_labs))
    prime2fill = dict(zip(temp_primes, temp_fill))

    fill = np.max(np.array(temp_fill).astype(int)) + 1
    rowOut = []

    for u in unq_cum_primes:
        if u != 0:
            if u in prime2lab:
                #print(prime2lab[u], u)
                row = " ".join([str(prime2fill[u]), str(u), prime2lab[u], str(prime2fill[u])]) #
                print(row)
                rowOut.append(row)

            else:
                p = prime_factors(u)
                factors = []
                labs    = []

                for prime in p:
                    factors.append(prime)
                    labs.append(prime2lab[prime])
                factors = [str(prime2fill[f]) for f in factors]
                row = " ".join([str(fill), str(u), '&'.join(labs), '_'.join(factors)]) #
                print(row)
                rowOut.append(row)
                fill += 1

    with open(LUTtemplatecum, 'w', newline='\n') as csvfile:
        spamwriter = csv.writer(csvfile) #, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL

        for r in range(len(rowOut)):
            spamwriter.writerow([rowOut[r]])


    return

def mrtrixLUTParc2(inFile, LUTfile, outFile, noPrimes=False):

    head, tail  = split(outFile)

    print('Runnning nodezLUTParc')
    if '.nii.gz' not in inFile:
        inFile = '{}.nii.gz'.format(inFile)

    p               = load(inFile)
    aff, header     = p.affine, p.header
    pData           = p.get_data()
    complete        = np.zeros(pData.shape, dtype=int)
    #fillLUT, numLUT, factors, label     = [], [], [], []

    temp_fill   = []
    temp_prime  = []
    temp_labs   = []
    temp_factors_fill= []

    with open(LUTfile, 'rt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            temp_fill.append(row[0])
            temp_prime.append(row[1])
            temp_labs.append(row[2])
            temp_factors_fill.append(row[3])

    prime2fill = dict(zip(np.array(temp_prime).astype(int), np.array(temp_fill).astype(int)))
    prime2lab  = dict(zip(np.array(temp_prime).astype(int), temp_labs))
    prime2factors_fill  = dict(zip(np.array(temp_prime).astype(int), temp_factors_fill))


    #i = 1
    unq = np.unique(pData).astype(int)
    unq = unq[unq != 0]

    row = []
    row2= []

    for u in unq: print("%15f" % u)
    for u in unq:
        if u in prime2fill:

            out   = bin(pData, u, prime2fill[u])
            complete += out



            #fill2fill = [ f.split('_') for f in prime2factors_fill[u]]

            rowW  = " ".join([str(prime2fill[u]), str(u), str(prime2factors_fill[u]), prime2lab[u]])
            print(rowW)
            row.append(rowW)

            #i += 1
        else:
            print('not in dict')
            print(u)

    saveNifti(complete, aff, header, head, tail)

    csvPath = join(head, tail)
    with open(csvPath, 'w', newline='\n') as csvfile:
        spamwriter = csv.writer(csvfile)

        for r in range(len(row)):
            spamwriter.writerow([row[r]])

    return True

def mrtrixLUTParc3(inFile, LUTfile, outFile, noPrimes=False):

    head, tail  = split(outFile)

    print('Runnning nodezLUTParc')
    if '.nii.gz' not in inFile:
        inFile = '{}.nii.gz'.format(inFile)

    p               = load(inFile)
    aff, header     = p.affine, p.header
    pData           = p.get_data()
    complete        = np.zeros(pData.shape, dtype=int)
    #fillLUT, numLUT, factors, label     = [], [], [], []

    temp_fill   = []
    temp_prime  = []
    temp_labs   = []
    temp_factors_fill= []

    with open(LUTfile, 'rt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            temp_fill.append(row[0])
            temp_prime.append(row[1])
            temp_labs.append(row[2])
            if not noPrimes:
                    temp_factors_fill.append(row[3])


        prime2fill = dict(zip(np.array(temp_prime).astype(int), np.array(temp_fill).astype(int)))
        prime2lab  = dict(zip(np.array(temp_prime).astype(int), temp_labs))
        if not noPrimes:
            prime2factors_fill  = dict(zip(np.array(temp_prime).astype(int), temp_factors_fill))


    #i = 1
    unq = np.unique(pData).astype(int)
    unq = unq[unq != 0]

    row = []
    row2= []

    for u in unq: print("%15f" % u)
    for u in unq:
        if u in prime2fill.keys():

            out   = bin(pData, u, prime2fill[u])
            complete += out



            #fill2fill = [ f.split('_') for f in prime2factors_fill[u]]
            if not noPrimes:
                rowW  = " ".join([str(prime2fill[u]), str(u), str(prime2factors_fill[u]), prime2lab[u]])
            else:
                rowW  = " ".join([str(prime2fill[u]), str(u), prime2lab[u]])

            print(rowW)
            row.append(rowW)

            #i += 1
        else:
            print('not in dict')
            print(u)

    saveNifti(complete, aff, header, head, tail)

    csvPath = join(head, tail.replace('.nii.gz','.txt'))
    with open(csvPath, 'w', newline='\n') as csvfile:
        spamwriter = csv.writer(csvfile)

        for r in range(len(row)):
            spamwriter.writerow([row[r]])

    return True

def mrtrixLUTParc(inFile, LUTfile, outFile):

    head, tail  = split(outFile)

    print('Runnning nodezLUTParc')
    if '.nii.gz' not in inFile:
        inFile = '{}.nii.gz'.format(inFile)

    p               = load(inFile)
    aff, header     = p.affine, p.header
    pData           = p.get_data()
    complete        = np.zeros(pData.shape, dtype=int)
    fillLUT, numLUT, factors, label     = [], [], [], []

    labDict = {}
    with open(LUTfile, 'rt') as csvfile:
       spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
       for row in spamreader:
           labDict[row[0]] = row[1]



    i = 1
    unq = np.unique(pData)
    unq = np.delete(unq, [unq == 0])

    row = []
    row2= []

    for u in unq: print("%15f" % u)
    for u in unq:

        out   = bin(pData, u, i)
        complete += out

        #label = '{}_{}'.format(tail,int(u))

        #saveNifti(out, aff, header, head, label)


        facts = prime_factors(u)
        facts = [str(int(f)) for f in facts]

        label = []
        for f in facts:
            label.append(labDict[f])

        if len(facts) > 1:
            facts = " ".join(facts)
            label = "_".join(label)

        else:
            facts = "{}".format(int(facts[0]))
            label = "{}".format(label[0])
        label = label.replace('.brain.bin.nii.gz','')
        #print("{}   {}      {}".format(i, u, facts))
        #labels = [labDict['{}'.format(int(f))] for f in facts]

        #factors.append(facts)
        #fillLUT.append(i)
        #numLUT.append(int(u))
        rowW  = "{} {} {}".format(i, int(u), facts)
        rowW2 = "{} {}".format(i, label)
        print(rowW)
        print(rowW2)
        row.append(rowW)
        row2.append(rowW2)

        i += 1

    #label = '{}_{}'.format(head, )
    saveNifti(complete, aff, header, head, tail)

    print(row)
    print(row2)

    csvPath = join(head, tail)
    with open(csvPath, 'w', newline='\n') as csvfile:
        spamwriter = csv.writer(csvfile) #, delimiter=' ',
                                          #quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #for j in range(len(fillLUT)):
        #    spamwriter.writerow([fillLUT[j], numLUT[j], factors[j]])
        for r in range(len(row)):
            spamwriter.writerow([row[r]])

    csvPath = join(head, "{}_2".format(tail))
    with open(csvPath, 'w', newline='\n') as csvfile:
        spamwriter = csv.writer(csvfile) #, delimiter=' ',
                                          # quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #for j in range(len(fillLUT)):
        #    spamwriter.writerow([fillLUT[j], numLUT[j], factors[j]])
        for r in range(len(row2)):
            spamwriter.writerow([row2[r]])

    return True

def nii2mif(inFile, outFile):
    # if '.nii.gz' not in inFile:
    #     inFile = "{}.nii.gz".format(inFile)
    # if '.mif'    not in outFile:
    #     outFile = "{}.mif".format(outFile)
    # for f in MR*; do mrconvert ${f}/mask.localizer.brain.localizers_Parc.nii.gz ${f}/mask.localizer.brain.localizers_Parc.mif; done



    t = Template('mrconvert $_inFile $_outFile ')
    c=t.substitute(_inFile=inFile, _outFile=outFile)
    output, error = run_command(c)
    return True

def mrconvert(inFile, outFile):
    # if '.nii.gz' not in inFile:
    #     inFile = "{}.nii.gz".format(inFile)
    # if '.mif'    not in outFile:
    #     outFile = "{}.mif".format(outFile)
    # for f in MR*; do mrconvert ${f}/mask.localizer.brain.localizers_Parc.nii.gz ${f}/mask.localizer.brain.localizers_Parc.mif; done



    t = Template('mrconvert $_inFile $_outFile ')
    c=t.substitute(_inFile=inFile, _outFile=outFile)
    output, error = run_command(c)
    return True

def gmFix(inFile, outFile):
    run_command()
    return True

def assignStreamlines(sift, nodes, LUT):
    conn = "{}_Conn".format(nodes.replace('.nii.gz', ''))
    t = Template('/usr/local/mrtrix3/bin/tck2connectome $_10M_SIFT $_nodes_fixSGM $_connectome -force')
    c=t.substitute(_10M_SIFT=sift, _nodes_fixSGM=nodes, _connectome=conn)
    out, error = run_command(c)
    return out, error

def prime2nodeParc():
    return True

def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

def is_prime(n):
    if n == 2 or n == 3: return True
    if n < 2 or n%2 == 0: return False
    if n < 9: return True
    if n%3 == 0: return False
    r = int(n**0.5)
    f = 5
    while f <= r:
        print('\t {}'.format(f))
        if n%f == 0: return False
        if n%(f+2) == 0: return False
        f +=6
    return True

def next_prime(s=0):
    s += 1
    while not is_prime(s):
            s += 1
    return s

def openVol(volPath):
    if '.nii' in volPath:
        p               = loadnii(volPath)
        aff, header     = p.affine, p.header
        pData           = p.get_data()
        return pData, aff, header
    elif '.mgz' in volPath:
        p               = loadmgz(volPath)
        aff, header     = p.affine, p.header
        pData           = p.get_data()
        return pData, aff, header
    else:
        p               = loadnii("{}.nii.gz".format(volPath))
        aff, header     = p.affine, p.header
        pData           = p.get_data()
        return pData, aff, header
    return False

def dump(Data, ROI, search=None):
    ROI = np.array(ROI, dtype=bool)
    g = np.zeros(ROI.shape, dtype=int)
    if search == None:
        g[np.where(ROI != 0)] = Data[np.where(ROI != 0)]
    else:
        g[np.where(ROI == search)] = Data[np.where(ROI == search)]
    return g

def dumpNifti(dataPath, ROIPath, outPath=False, search=None):

    head, tail = split(dataPath)
    head_out, tail_out = split(outPath)

    dData, dAff, dHeader = openVol(dataPath)
    rData, rAff, rHeader = openVol(ROIPath)


    g = dump(dData, rData, search)

    if outPath:
        saveNifti(g, dAff, dHeader, head_out, tail_out)
    else:
        saveNifti(g, dAff, dHeader, head, "{}.Fix".format(tail))
    return True

def bin(Data, search, fill):
    g = np.zeros(Data.shape, dtype=int)
    g[np.where(Data == search)] = fill
    return g

def saveNifti(g, aff, head, path, label):

    img = nib.Nifti1Image(g, affine=aff, header=head)
    if ".nii" not in label:
        label = '{}.nii.gz'.format(label)
    nib.save(img, join(path,label))

def thresh(vol, thr=False, uthr=False, bin=False, out=False):
    if '.nii' or '.nii.gz' or '.mgz' in vol: 
        data, aff, header = openVol(vol)
    else: 
        data = vol 
        
    if thr: 
        data[np.where(data < thr)] = 0
    if uthr: 
        data[np.where(data > thr)] = 0 
    if bin:
        data[np.where(data != 0 )] = 1

    if out: 
        head, tail = split(out)
        saveNifti(g=data, aff=aff, head=header, path=head, label=tail)
        print("Thresholded and saved to: {}/{}".format(head,tail))
        return True     
    else: 
        return data, aff, header


def labelsgmfix(nodesmif, T1, fsdefault, nodes_fixSGM):
    print('Running _labelsgmfix: ')
    t = Template('labelsgmfix $_nodesmif $_acpc $_fsdefault $_nodes_fixSGM -premasked')
    c=t.substitute(_nodesmif=nodesmif, _acpc=T1, _fsdefault=fsdefault, _nodes_fixSGM=nodes_fixSGM)
    output, error = run_command(c)
    return output, error







    # def intersect(a, b, new):
#     # need to automate expansion of primes
#     #c = np.zeros(hcp_Data.shape, dtype=int)
#
#     head, tail  = split(new)
#
#     a_Load  = load(a)
#     b_Load  = load(b)
#
#     a_Data  = a_Load.get_data()
#     b_Data  = b_Load.get_data()
#
#     a_Data[np.where(a_Data != 0)] = 3
#     b_Data[np.where(b_Data != 0)] = 7
#
#     a_Data[np.where(a_Data == 0)] = 1
#     b_Data[np.where(b_Data == 0)] = 1
#
#     c_Data = a_Data*b_Data
#
#     unq = np.unique(c_Data)
#     i = 1
#     #u = 3
#     for u in unq:
#         if u != 1:
#             out   = bin(c_Data, u, 1)
#             aff   = a_Load.affine
#             header  = a_Load.header
#             label = '{}_{}'.format(tail,int(u))
#
#             saveNifti(out, aff, header, head, label)




# def nodeParc():
#
# # create nodeParcellation, individual bins and LUT
#
# hcpM         = load(HCPMask)
# hcp_Data     = hcpM.get_data()
# c    = 1
# fill = 1
#
#
# tocsv = []
# tocsv.append(['fill', 'label'])
#
# complete = np.zeros(hcp_Data.shape, dtype=int)
#
#
#
# for lab in range(len(locROI_Name)):
#     locROI_Load  = load(locROI_Path[lab])
#     locROI_Data  = locROI_Load.get_data()
#
#     aff  = locROI_Load.affine
#     head = locROI_Load.header
#
#     label       = locROI_Name[lab].split('.')[0]
#     glLabel     = '{}_{}'.format(lab+1, label)
#
#
#
#     r            = np.zeros(locROI_Data.shape, dtype=int)
#     g            = dump(hcp_Data, locROI_Load.get_data())
#
#     r[np.where(g > 1000)] = lab+1
#     rr           = bin(r, lab+1, 1)
#
#     #saveNifti(rr, aff, head, outDir2, '{}_{}.bin'.format(lab+1,label))
#     saveNifti(rr, aff, head, outDir3, '{}_{}.bin'.format(lab+1,label))
#
#
#     tocsv.append([fill, glLabel, label])
#
#
#     complete += r
#
#
# aff  = hcpM.affine
# head = hcpM.header
# #saveNifti(complete, aff, head, outDir2, 'Glasser-Localizer.bin')
# saveNifti(complete, aff, head, outDir3, 'Glasser-Localizer.bin.papers')
#
# #csvPath = join(mainDir, 'MR1103','Glasser-Localizer_bin_papers_LUT')
# csvPath = join(mainDir, 'MR1103','Glasser-Localizer_bin_LUT')
#
# with open(csvPath, 'w', newline='\n') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter=' ',
#                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     for i in tocsv:
#         spamwriter.writerow(i)
#

#create LUT for mrtrix
# tocsv = []
# tocsv.append(['fill', 'label', 'unq', 'unqCount'])
#
# complete = np.zeros(hcp_Data.shape, dtype=int)
#
#useUnq = False
#
# for lab in range(len(locROI_Name)):
#     locROI_Load  = load(locROI_Path[lab])
#     locROI_Data  = locROI_Load.get_data()
#     label        = locROI_Name[lab].split('.')[0]
#     g            = dump(hcp_Data, locROI_Load.get_data())
#
#     nonUnq = np.zeros(hcp_Data.shape, dtype=int)
#
#     for unq in np.unique(g):
#         if unq > 1000:
#             unqCount = len(np.where(g == unq))
#             r = bin(g, unq, fill)
#             aff  = locROI_Load.affine
#             head = locROI_Load.header
#             glLabel = '{}_{}_{}'.format(label, unq)
#             saveNifti(r, aff, head, outDir, '{}_{}.unq'.format(fill,label,unq))
#             tocsv.append([fill, glLabel, label, unq, unqCount])
#             if useUnq:
#                 fill += 1
#             complete += r
#             nonUnq   += r
#
#     saveNifti(nonUnq, aff, head, outDir, '{}_{}.unq'.format(fill,label))
#
# fill += 1









# a=join(mainDir, 'MR1103','mask.localizer-Glasser.bin.fix','6_1103_TVSA.bin.nii.gz')
# b=join(mainDir, 'MR1103','mask.localizer-Glasser.bin.fix','11_1103_midTemp_from_word_contrast.bin.nii.gz')
# new=join(mainDir, 'MR1103','mask.localizer-Glasser.bin.fix','TVSA_midTemp_wC_Intersect')
# intersect(a,b,new)
#
# roiDir =join(mainDir, 'MR1103','mask.localizer-Glasser.bin.fix')
# outPath=join(roiDir, 'Glasser-Localizer.bin.fix')
# buildParcellation(roiDir, outPath)
