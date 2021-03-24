import sys

from CodeWriter import *
from Parser import *
import os
ARITHMETICCOMMAND = "C_ARITHMETIC"
PUSHCOMMAND = "C_PUSH"
POPCOMMAND = "C_POP"
LABELCOMMAND = "C_LABEL"
GOTOCOMMAND = "C_GOTO"
IFCOMMAND = "C_IF"
FUNCCOMMAND = "C_FUNCTION"
RETURNCOMMAND = "C_RETURN"
CALLCOMMAND = "C_CALL"


def mainIteration(ifile, codeWriter):
    """
    runs over a current inputfile, and translates the vm language to asm
    :param ifile: the current inputfile
    :param codeWriter: an object of type codewriter
    :return:
    """
    fileParse = Parser(ifile)
    while fileParse.hasMoreCommands():
        fileParse.advance()
        if fileParse.commandType()==ARITHMETICCOMMAND:
            codeWriter.writeArithmetic(fileParse.arg1())
        elif fileParse.commandType()==PUSHCOMMAND:
            codeWriter.WritePushPop(PUSHCOMMAND,fileParse.arg1(),fileParse.arg2())
        elif fileParse.commandType()==POPCOMMAND:
            codeWriter.WritePushPop(POPCOMMAND,fileParse.arg1(),fileParse.arg2())
        elif fileParse.commandType()==GOTOCOMMAND:
            codeWriter.writeGoto(fileParse.arg1())
        elif fileParse.commandType() == IFCOMMAND:
            codeWriter.writeIf(fileParse.arg1())
        elif fileParse.commandType() == FUNCCOMMAND:
            codeWriter.writeFunction(fileParse.arg1(),fileParse.arg2())
        elif fileParse.commandType() == RETURNCOMMAND:
            codeWriter.writeReturn()
        elif fileParse.commandType()==CALLCOMMAND:
            codeWriter.writeCall(fileParse.arg1(),fileParse.arg2())
        elif fileParse.commandType() == LABELCOMMAND:
            codeWriter.writeLabel(fileParse.arg1())

if __name__ == '__main__':
    isDir = os.path.isdir(sys.argv[1])
    path = os.path.normpath(sys.argv[1])
    files=[path]
    if isDir is True:
        outputfile = os.path.join(path, os.path.basename(path)+".asm")
        files.clear()
        i=0
        for filename in os.listdir(path):
           if filename.endswith(".vm"):
               files.append(os.path.join(path,filename))
    else:
        outputfile, _sep, tail = files[0].rpartition(".vm")
        outputfile = outputfile + ".asm"
    ofile = open(outputfile, "w")
    codeW = CodeWriter(outputfile)
    codeW.writeInit()
    for vmFile in files:
       f = open(vmFile,"r")
       outputfile, _sep, tail = vmFile.rpartition(".vm")
       outputfile = outputfile + ".asm"
       codeW.setFileName(outputfile)
       mainIteration(f,codeW)
       f.close()
    codeW.close()




