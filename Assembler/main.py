import sys
from Code import *
from Parser import *
from SymbolTable import *
import os


def makeNum15Bin(num):
    """
    convert num for binary
    :param num:
    :return: binary string
    """
    numString = bin(num)
    numString = numString[2:]
    length = len(numString)
    for i in range(0, 15 - length):
        numString = "0" + numString
    numString = "0" + numString
    return numString


def AcommandResponse(symbol,symTable):
    """
    check symbol
    :param symbol: symbol
    :param symTable: present of symbol
    :return: binary represent
    """
    try:
        line = int(symbol)
        return makeNum15Bin(line)
    except ValueError:
        if symTable.contains(symbol):
            return makeNum15Bin(symTable.getAddress(symbol))
        else:
            symTable.addVariable(symbol)
            return makeNum15Bin(symTable.getAddress(symbol))

def firstIterationParser(parser):
    """
    first iteration
    :param parser: parser of file
    :return: symbol table
    """
    symbolTable = SymbolTable()
    count =0
    while parser.hasMoreCommands() is True:
        parser.advance()
        if(parser.commandType() == "L_COMMAND"):
            symbolTable.addEntry(parser.symbol(),parser.getLine()-count)
            count+=1
    return symbolTable


def mainParse(file, symbolTable, ofile, parser):
    """
    main praser
    :param file: file for
    :param symbolTable: symbole table
    :param ofile: output file
    :param parser:parser of file
    :return:
    """
    code  = Code()
    while parser.hasMoreCommands() is True:
        parser.advance()
        if parser.commandType() == "L_COMMAND":
            continue
        elif parser.commandType() == "A_COMMAND":
            line = AcommandResponse(parser.symbol(),symbolTable)
            ofile.write(line + "\n")
        elif parser.commandType() == "C_COMMAND":
            dest = code.dest(parser.dest())
            comp = code.comp(parser.comp())
            jump = code.jump(parser.jump())
            line = "101" + comp + dest + jump if parser.special_c() else  "111" + comp + dest + jump
            ofile.write(line + "\n")


if __name__ == '__main__':
    isDir = os.path.isdir(sys.argv[1])
    files=[sys.argv[1]]
    if isDir is True:
        files.clear()
        i=0
        for filename in os.listdir(sys.argv[1]):
           if filename.endswith(".asm"):
               files.append(os.path.join(sys.argv[1],filename))
    for asmFile in files:
       f = open(asmFile,"r")
       outputfile,_sep,tail = asmFile.rpartition(".asm")
       outputfile = outputfile + ".hack"
       ofile = open(outputfile,"w")
       parser = Parser(f)
       symTable = firstIterationParser(parser)
       parser.restart()
       mainParse(f,symTable,ofile,parser)
       ofile.close()
       f.close()





