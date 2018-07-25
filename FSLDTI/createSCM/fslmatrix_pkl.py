import os
import pickle
import matplotlib.pyplot
import numpy as np

def open_pckls(mypath):
    files = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    pckls = []

    for i in range(len(files)):
        print(i)
        print(files[i])
        file2 = open(files[i], 'rb')
        pckls.append(pickle.load(file2))
        file2.close()

    return pckls


def extract_connOut1(conn, selectLabs, labs):

    indexLabs = []
    indexNums  = []
    blob      = []

    j  = 0
    for i in range(len(selectLabs)):
        for ii in range(len(labs)):
            if selectLabs[i] in labs[ii]:
                indexLabs.append(labs[ii])
                indexNums.append(ii)
                blob.append(j)

        j += 1





    #print(indexLabs)
    #print(indexNums)
    #print(blob)


    connOut = conn[np.ix_(indexNums,indexNums)]



    return dd,selectLabs



def extract_connOut2(conn, selectLabs, labs):

    indexLabs = []
    indexNums  = []
    blob      = []

    j  = 0
    missing = []
    for i in range(len(selectLabs)):
        found = False
        for ii in range(len(labs)):
            if selectLabs[i] in labs[ii]:
                indexLabs.append(labs[ii])
                indexNums.append(ii)
                blob.append(j)
                found = True
        if not found:
                indexLabs.append(labs[ii])
                blob.append(j)
                missing.append(j)
                print(selectLabs[i])

        j += 1





    #print(indexLabs)
    #print(indexNums)
    #print(blob)

    #for i in range(len(index)):
    #    print(labs[index[i]])

    #for b in blob:
    #    blobOut = conn[np.ix_(blob[b],blob[b])]



    connOut = conn[np.ix_(indexNums,indexNums)]

    print('missing')
    print(missing)

    #print(connOut.shape)
    if missing:
        for m in missing:
            #connOut = np.insert(connOut, j, [np.nan]*connOut.shape[0], axis=1)
            #connOut = np.insert(connOut, j, [np.nan]*connOut.shape[1], axis=0)

            connOut = np.insert(connOut, m, np.nan, axis=1)
            connOut = np.insert(connOut, m, np.nan, axis=0)


    #print(connOut)


    setblob = set(blob)
    N = len(blob)
    Nsetblob = len(setblob)

    m1 = np.array([blob,]*N)
    m2 = np.array([blob,]*Nsetblob).transpose()

    print(connOut.shape)
    print(blob)

    #print(m1.shape)
    #print(m1.shape)
    #print(m1.shape)
    #print(m1)
    #print(m2.shape)
    #print(m2)


    np.fill_diagonal(connOut, 0)
    #print(blob)
    c = []
    for height in range(connOut.shape[0]):
        r = []
        for s in setblob:
            sum_list = []
            for ss in range(len(blob)):
                if s == blob[ss]:
                    sum_list.append(connOut[height][ss])
            #print("h:{} s:{} sumlist'{}".format(height, s, sum_list))

            r.append(sum(sum_list))
        c.append(r)

    cc = np.array(c)

    #print(cc.shape)


    d = []
    for width in range(cc.shape[1]):
        r = []
        for s in setblob:
            sum_list = []
            for ss in range(len(blob)):
                if s == blob[ss]:
                    sum_list.append(cc[ss][width])
            #print("w:{} s:{} sumlist:{}".format(width, s, sum_list))

            r.append(sum(sum_list))
        d.append(r)
    dd = np.array(d)
    #print(dd.shape)
    #print(dd)





    #arr1 = np.empty((Nsetblob,N), int)
    #arr2 = np.empty((Nsetblob,Nsetblob), int)

    #print('setblob')
    #print(setblob)
    #print(m1)

    #for ii in range(m1.shape[0]):
    #for i in setblob:
    #    c.append(connOut[i == m1].sum(keepdims=True))
    #print(c)

    #np.ma.array(connOut, mask=)

    #for i in setblob:
    #    print(c[i == m2])
    #    d.append(c[i == m2].sum(axis=0))

        #s = np.ma.array(connOut, mask=np.ma.masked_where(m1==i, m1))
        #print(s)
        #print('sum')
        #print(s.sum(axis=0))


    #print(c)
    #m2 = np.array([blob,]*len(c)).transpose()

    #for i in range(len(setblob)):
    #    s = np.ma.array(c, mask=np.ma.masked_where(m2==i, m2))
    #    d.append(s.sum(axis=1))



    #print(d)
    #d.append(np.ma.sum(connOut, axis=1, mask=np.ma.masked_where(m2==i, m2)))




    selectLabs = [x.rstrip('.') for x in selectLabs if x ]

    #print(dd)
    #print(selectLabs)
    return dd,selectLabs



