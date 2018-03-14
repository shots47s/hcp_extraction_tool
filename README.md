# hcp_extraction_tool
This is a tool that will take a group of HCP data files that are tarred by subject and extract data files and subjects from the full dataset.

To use this tool you must have access to the HCP data.
This tool is special purpose as it works on the HCP data with the dataset tarred by subject (e.g. 104021.tar), which is necessary in HPC environments that require limits on the number of files.

To use the tool:

```
usage: extract_from_hcp.py [-h] [--subjectfile SUBJECTFILE]
                           [--extractfile EXTRACTFILE] [--outputdir OUTPUTDIR]
                           [--hcpdir HCPDIR]

Program to extract data set from HCP on CEDAR

optional arguments:
  -h, --help            show this help message and exit
  --subjectfile SUBJECTFILE, -s SUBJECTFILE
                        File with the subjects to be searched each one a line
  --extractfile EXTRACTFILE, -e EXTRACTFILE
                        File with the subjects to be searched each one a line
  --outputdir OUTPUTDIR, -o OUTPUTDIR
                        Directory to store the output of the extraction
  --hcpdir HCPDIR, -p HCPDIR
                        Location of the HCP data you would like to extract
                        from
```

The result will be the directory specified by outputdir that has the subset of the files that you asked to be extracted.

The strings in the extractfile needs to contain the strings to the files that you would like to extract from data set subjects.  Directories can be extracted as well, just put he directory name.


