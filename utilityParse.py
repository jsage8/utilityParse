#!/usr/bin/python

import sys
import os
import re
import gzip

def fastAExtract(fileHandle):
  """-------------------------------------------------------------------
  fastAExtract()
  Process a fastA fileHandle 
  return a count of the number of sequnces and the total number of 
  residues in those sequences.
  -------------------------------------------------------------------"""
  seq_res = []
  seqCount = 0
  resCount = 0

  # Scan through file line by line counting sequences and residues  
  for line in fileHandle:
    matchSeq = re.search(r'^>', line)
    if matchSeq:
      seqCount += 1
    else:
      resCount += len(line.strip())
  
  # Close the file    
  fileHandle.close()
  
  # Store seqCount and resCount in seq_res and return it 
  seq_res.append(seqCount)
  seq_res.append(resCount)
  return seq_res
  
def fastQExtract(fileHandle):
  """-------------------------------------------------------------------
  fastQExtract()
  Process a fastQ fileHandle 
  Return a count of the number of sequnces and the total number of 
  residues in those sequences. This method uses a four count to 
  determine what type of information to expect on the current line.
  When the count is 4 there should be a new header line, however, an
  additional check for '@' at the beginning of the line is performed.
  If not found, the count will exceed 4 and continue to check every
  subsequent line for a new header line. This prevents comments or
  other line breaks from disrupting the count. Residue sequences should
  always be found when the count is 1 (directly after a new header).
  -------------------------------------------------------------------"""
  seq_res = []
  seqCount = 0
  resCount = 0
  
  # Scan through file line by line counting sequences and residues
  fourCount = 4
  for line in fileHandle:
    if fourCount >= 4:
      matchSeq = re.search(r'^@', line)
      if matchSeq:
        seqCount += 1
        fourCount = 0
    elif fourCount == 1:
      resCount += len(line.strip())
    fourCount += 1
  
  # Close the file    
  fileHandle.close()
  
  # Store seqCount and resCount in seq_res and return it 
  seq_res.append(seqCount)
  seq_res.append(resCount)
  return seq_res


def main():
  """------------------------------------------------------------------- 
  main()
  Command-line parsing
  Check for the -summary argument and load in all other arguments as 
  possible files.

  File Opening
  Check to see if a file exists, if it is compressed, and whether it is
  fastA or fastQ.

  Output
  If -summary argument is true print results to summary.txt. Otherwise,
  print results to console. 
  -------------------------------------------------------------------"""
  # Make a list of command line arguments, omitting the [0] element 
  # which is the script itself. 
  args = sys.argv[1:]

  # Exit if there are no arguments
  if not args:
    sys.exit(1)

  # Notice the summary flag and remove it from args if it is present.
  summary = False
  if args[0] == '-summary':
    summary = True
    del args[0]
    
  # Exit if there are no arguments
  if not args:
    sys.exit(1)

  # Check to see if the summary file should be overwritten or appended
  newRun = True

  # For each filename, get the number of sequences and residues, then 
  # either print the text output or write it to a summary file
  for filename in args:
    # Check to see if the file exists
    if os.path.isfile(filename):
      # Check if the file is a compressed .gz file and open accordingly
      isCompressed = re.search(r'.gz$', filename)
      if isCompressed:
        fileHandle = gzip.open(filename, 'rt')
      else:
        fileHandle = open(filename, 'rU')
      
      #Check the file format and call the respective extraction method
      isFastQ = re.search(r'.fastq$|.fq$|.fastq.gz$|.fq.gz$', filename)
      isFastA = re.search(r'.fasta$|.fa$|.fasta.gz$|.fa.gz$', filename)
      if isFastQ:
        info = fastQExtract(fileHandle)
      elif isFastA:
        info = fastAExtract(fileHandle)
      else:
        print 'WARNING: ' + filename + ' is not a recognized format!'
      
      # If the summary argument is given make a summary.txt file
      if summary:
        # Overwrite summary.txt for a new run
        if newRun:
          fileHandle = open('summary.txt', 'w')
          fileHandle.write('Summary for: ' + filename + '\nTotal sequences found: ' + `info[0]` + '\nTotal residues found: ' + `info[1]` + '\n\n')
          fileHandle.close()
        # Append to summary.txt for additional file arguments
        else:
          fileHandle = open('summary.txt', 'a')
          fileHandle.write('Summary for: ' + filename + '\nTotal sequences found: ' + `info[0]` + '\nTotal residues found: ' + `info[1]` + '\n\n')
          fileHandle.close()
      else:
        print 'Summary for: ' + filename + '\nTotal sequences found: ' + `info[0]` + '\nTotal residues found: ' + `info[1]` + '\n'
      newRun = False
    # If the file does not exist print a warning 
    else:
      print 'WARNING: ' + filename + ' does not exist!'
  
if __name__ == '__main__':
  main()
