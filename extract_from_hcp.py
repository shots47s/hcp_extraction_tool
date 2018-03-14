import os,sys
import glob
import tarfile
import argparse
import errno
import multiprocessing


def parseCommandLine():
    parser = argparse.ArgumentParser(description = "Program to extract data set from HCP on CEDAR")
    parser.add_argument('--subjectfile','-s',
                        type=lambda x: file_exists(parser,x),
                        help='File with the subjects to be searched each one a line')
    parser.add_argument('--extractfile','-e',
                        type=lambda x: file_exists(parser,x),
                        help='File with the subjects to be searched each one a line')
    parser.add_argument('--outputdir','-o',
                        help='Directory to store the output of the extraction')
    parser.add_argument('--hcpdir','-p', type=lambda x: dir_exists(parser,x),
                        help='Location of the HCP data you would like to extract from')
    parser.add_argument('--numprocs','-n',default=1,
                        help='Number of processors to use')

    return parser.parse_args()

def file_exists(parser,x):
    if not os.path.exists(x):
        parser.error("File Not Found: {0}".format(x))
    return x

def dir_exists(parser,x):
    if not os.path.isdir(x):
        parser.error('Directory Not Found: {0}'.format(x))
    return x

def extractFromSubject(subjectId, opts, extractionStrings):
    print "Extracting {0}".format(subjectId)
    tarFileName = "{0}/{1}.tar".format(opts.hcpdir,subjectId)
    with tarfile.open(tarFileName) as t:
        subdirs = [ tarinfo for tarinfo in t.getmembers() ]
        extractSubs = []
        for e in extractionStrings:
            for sd in subdirs:
                if sd.name.find(e) > -1:
                    extractSubs.append(sd)
                    
        t.extractall(members=extractSubs)

def extractHelper(args):
    return extractFromSubject(*args)
        
def main():
    opts = parseCommandLine()

    ### Read Subject File
    subjects = []
    with open(opts.subjectfile,"r") as f:
        for l in f.readlines():
            subjects.append(l.strip())

    ### Get extraction string
    extractionStrings = []
    with open(opts.extractfile,"r") as f:
        for l in f.readlines():
            extractionStrings.append(l.strip())

    hcpDirGlob = glob.glob('{0}/*.tar'.format(opts.hcpdir))
    hcpSubjects = [os.path.basename(x).replace('.tar','') for x in hcpDirGlob]

    goodSubjects = []
    for s in subjects:
        if s not in hcpSubjects:
            print "Subject {0} is not in the data set and will be skipped".format(s)
        else:
            goodSubjects.append(s)


    ### Create Output directory if it doesn't exist 
    try:
        os.makedirs(opts.outputdir)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(opts.outputdir):
            pass

    os.chdir(opts.outputdir)

    jobArgs = [(x, opts, extractionStrings) for x in goodSubjects]
    
    p = multiprocessing.Pool(opts.numprocs)
    p.map(extractFromSubject,jobArgs)

#    for s in goodSubjects:
#        print "Extracting data for subject {0}".format(s)
        #try: 
        #    os.makedirs("{0}/{1}".format(opts.outputdir,s))
        #except OSError as exc: 
        #    if exc.errno == errno.EEXIST and os.path.isdir(opts.outputdir): 
        #        pass
        #os.chdir("{0}/{1}".format(opts.outputdir,s))
#        tarFileName = "{0}/{1}.tar".format(opts.hcpdir,s)
#        with tarfile.open(tarFileName) as t:
#            subdirs = [ tarinfo for tarinfo in t.getmembers() ]
#            extractSubs = []
#            for e in extractionStrings:
#                for sd in subdirs:
#                    if sd.name.find(e) > -1:
#                        extractSubs.append(sd)
#
#            t.extractall(members=extractSubs)
        #os.chdir("..")

if __name__ == "__main__":

    main()

