################################################################################
"""CSMI MSP Parsing

Usage:
  mspCSMI.py makeDB <mspFile> <metaDataFile> <spectrumFile>
  mspCSMI.py getSpectrum <spectrumIndex> <spectrumFile> [<outFile>]
  mspCSMI.py plotSpectrum <spectrumIndex> <spectrumFile> <outFile>
  mspCSMI.py (-h | --help)
  mspCSMI.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --speed=<kn>  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.

"""
################################################################################
import sys
import os
import re
import numpy as np
import pandas as pd
import pickle as pkl
import matplotlib.pyplot as plt
from docopt import docopt
################################################################################

def getMD(mdt):
    md = {}
    for mx in mdt.strip().split('\n'):
        splitTemp = [mx.split(":")[0], ":".join(mx.split(":")[1 : ])]
        l = [x.strip() for x in splitTemp]
        if len(l) != 2:
            sys.exit(f"Error parsing line: {mx}")
        try: 
            v = int(l[1])
        except:
            try:
                v = float(l[1])
            except:
                if l[1].strip() == "":
                    v = None
                else:
                    v = l[1]
        md[l[0]] = v
    return(md)

def getSpec(spect):
    l = spect.strip().split('\n')[1 : ]
    outSpec = []
    for ls in l:
        ls = ls.strip()
        for badS in ["(2M-H)-", "+", "-"]:
            if badS in ls:
                ls = ls.replace(badS, "")
        if ls.startswith("===") or ls == '' or ls.startswith("m/z Abund"):
            continue
        elif '\t' not in ls and ' ' not in ls and ',' in ls:
            ls = ls.replace(',', '\t')
            splitTemp = ls.replace('\t\t\t', '\t').replace('\t\t', '\t').split('\t')
        elif '\t' not in ls:
            splitTemp = [' '.join(ls.split(' ')[ : -1]), ls.split(' ')[-1]]
        else:
            splitTemp = ls.replace('\t\t\t', '\t').replace('\t\t', '\t').split('\t')
        splitTemp[0] = splitTemp[0].split(' ')[0]
        splitTemp = [x.replace(',', '').strip() for x in splitTemp if x != '']
        splitTemp = [float(x) for x in splitTemp]
        if len(splitTemp) == 1:
            splitTemp.append(0)
        outSpec.append(splitTemp)
    spec = np.array(outSpec)
    return(spec)

def processChunk(chunk, chunkIdx):
    mdt, spect = chunk.split('Num Peaks:')
    md = getMD(mdt)
    npi = spect.split('\n')[0].strip()
    if npi != '':
        md['Num Peaks'] = int(npi)
    else:
        md['Num Peaks'] = 0
    md['Idx'] = chunkIdx
    spec = getSpec(spect)
    return(md, spec)

def getDB(fnameIn):
    with open(fnameIn, 'r', encoding = 'latin-1') as f:
        lines = f.read()
    chunks = [f"NAME:{x}" for x in lines.split('NAME:') if x != '']
    mds, specs = zip(*([processChunk(chunk, i_chunk) for i_chunk, chunk in enumerate(chunks)]))
    dfMD = pd.DataFrame(mds)
    return(dfMD, specs)

def createDB(fnameIn, fnameOutMD, fnameOutSpecs):
    if not fnameOutSpecs.endswith(".pkl"):
        sys.exit("Error - Spectra out file must end in .pkl")
    if not fnameOutSpecs.endswith(".pkl"):
        sys.exit("Error - Spectra out file must end in .pkl")
    if not fnameOutMD.endswith(".tsv"):
        sys.exit("Error - Metadata out file must end in .tsv")
    dfMD, specs = getDB(fnameIn)
    dfMD.to_csv(fnameOutMD, sep = '\t', index = False)
    pkl.dump(specs, open(fnameOutSpecs, 'wb'))
    print(f"\nMetadata file created at {fnameOutMD}\n")
    print(f"Spectra file created at {fnameOutSpecs}\n")
    print(f"Available keys to Query are:")
    d = {'object': "String", "float64" : "float", "int64" : "int"}
    for c in dfMD.columns:
        print(f"\t{c} -- ({d[str(dfMD.dtypes[c])]} query)")
    return(dfMD, specs)
    
def getSpectrumVals(idx, fnameSpecs, outFile = None):
    specs = pkl.load(open(fnameSpecs, 'rb'))
    s = "m/z\tIntensity\n"
    for mz, intensity in specs[idx]:
        s+= f"{mz}\t{intensity}\n"
    if outFile != None:
        with open(outFile, 'w') as f:
            print(s, file = f)
    else:
        print(s)
        
def plotSpectrum(idx, fnameSpecs, outFile):
    specs = pkl.load(open(fnameSpecs, 'rb'))
    spec = specs[idx]
    fig, ax = plt.subplots()
    plt.vlines(spec[ : , 0], 0, spec[ : , 1], color = 'k')
    _ = ax.set_ylim(0, ax.get_ylim()[1])
    _ = ax.set_xlim(0, ax.get_xlim()[1])
    _ = plt.xlabel("m/z")
    _ = plt.ylabel("Intensity")
    plt.savefig(outFile, bbox_inches = 'tight')
    plt.close()
    
def main():
    args = docopt(__doc__, version='mspCMSI 0.1')
    if args["makeDB"]:
        createDB(args["<mspFile>"], args["<metaDataFile>"], args["<spectrumFile>"])
    if args["getSpectrum"]:
        getSpectrumVals(int(args["<spectrumIndex>"]), args["<spectrumFile>"], outFile = args["<outFile>"])
    if args["plotSpectrum"]:
        plotSpectrum(int(args["<spectrumIndex>"]), args["<spectrumFile>"], args["<outFile>"])
    
################################################################################

if __name__ == '__main__':
    main()

