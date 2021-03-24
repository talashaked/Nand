from SymbolTable import SymbolTable

from JackTokenizer import JackTokenizer
from VMWriter import VMWriter


class CompilationEngine:
    ifLabels=0
    strIf = 'IfLabel'
    whileLabels =0
    strWhile = 'whileLabel'
    className = ''
    """
    Parser the file
    """
    operatorList = {'+','-','*','/','&','|','<','>','='}
    def __init__(self, inputStreamFile, outputStreamFile):
        """
        init the compilationEngine
        :param inputF: file of input
        """
        self.ofile = outputStreamFile
        self.fileTokenizer = JackTokenizer(inputStreamFile)
        self.vmWriter = VMWriter(outputStreamFile)
        self.classSymTable = SymbolTable()
        self.funcTypes={}
        self.CompileClass()




    def writeInFile(self,type,whatToWrite):
        """
        write the template <type>what</type> in the ofile
        :param type: the type
        :param whatToWrite: what
        :return:
        """
        type = type.lower()
        if type == "stringconstant":
            type = "stringConstant"
        elif type == "integerconstant":
            type = "integerConstant"
        self.ofile.write("<"+type+"> "+whatToWrite+" </"+type+">\n")

    def writeType(self):
        """
        if the given token is some sort of type, this function would write it and advance, and return true, else false
        :return:
        """
        type = ""
        if self.fileTokenizer.tokenType() == 'KEYWORD' or self.fileTokenizer.tokenType() == 'IDENTIFIER':
            if self.fileTokenizer.tokenType() == 'KEYWORD' and (
                    self.fileTokenizer.keyword() == 'INT' or self.fileTokenizer.keyword() == 'BOOLEAN' or self.fileTokenizer.keyword() == 'CHAR'):
                type = self.fileTokenizer.keyword()
            else:
                type = self.fileTokenizer.identifier()
            self.fileTokenizer.advance()
        return type

    def CompileClass(self):
        """
        compiles the class section
        :return:
        """
        self.fileTokenizer.advance()
        if self.fileTokenizer.tokenType() == "KEYWORD":
            if self.fileTokenizer.keyword() == 'class':
                self.fileTokenizer.advance()
                if self.fileTokenizer.tokenType() == 'IDENTIFIER':
                    self.className = self.fileTokenizer.identifier()
                    self.vmWriter.WriteLabel(self.className)
                    self.fileTokenizer.advance()
                    if self.fileTokenizer.tokenType()== 'SYMBOL':
                        if self.fileTokenizer.symbol() == '{':
                            self.fileTokenizer.advance()
                            if self.fileTokenizer.tokenType() == 'KEYWORD':
                                while (self.fileTokenizer.keyword() == 'static' or self.fileTokenizer.keyword() == 'field'):
                                    self.CompileClassVarDec()
                            if self.fileTokenizer.tokenType() == 'KEYWORD':
                                while (self.fileTokenizer.keyword()=="constructor" or self.fileTokenizer.keyword()=="function" or self.fileTokenizer.keyword()=="method"):
                                    self.classSymTable.startSubroutine()
                                    self.CompileSubRoutineDec(self.className)
                            if self.fileTokenizer.tokenType() == 'SYMBOL':
                                if self.fileTokenizer.symbol() == '}':
                                    return

    def CompileClassVarDec(self):
        """
        compiles the class varDEc section
        :return: 
        """""
        keyw = self.fileTokenizer.keyword().upper()
        # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.keyword().lower())
        self.fileTokenizer.advance()
        curType = self.writeType()
        if curType!="":
            while True:
                if self.fileTokenizer.tokenType()=='IDENTIFIER':
                    # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.identifier())
                    self.classSymTable.define(self.fileTokenizer.identifier(),curType,keyw)
                    self.fileTokenizer.advance()
                    if self.fileTokenizer.tokenType()=='SYMBOL':
                        if self.fileTokenizer.symbol()==",":
                            # self.writeInFile(self.fileTokenizer.tokenType(),self.fileTokenizer.symbol())
                            self.fileTokenizer.advance()
                        elif self.fileTokenizer.symbol() == ";":
                            # self.writeInFile(self.fileTokenizer.tokenType(),";")
                            self.fileTokenizer.advance()
                            break


    def CompileSubRoutineDec(self,className):
        """
        compiles to subroutineDec
        :return:
        """
        # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.keyword())
        keyW = self.fileTokenizer.keyword()
        self.fileTokenizer.advance()
        if self.fileTokenizer.tokenType()=="KEYWORD" or "IDENTIFIER":
           retType = self.writeType()
           if retType!="" or self.fileTokenizer.keyword()=="void":
           # if self.fileTokenizer.keyword()=="void" or self.writeType():
                if self.fileTokenizer.keyword() == "void":
                    # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.keyword())
                    retType = "void"
                    self.fileTokenizer.advance()
                if self.fileTokenizer.tokenType() == 'IDENTIFIER':
                    # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.identifier())
                    funcName = self.fileTokenizer.identifier()
                    if retType == "void":
                        self.funcTypes[funcName] = [True,keyW]
                    else:
                        self.funcTypes[funcName] = [False, keyW]
                    self.fileTokenizer.advance()
                    if self.fileTokenizer.tokenType() == 'SYMBOL':
                        if self.fileTokenizer.symbol() == '(':
                            # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                            self.fileTokenizer.advance()
                            # self.ofile.write("<parameterList>\n")
                            if keyW == "method":
                                self.classSymTable.define('this', self.className, 'ARG')
                            self.CompileParameterList()
                            numArgs = self.classSymTable.varCount("ARG")
                            # self.ofile.write("</parameterList>\n")
                            if self.fileTokenizer.tokenType() == 'SYMBOL':
                                if self.fileTokenizer.symbol() == ')':
                                    # self.writeInFile(self.fileTokenizer.tokenType(),
                                    #                  self.fileTokenizer.symbol())
                                    self.fileTokenizer.advance()
                                    # self.ofile.write("<subroutineBody>\n")
                                    self.CompileSubroutineBody(keyW,funcName,className)
                                    # self.ofile.write("</subroutineBody>\n")

    def CompileParameterList(self):
        """
        compiles the parameter list
        :return:
        """
        argType = self.writeType()
        if argType!="":
            if self.fileTokenizer.tokenType()=="IDENTIFIER":
                # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.identifier())
                self.classSymTable.define(self.fileTokenizer.identifier(),argType,"ARG")
                self.fileTokenizer.advance()
                if self.fileTokenizer.tokenType() == 'SYMBOL':
                    if self.fileTokenizer.symbol() == ",":
                        # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                        self.fileTokenizer.advance()
                        self.CompileParameterList()

    def CompileSubroutineBody(self,keyW,funcName,className):
        """
        compiles the subroutineBody
        :return:
        """
        countLCLs = 0
        if self.fileTokenizer.tokenType() == 'SYMBOL':
            if self.fileTokenizer.symbol() == '{':
                # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                self.fileTokenizer.advance()
                if self.fileTokenizer.tokenType() == "KEYWORD":
                    while self.fileTokenizer.keyword() == "var":
                        # self.ofile.write("<varDec>\n")
                        countLCLs += self.CompileVarDec()
                        # self.ofile.write("</varDec>\n")
                        if self.fileTokenizer.tokenType() != "KEYWORD":
                            break
                if keyW == "method":
                    self.vmWriter.writeFunction(className + '.' + funcName, countLCLs)
                    self.vmWriter.writePush("ARG", '0')
                    self.vmWriter.writePop("POINTER", '0')
                elif keyW == "function":
                    self.vmWriter.writeFunction(className + '.' + funcName, countLCLs)
                else:
                    self.vmWriter.writeFunction(className + '.' + funcName, countLCLs)
                    place = self.classSymTable.varCount("FIELD")
                    self.vmWriter.writePush("CONST", str(place))
                    self.vmWriter.WriteCall("Memory.alloc", '1')
                    self.vmWriter.writePop("POINTER", '0')

                # self.ofile.write("<statements>\n")
                self.CompileStatements()
                # self.ofile.write("</statements>\n")
                if self.fileTokenizer.tokenType() == 'SYMBOL':
                    if self.fileTokenizer.symbol() == '}':
                        # self.writeInFile(self.fileTokenizer.tokenType(),
                                         # self.fileTokenizer.symbol())
                        self.fileTokenizer.advance()

    def CompileVarDec(self):
        """
        compiles the varDec
        :return:
        """
        # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.keyword())
        self.fileTokenizer.advance()
        count = 0
        bool = True
        curType = self.writeType()
        if (curType!=""):
            while bool:
                if self.fileTokenizer.tokenType() == "IDENTIFIER":
                    # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.identifier())
                    self.classSymTable.define(self.fileTokenizer.identifier(),curType,"VAR")
                    count+=1
                    self.fileTokenizer.advance()
                    if self.fileTokenizer.tokenType() == 'SYMBOL':
                        if self.fileTokenizer.symbol() == ",":
                            # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                            self.fileTokenizer.advance()
                        elif self.fileTokenizer.symbol() == ";":
                            # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                            self.fileTokenizer.advance()
                            bool = False
            return count

    def CompileStatements(self):
        """
        compiles the statements
        :return:
        """
        if self.fileTokenizer.tokenType() == "KEYWORD":
            if self.fileTokenizer.keyword() == "let":
                # self.ofile.write("<letStatement>\n")
                self.CompileLetStatement()
                # self.ofile.write("</letStatement>\n")
                self.CompileStatements()
            elif self.fileTokenizer.keyword() == "if":
                # self.ofile.write("<ifStatement>\n")
                curLabel = self.CompileIfStatement()
                self.vmWriter.WriteLabel("else"+self.strIf+str(curLabel))
                if self.fileTokenizer.tokenType() == "KEYWORD":
                    if self.fileTokenizer.keyword() == "else":
                        self.CompileElseStatement()
                # self.ofile.write("</ifStatement>\n")
                self.vmWriter.WriteLabel('endof'+self.strIf+str(curLabel))
                self.CompileStatements()
            elif self.fileTokenizer.keyword() == "while":
                # self.ofile.write("<whileStatement>\n")
                self.CompileWhileStatement()
                # self.ofile.write("</whileStatement>\n")
                self.CompileStatements()
            elif self.fileTokenizer.keyword() == "do":
                # self.ofile.write("<doStatement>\n")
                self.CompileDoStatement()
                # self.ofile.write("</doStatement>\n")
                self.CompileStatements()
            elif self.fileTokenizer.keyword() == "return":
                # self.ofile.write("<returnStatement>\n")
                self.CompileReturnStatement()
                # self.ofile.write("</returnStatement>\n")
                self.CompileStatements()

    def CompileLetStatement(self):
        """
        compiles the let statement
        :return:
        """
        # self.writeInFile(self.fileTokenizer.tokenType(),self.fileTokenizer.identifier())
        self.fileTokenizer.advance()
        if self.fileTokenizer.tokenType()=="IDENTIFIER" and self.classSymTable.indexOf(self.fileTokenizer.identifier()) is not None:
            lval = self.fileTokenizer.identifier()
            # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.identifier())
            self.fileTokenizer.advance()
            if self.fileTokenizer.tokenType() == 'SYMBOL':
                if self.fileTokenizer.symbol() == "[":
                    # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                    self.fileTokenizer.advance()
                    if self.classSymTable.kindOf(lval) == 'FIELD':
                        self.vmWriter.writePush("THIS", self.classSymTable.indexOf(lval))
                    else:
                        self.vmWriter.writePush(self.classSymTable.kindOf(lval),self.classSymTable.indexOf(lval))
                    # self.ofile.write("<expression>\n")
                    self.CompileExpression()
                    # self.ofile.write("</expression>\n")
                    if self.fileTokenizer.tokenType() == 'SYMBOL':
                        if self.fileTokenizer.symbol() == "]":
                            # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                            self.vmWriter.WriteArithmetic("ADD")
                            self.fileTokenizer.advance()
                            self.secondPartOfLetStatement()
                            self.vmWriter.writePop("TEMP", '0')
                            self.vmWriter.writePop("POINTER", '1')
                            self.vmWriter.writePush("TEMP", '0')
                            self.vmWriter.writePop("THAT", '0')
                else:
                    self.secondPartOfLetStatement()
                    if self.classSymTable.kindOf(lval) == "FIELD":
                        self.vmWriter.writePop('THIS', self.classSymTable.indexOf(lval))
                    else:
                        self.vmWriter.writePop(self.classSymTable.kindOf(lval),self.classSymTable.indexOf(lval))

    def secondPartOfLetStatement(self):
        """
        compiles an inner section of the let statement, from the '=' and following
        :return:
        """
        if self.fileTokenizer.tokenType() == 'SYMBOL':
            if self.fileTokenizer.symbol() == "=":
                # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                self.fileTokenizer.advance()
                # self.ofile.write("<expression>\n")
                self.CompileExpression()
                # self.ofile.write("</expression>\n")
                if self.fileTokenizer.tokenType() == 'SYMBOL':
                    if self.fileTokenizer.symbol() == ";":
                        # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                        self.fileTokenizer.advance()


    def CompileIfStatement(self):
        """
        compiles the if statement
        :return:
        """
        self.writeIfOrWhileIncapsulation()
        self.vmWriter.WriteIf(self.strIf+str(self.ifLabels))
        self.vmWriter.WriteGoto("else"+self.strIf+str(self.ifLabels))
        self.vmWriter.WriteLabel(self.strIf+str(self.ifLabels))
        selfLabelsRemeber = self.ifLabels
        self.ifLabels+=1
        self.writeStatementsIncapsulation()
        self.vmWriter.WriteGoto("endof"+self.strIf+str(selfLabelsRemeber))
        return selfLabelsRemeber

    def writeIfOrWhileIncapsulation(self):
        """
        compiles the if or while incapsulation
        :return:
        """
        # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.identifier().lower())
        self.fileTokenizer.advance()
        if self.fileTokenizer.tokenType() == 'SYMBOL':
            if self.fileTokenizer.symbol() == "(":
                # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                self.fileTokenizer.advance()
                # self.ofile.write("<expression>\n")
                self.CompileExpression()
                # self.ofile.write("</expression>\n")
                if self.fileTokenizer.tokenType() == 'SYMBOL':
                    if self.fileTokenizer.symbol() == ")":
                        # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                        self.fileTokenizer.advance()
                        return

    def writeStatementsIncapsulation(self):
        """
        write statements incapsulation
        :return:
        """
        if self.fileTokenizer.tokenType() == 'SYMBOL':
            if self.fileTokenizer.symbol() == "{":
                # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                self.fileTokenizer.advance()
                # self.ofile.write("<statements>\n")
                self.CompileStatements()
                # self.ofile.write("</statements>\n")
                if self.fileTokenizer.tokenType() == 'SYMBOL':
                    if self.fileTokenizer.symbol() == "}":
                        # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                        self.fileTokenizer.advance()

    def CompileElseStatement(self):
        """
        compile the else statement
        :return:
        """
        # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.identifier().lower())
        self.fileTokenizer.advance()
        self.writeStatementsIncapsulation()

    def CompileWhileStatement(self):
        """
        compiles the while sttement
        :return:
        """
        self.vmWriter.WriteLabel(self.strWhile+str(self.whileLabels)+".cond")
        self.writeIfOrWhileIncapsulation()
        self.vmWriter.WriteIf(self.strWhile+str(self.whileLabels))
        self.vmWriter.WriteGoto(self.strWhile + str(self.whileLabels) + ".end")
        self.vmWriter.WriteLabel(self.strWhile+str(self.whileLabels))
        rememberWhileLabael = self.whileLabels
        self.whileLabels+=1
        self.writeStatementsIncapsulation()
        self.vmWriter.WriteGoto(self.strWhile + str(rememberWhileLabael) + ".cond")
        self.vmWriter.WriteLabel(self.strWhile+str(rememberWhileLabael)+".end")

    def CompileDoStatement(self):
        """
        compiles the do statement
        :return:
        """
        # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.keyword().lower())
        self.fileTokenizer.advance()
        if self.fileTokenizer.tokenType() == "IDENTIFIER":
            strName = self.fileTokenizer.identifier()
            self.fileTokenizer.advance()
            self.compileSubroutineCall(strName)
            if self.fileTokenizer.tokenType() == 'SYMBOL':
                if self.fileTokenizer.symbol() == ";":
                    # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                    self.vmWriter.writePop("TEMP",'0')
                    self.fileTokenizer.advance()

    def CompileReturnStatement(self):
        """
        compiles the return statement
        :return:
        """
        # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.identifier().lower())
        self.fileTokenizer.advance()
        if self.fileTokenizer.symbol() != ";":
            # self.ofile.write("<expression>\n")
            self.CompileExpression()
            # self.ofile.write("</expression>\n")
        else:
            self.vmWriter.writePush('CONST','0')
        if self.fileTokenizer.tokenType() == 'SYMBOL':
            if self.fileTokenizer.symbol() == ";":
                # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                self.vmWriter.writeReturn()
                self.fileTokenizer.advance()

    def CompileExpression(self):
        """
        compiles expression
        :return:
        """
        # self.ofile.write("<term>\n")
        self.CompileTerm()
        # self.ofile.write("</term>\n")
        arith = ''
        if self.fileTokenizer.tokenType() == 'SYMBOL':
            while self.fileTokenizer.symbol() in self.operatorList:
                if self.fileTokenizer.symbol() == "<":
                    # self.writeInFile(self.fileTokenizer.tokenType(), "&lt;")
                    arith = "LT"
                elif self.fileTokenizer.symbol() == ">":
                    arith = 'GT'
                    # self.writeInFile(self.fileTokenizer.tokenType(), "&gt;")
                elif self.fileTokenizer.symbol() == "&":
                    # self.writeInFile(self.fileTokenizer.tokenType(), "&amp;")
                    arith = "AND"
                elif self.fileTokenizer.symbol() == "+":
                    arith = "ADD"
                elif self.fileTokenizer.symbol() == "-":
                    arith = "SUB"
                elif self.fileTokenizer.symbol() == "/":
                    arith = 'divide'
                elif self.fileTokenizer.symbol() == "|":
                    arith = "OR"
                elif self.fileTokenizer.symbol() == "=":
                    arith = "EQ"
                elif self.fileTokenizer.symbol() == "*":
                    arith = 'multiply'
                self.fileTokenizer.advance()
                # self.ofile.write("<term>\n")
                self.CompileTerm()
                # self.ofile.write("</term>\n")
                if arith!='':
                    if arith == 'multiply':
                        self.vmWriter.WriteCall('Math.multiply','2')
                    elif arith == 'divide':
                        self.vmWriter.WriteCall('Math.divide', '2')
                    else:
                        self.vmWriter.WriteArithmetic(arith)
                    arith = ''
                if self.fileTokenizer.tokenType() != 'SYMBOL':
                    break

    def CompileTerm(self):
        """
        compiles terms
        :return:
        """
        if self.fileTokenizer.tokenType() == "INT_CONST":
            # self.writeInFile("integerConstant", self.fileTokenizer.intVal())
            self.vmWriter.writePush("CONST",self.fileTokenizer.intVal())
            self.fileTokenizer.advance()
        elif self.fileTokenizer.tokenType() == "STRING_CONST":
            # self.writeInFile("stringConstant", self.fileTokenizer.stringVal())
            self.vmWriter.writePush("CONST",len(self.fileTokenizer.stringVal()))
            self.vmWriter.WriteCall("String.new", 1)
            for i in range(len(self.fileTokenizer.stringVal())):
                self.vmWriter.writePush("CONST",ord(self.fileTokenizer.stringVal()[i]))
                self.vmWriter.WriteCall("String.appendChar", 2)
            self.fileTokenizer.advance()
        elif self.fileTokenizer.tokenType() == "KEYWORD":
            if self.fileTokenizer.keyword() == "true" or "false" or "null" or "this":
            #     # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.keyword())
                if self.fileTokenizer.keyword() == "true":
                    self.vmWriter.writePush("CONST", '1')
                    self.vmWriter.WriteArithmetic('NEG')
                elif self.fileTokenizer.keyword() == "false":
                    self.vmWriter.writePush("CONST", '0')
                elif self.fileTokenizer.keyword() == "null":
                    self.vmWriter.writePush("CONST", '0')
                elif self.fileTokenizer.keyword() == "this":
                    self.vmWriter.writePush("POINTER", '0')
                self.fileTokenizer.advance()
        elif self.fileTokenizer.tokenType() == "IDENTIFIER":
            # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.identifier())
            strName = self.fileTokenizer.identifier()
            self.fileTokenizer.advance()
            if self.fileTokenizer.tokenType() == 'SYMBOL':
                if self.fileTokenizer.symbol() == "[":
                    if self.classSymTable.kindOf(strName) == "FIELD":
                        self.vmWriter.writePush('THIS', self.classSymTable.indexOf(strName))
                    else:
                        self.vmWriter.writePush(self.classSymTable.kindOf(strName),self.classSymTable.indexOf(strName))
                    # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                    self.fileTokenizer.advance()
                    # self.ofile.write("<expression>\n")
                    self.CompileExpression()
                    # self.ofile.write("</expression>\n")
                    if self.fileTokenizer.tokenType() == 'SYMBOL':
                        if self.fileTokenizer.symbol() == "]":
                            # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                            self.vmWriter.WriteArithmetic("ADD")
                            self.vmWriter.writePop("POINTER",'1')
                            self.vmWriter.writePush("THAT",'0')
                            self.fileTokenizer.advance()
                elif self.fileTokenizer.symbol() == "(" or self.fileTokenizer.symbol() == ".":
                    self.compileSubroutineCall(strName)
                else:
                    if self.classSymTable.kindOf(strName) == 'FIELD':
                        self.vmWriter.writePush("THIS", self.classSymTable.indexOf(strName))
                    elif self.classSymTable.kindOf(strName) == "ARG" or self.classSymTable.kindOf(strName) == "STATIC":
                        self.vmWriter.writePush(self.classSymTable.kindOf(strName), self.classSymTable.indexOf(strName))
                    elif self.classSymTable.kindOf(strName) == "LOCAL":
                        self.vmWriter.writePush(self.classSymTable.kindOf(strName), self.classSymTable.indexOf(strName))
        elif self.fileTokenizer.tokenType()=="SYMBOL":
            if self.fileTokenizer.symbol()=="(":
                # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                self.fileTokenizer.advance()
                # self.ofile.write("<expression>\n")
                self.CompileExpression()
                # self.ofile.write("</expression>\n")
                if self.fileTokenizer.tokenType() == "SYMBOL":
                    if self.fileTokenizer.symbol() == ")":
                        # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                        self.fileTokenizer.advance()
            elif self.fileTokenizer.symbol() == "-" or "~":
                str =""
                if self.fileTokenizer.symbol() == "-":
                    str = "NEG"
                else:
                      str = "NOT"
                # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                self.fileTokenizer.advance()
                # self.ofile.write("<term>\n")
                self.CompileTerm()
                # self.ofile.write("</term>\n")
                self.vmWriter.WriteArithmetic(str)

    def compileSubroutineCall(self,strName):
        """
        compiles subroutine call
        :return:
        """
        if self.fileTokenizer.tokenType() == 'SYMBOL':
            if self.fileTokenizer.symbol() == ".":
                # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                self.fileTokenizer.advance()
                if self.fileTokenizer.tokenType() == "IDENTIFIER":
                    # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.identifier())
                    if self.classSymTable.indexOf(strName) is not None:
                        strNameCat = self.classSymTable.typeOf(strName)+"."+ self.fileTokenizer.identifier()
                    else:
                        strNameCat = strName+"."+ self.fileTokenizer.identifier()
                    self.fileTokenizer.advance()
                    self.innerSubroutineNameCall(strNameCat,strName)
            else:
                self.innerSubroutineNameCall(strName,"")

    def innerSubroutineNameCall(self, funcName,classOrObjName):
        """
        compiles the second part of the subroutine call, from the "(" and forward
        :return:
        """
        n=0
        if self.fileTokenizer.tokenType() == 'SYMBOL':
            if self.fileTokenizer.symbol() == "(":
                # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                self.fileTokenizer.advance()
                # self.ofile.write("<expressionList>\n")
                if self.funcTypes.get(funcName) == "METHOD" or self.classSymTable.indexOf(classOrObjName) is not None:
                    if classOrObjName is not "":
                        if self.classSymTable.kindOf(classOrObjName) == 'FIELD':
                            self.vmWriter.writePush("THIS", self.classSymTable.indexOf(classOrObjName))
                        else:
                            self.vmWriter.writePush(self.classSymTable.kindOf(classOrObjName),self.classSymTable.indexOf(classOrObjName))
                        n+=1
                elif classOrObjName is "":
                    self.vmWriter.writePush('POINTER',
                                            '0')
                    n += 1
                    funcName = self.className + "." + funcName
                n += self.CompileExpressionList(0)
                # self.ofile.write("</expressionList>\n")
                if self.fileTokenizer.symbol() == ")":
                    self.vmWriter.WriteCall(funcName, n)
                    if self.funcTypes.get(funcName) is not None :  ## this function is a void func
                        if self.funcTypes.get(funcName)[0]:
                            self.vmWriter.writePop("TEMP", '0')
                    self.fileTokenizer.advance()

    def CompileExpressionList(self,count):
        """
        cimpiles expression list
        :return:
        """
        if self.fileTokenizer.tokenType() == 'SYMBOL':
            if self.fileTokenizer.symbol() == ")":
                return count
        # self.ofile.write("<expression>\n")
        self.CompileExpression()
        count+=1
        # self.ofile.write("</expression>\n")
        if self.fileTokenizer.tokenType() == 'SYMBOL':
            if self.fileTokenizer.symbol() == ",":
                # self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                self.fileTokenizer.advance()
                return self.CompileExpressionList(count)
            elif self.fileTokenizer.symbol() == ')':
                return count






















