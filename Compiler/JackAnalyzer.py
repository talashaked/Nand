import sys
import os

from CompilationEngine import CompilationEngine


if __name__ == '__main__':
    isDir = os.path.isdir(sys.argv[1])
    files=[sys.argv[1]]
    if isDir is True:
        files.clear()
        i=0
        for filename in os.listdir(sys.argv[1]):
           if filename.endswith(".jack"):
               files.append(os.path.join(sys.argv[1],filename))
    for jackFile in files:
       f = open(jackFile,"r")
       outputfile,_sep,tail = jackFile.rpartition(".jack")
       outputfile = outputfile + ".vm"
       ofile = open(outputfile,"w")
       CompilationEngine(f,ofile)
       ofile.close()
       f.close()