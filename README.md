# mspCMSI



## Usage v0.1

### Create "Database"

First, create a "database" (metadata .tsv file + a binary pickle file containing spectra) from an msp file by running

``` bash
mspCSMI.py makeDB <mspFile.msp> <metaDataFile.tsv> <spectrumFile.pkl>
```

This will create a .tsv file in the location specified by <metaDataFile.tsv>. For now, this file can be used for querying the contents of the MSP file

### Get Spectrum
Once you've found an interesting spectrum's index, get the spectrum by running

``` bash
mspCSMI.py getSpectrum <spectrumIndex> <spectrumFile.pkl> [<outFile>]
```

Optionally including a tab-separated <outFile> to write to (e.g. (otherwise the spectrum will just print to stdout)


### Plot Spectra

A spectrum plot can be created by running 

``` bash
mspCSMI.py plotSpectrum <spectrumIndex> <spectrumFile.msp> <outFile>
```

Here <outFile> is required



## (Optional) Installation