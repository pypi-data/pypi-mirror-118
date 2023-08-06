#!/usr/bin/env python3

from fire import Fire
from read_vme_offline.version import __version__

#print("i... module read_vme_offline/ascdf is being run")

import pandas as pd
import tables # here, to avoid a crash when writing pandas
import h5py
import datetime
import subprocess as sp
import numpy as np

import os
import datetime as dt

#>>> import pandas as pd
#>>> import matplotlib.pyplot as plt
#>>> df=pd.read_hdf("run0001_20200526_102519.h5")
#>>> plt.hist( df['E'][  (df.xx=0) & ( (df.t-df.t.shift())<0.0001) ] , 1024, range=[0,2048] )
# plt.show()
#
#

def main1(filename, chan=1, od=0, do=9999999):
    """
    use: read_vme_offline cut1 filename_with_asc  60 120
    """
    # od = 0
    # do = 999999


    basename = os.path.basename(filename)
    startd = basename.split("_")[1]
    startt = basename.split("_")[2]
    print(startd+startt)
    ok = False
    try:
        start = dt.datetime.strptime(startd+startt,"%Y%m%d%H%M%S" )
        ok = True
    except:
        print("x... year may not by 4 digits")

    if not(ok):
        start = dt.datetime.strptime(startd+startt,"%y%m%d%H%M%S" )


    print("D... real start",start)
    od_dt = dt.timedelta(seconds=od)
    print("D... skip      ",od_dt)
    startcut = start + od_dt
    print("D...  cut start",startcut)

    print(basename)
    df = pd.read_table( filename, names=['time','E','x','ch','y'], sep = "\s+", comment="#")
    print(df)

    print(f"D...  selecting events for  channel {chan} from {od}s to {do}s")

    ex = 1e+8
    # df1 = df[ (df.ch==chan)&(df.E!=0)&(df.time>ex*od)&(df.time<ex*do)  ]
    df1 = df[ (df.ch==chan)&(df.time>ex*od)&(df.time<ex*do)  ]
    #df2=df['E']
    #df3 = df2[ (df1.E!=0)  ]


    print(f"D...  numpy array for ch {chan}  ________________________CUT___________")
    df1.reset_index(inplace=True, drop=True)
    print(df1)

    dfzero = df1[ (df.E==0) ]
    df2 = df1[ df.E!=0 ]
    df2.reset_index(inplace=True, drop=True)
    print()
    print("i... ZEROES == ", len(dfzero))
    print("i... EVENTS == ", len(df2))
    deadtpr = len(dfzero)/len(df2) * 100
    fev = df1.time.iloc[0]/ex
    lev = df1.time.iloc[-1]/ex
    print(f"i... DT %   == {deadtpr:.2f}")
    # print(f"i... events == {fev} ... {lev}")
    # print(f"i... times  == {fev:.2f} ... {lev:.2f}")
    dift = lev - fev
    deadt = dift*deadtpr/100
    livet = dift - deadt

    print(f"i... times  == {fev:.2f} ... {lev:.2f}")
    print(f"i... real T == {dift:.2f} s")
    print(f"i... live T == {livet:.2f} s")
    print(f"i... dead T == {deadt:.2f} s")
    print(f"i... start  == {start} ")
    print(f"i... CUTsta == {startcut} ")
    print()

    narr = df2.E.to_numpy()

    print(f"D...  creating histogram for channel {chan} from numpy")

    his,bins = np.histogram(narr,bins=1024*32,range=(0.0,1024*32) )
    print(his)
    print(bins)

    outfile = os.path.splitext(filename)[0]+".txt"
    print("D... outfile=", outfile)
    np.savetxt(outfile, his, fmt="%d")



if __name__=="__main__":
    Fire(main1)