def extract_connOut3(conn, selectLabs, labs):

    indexLabs = []
    indexNums  = []
    blob      = []

    j  = 0
    missing = []
    for i in range(len(selectLabs)):
        found = False
        for ii in range(len(labs)):
            if selectLabs[i] in labs[ii]:
                indexLabs.append(labs[ii])
                indexNums.append(ii)
                blob.append(j)
                found = True
        if not found:
            indexLabs.append(labs[ii])
            blob.append(j)
            missing.append(j)
            print(selectLabs[i])

        j += 1


    connOut = conn[np.ix_(indexNums,indexNums)]

    print('missing')
    print(missing)

    if missing:
        for m in missing:

            connOut = np.insert(connOut, m, np.nan, axis=1)
            connOut = np.insert(connOut, m, np.nan, axis=0)

    setblob = set(blob)
    N = len(blob)
    Nsetblob = len(setblob)

    print(connOut.shape)
    print(blob)

    out = np.empty([Nsetblob,Nsetblob])
    for i in range(Nsetblob):
        for ii in range(Nsetblob):
            #if i == ii:
            #    out[i][ii] = 1
            #else:
            xi = [ix for ix,xx in enumerate(blob) if i == xx ]
            yi = [ix for ix,xx in enumerate(blob) if ii == xx ]
            out[i][ii] = connOut[np.ix_(xi,yi)].mean()




    print(out)

    selectLabs = [x.rstrip('.') for x in selectLabs if x ]


    return out,selectLabs





def plot_fsl(connOut, selectLabs, saveName):

    #selectLabs = [labs[index[i]] for i in range(len(index))]
    #selectLabs = [ for i in range(len(selectLabs)) if selectLabs[i] ]


# figure plotting
    fig = matplotlib.pyplot.figure(figsize=(18, 15), dpi=100,)
    ax = fig.add_subplot(111)
    cax = ax.matshow(connOut, interpolation='nearest', )
    cax.set_cmap('hot')
    #caxes = cax.get_axes()

    # set number of ticks
    #caxes.set_xticks(range(len(new_order)))
    #caxes.set_yticks(range(len(new_order)))

    # label the ticks
    #if
    #caxes.set_xticklabels(new_order, rotation=90)
    #caxes.set_yticklabels(new_order, rotation=0)

    selectLabs = [x.replace('antTemporal_mask','aSTC') for x in selectLabs if x]
    selectLabs = [x.replace('midTemp_from_word_contrast','mSTC') for x in selectLabs if x]
    selectLabs = [x.replace('pSTS_test','pSTS') for x in selectLabs if x]

    selectLabs = [x[4:] if x[0:2].isdigit() else x for x in selectLabs  ]


    matplotlib.pyplot.xticks(range(len(selectLabs)), selectLabs, rotation='90', fontsize=20)
    matplotlib.pyplot.yticks(range(len(selectLabs)), selectLabs, rotation='horizontal', fontsize=20)        # axes labels
    #caxes.set_xlabel('Target ROI', fontsize=20)
    #caxes.set_ylabel('Seed ROI', fontsize=20)
    matplotlib.pyplot.xlabel('Target ROI', fontsize=23)
    matplotlib.pyplot.ylabel('Seed ROI', fontsize=23)

    # Colorbar
    cbar = fig.colorbar(cax)
    cbar.ax.tick_params(labelsize=20)

    #cbar.set_label('% of streamlines from seed to target', rotation=-90, fontsize=20)

    # title text
    #title_text = ax.set_title('Structural Connectivity with Freesurfer Labels & ProbtrackX2',
    #    fontsize=26)
    #title_text.set_position((.5, 1.10))

    #fig.show()
    fig.savefig(saveName+'.png')

    connSave = {'conn':connOut, 'labs':selectLabs, 'fig':fig}
    saveFile = open(saveName+'.pkl','wb')
    pickle.dump(connSave, saveFile)
    saveFile.close()


    matplotlib.pyplot.close()




mypath = '/media/richard/019147a8-ab26-4b03-a224-8cc72deaa00c/data03/saves'
conns = open_pckls(mypath)


STS1 = [ '032_R.BA1.1',
        '004_R.BA1.2',
        '057_R.BA1.3',
        '050_R.BA1.4',
        '254_L.BA1.1',
        '148_L.BA1.2',
        '262_L.BA1.3',
        '018_R.BA40.1',
        '100_R.BA40.2',
        '094_R.BA40.3',
        '005_R.BA40.4',
        '017_R.BA40.5',
        '195_L.BA40.1',
        '268_L.BA40.2',
        '245_L.BA40.3',
        '166_L.BA40.4',
        '015_R.BA41.1',
        '056_R.BA41.2',
        '218_L.BA41.1',
        '183_L.BA41.2',
        'pSTS_test']


STS1 = [ '032_R.BA1.1',
         '004_R.BA1.2',
         '057_R.BA1.3',
         '050_R.BA1.4',
         '018_R.BA40.1',
         '100_R.BA40.2',
         '094_R.BA40.3',
         '005_R.BA40.4',
         '017_R.BA40.5',
         '015_R.BA41.1',
         '056_R.BA41.2',
         '254_L.BA1.1',
         '148_L.BA1.2',
         '262_L.BA1.3',
         '195_L.BA40.1',
         '268_L.BA40.2',
         '245_L.BA40.3',
         '166_L.BA40.4',
         '218_L.BA41.1',
         '183_L.BA41.2',
         'pSTS_test']

STS1 = [ '032_R.BA1.1',
         '004_R.BA1.2',
         '057_R.BA1.3',
         '050_R.BA1.4',
         '018_R.BA40.1',
         '100_R.BA40.2',
         '094_R.BA40.3',
         '005_R.BA40.4',
         '017_R.BA40.5',
         '015_R.BA41.1',
         '056_R.BA41.2',
         '254_L.BA1.1',
         '148_L.BA1.2',
         '262_L.BA1.3',
         '195_L.BA40.1',
         '268_L.BA40.2',
         '245_L.BA40.3',
         '166_L.BA40.4',
         '218_L.BA41.1',
         '183_L.BA41.2',
         'pSTS_test']

STS = [ 'R.BA1.',
        'R.BA40.',
        'R.BA41.',
        'R.BA22.',
        'L.BA1.',
        'L.BA40.',
        'L.BA41.',
        'L.BA22.',
        'pSTS_test']

localizer = ['antTemporal_mask',
             'IFG_mask',
             'midTemp_from_word_contrast',
             'pSTS_test',
             'TPC_mask',
             'TVSA',
             'VT_L_ant_parietal',
             'VT_L_insula',
             'VT_L_S1_test',
             'VT_L_S2',
             'VT_L_supp_motor_test',
             'VT_R_ant_parietal',
             'VT_R_insula',
             'VT_R_S2',
             'VT_R_supp_motor_test',
             'VWFA']

localizer2 = ['032_R.BA1.1',
              '004_R.BA1.2',
              '057_R.BA1.3',
              '050_R.BA1.4',
              '018_R.BA40.1',
              '100_R.BA40.2',
              '094_R.BA40.3',
              '005_R.BA40.4',
              '017_R.BA40.5',
              '254_L.BA1.1',
              '148_L.BA1.2',
              '262_L.BA1.3',
              '195_L.BA40.1',
              '268_L.BA40.2',
              '245_L.BA40.3',
              '166_L.BA40.4',
              'antTemporal_mask',
              'midTemp_from_word_contrast',
              'pSTS_test']

localizer3 = ['R.BA1.',
              'R.BA40.',
              'L.BA1.',
              'L.BA40.',
              'antTemporal_mask',
              'midTemp_from_word_contrast',
              'pSTS_test']

labs4use = [[STS1,       'STS_sum_full',                        False   ],
            [STS,        'STS_mean_condensed_diag_BA22',        True    ],
            [localizer,  'localizer',                           False   ],
            [localizer2, 'STS_STC_BA40_BA1_mean_full',             False   ],
            [localizer3, 'STS_STC_BA40_BA1_mean_condensed',   True    ],
            [localizer3, 'localizer2S12_sum_condensed',         True    ]]


labs2use = labs4use[4]
n=0
connAve = np.zeros((len(labs2use[0]), len(labs2use[0])))
for i in range(len(conns)):
    labs = conns[i]['labs']
    conn = conns[i]['conn']
    print('new')
    #print(labs)
    saveName='/media/richard/019147a8-ab26-4b03-a224-8cc72deaa00c/data03/STS/'+str(i)+'_'+labs2use[1]
    #connOut,selectLabs = extract_connOut2(conn, labs2use[0], labs)
    connOut,selectLabs = extract_connOut3(conn, labs2use[0], labs)

    print(connOut.shape)

    if labs2use[2]:
        #connOut = connOut-200
        np.fill_diagonal(connOut, 100)


    plot_fsl(connOut, selectLabs, saveName)


    connAve = np.nanmean(np.dstack((connAve,connOut)),2)

    n += 1


#connAveFinal = (connAve/n)
connAveFinal = connAve
#np.fill_diagonal(connAveFinal, 100)

saveNameAve='/media/richard/019147a8-ab26-4b03-a224-8cc72deaa00c/data03/STS/ave_'+labs2use[1]
plot_fsl(connAveFinal, selectLabs, saveNameAve)




