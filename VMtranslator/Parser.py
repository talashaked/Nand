class Parser:
    """
    Parser the file
    """

    def __init__(self, inputF):
        """
        init Parser
        :param inputF: file of input
        """
        self.lines = inputF.readlines()
        self.lines = [' '.join(l.split()) if l.find("//") == -1 else ' '.join(l[:l.find("//")].split()) for l in
                      self.lines]  ## remove space and remarks
        self.cur_line = -1
        self.ArithmeticCommand = {'add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not'}


    def hasMoreCommands(self):
        """
        has more commands
        :return: true if there are
        """
        return self.cur_line < len(self.lines) - 1

    def advance(self):
        """
        advance  for next line in file
        :return: nothing
        """
        self.cur_line = self.cur_line + 1

    def commandType(self):
        """
        Returns the type of the current command.
        C_ARITHMETIC is returned for all the
        arithmetic VM commands.
        """
        cur_command = self.lines[self.cur_line]
        cur_command = cur_command.split(" ")[0]
        for arithCom in self.ArithmeticCommand:
            if arithCom in cur_command:
                return "C_ARITHMETIC"
        if 'pop' in cur_command:
            return "C_POP"
        elif 'push' in cur_command:
            return "C_PUSH"
        elif 'if-goto' in cur_command:
            return "C_IF"
        elif 'function' in cur_command:
            return "C_FUNCTION"
        elif 'call' in cur_command:
            return "C_CALL"
        elif 'label' in cur_command:
            return "C_LABEL"
        elif 'goto' in cur_command:
            return "C_GOTO"
        elif 'return' in cur_command:
            return "C_RETURN"

    def arg1(self):
        """
        Returns the first arg. of the current command.
        In the case of C_ARITHMETIC, the command itself
        (add, sub, etc.) is returned. Should not be called
        if the current command is C_RETURN
        :return: string
        """
        cur_command = self.lines[self.cur_line].split(" ")
        if len(cur_command) > 1:
            return cur_command[1]
        return cur_command[0]

    def arg2(self):
        """Returns the second argument of the current
        command. Should be called only if the current
        command is C_PUSH, C_POP, C_FUNCTION, or
        C_CALL.

        :return: string
        """
        cur_command = self.lines[self.cur_line].split(" ")
        return cur_command[2]


    def getLine(self):
        """
        get line in file
        :return: line
        """
        return self.cur_line

    def restart(self):
        """
        start from the first line
        :return:
        """
        self.cur_line = -1


class CompilationEngine:
    """
    Parser the file
    """

    def __init__(self, inputStreamFile, outputStreamFile):
        """
        init Parser
        :param inputF: file of input
        """
        self.ofile = outputStreamFile
        self.fileTokenizer = JackTokenizer(inputStreamFile)
        self.ofile.write("<class>\n")
        self.CompileClass()
        self.ofile.write("</class>\n")

    def writeInFile(self,type,whatToWrite):
        self.ofile.write("<"+type.lower()+">"+whatToWrite+"</"+type.lower()+">\n")

    def writeType(self):
        if self.fileTokenizer.tokenType() == 'KEYWORD' or self.fileTokenizer.tokenType() == 'IDENTIFIER':
            if self.fileTokenizer.tokenType() == 'KEYWORD' and (
                    self.fileTokenizer.keyword() == 'INT' or self.fileTokenizer.keyword() == 'BOOLEAN' or self.fileTokenizer.keyword() == 'CHAR'):
                self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.keyword())
            else:
                # TODO: do we need to check if the string is something????
                self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.identifier())
            self.fileTokenizer.advance()
            return 1
        return 0



    def CompileClass(self):
        self.fileTokenizer.advance()
        if self.fileTokenizer.tokenType() == 'KEYWORD':
            if self.fileTokenizer.keyword() == 'CLASS':
                self.writeInFile(self.fileTokenizer.tokenType(),"class")
                self.fileTokenizer.advance()
                if self.fileTokenizer.tokenType() == 'IDENTIFIER':
                    self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.identifier())
                    self.fileTokenizer.advance()
                    if self.fileTokenizer.tokenType()== 'SYMBOL':
                        if self.fileTokenizer.symbol() == '{':
                            self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                            self.CompileClassVarDec()
                            self.CompileSubRoutine()
                            if self.fileTokenizer.tokenType() == 'SYMBOL':
                                if self.fileTokenizer.symbol() == '}':
                                    self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())

    def CompileClassVarDec(self):
        if self.fileTokenizer.hasMoreTokens():
            self.fileTokenizer.advance()
            if self.fileTokenizer.tokenType()=='KEYWORD':
                if self.fileTokenizer.keyword() == 'STATIC' or self.fileTokenizer.keyword() == 'FIELD':
                    self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.keyword().lower())
                    self.fileTokenizer.advance()
                    # if self.fileTokenizer.tokenType()=='KEYWORD' or self.fileTokenizer.tokenType()=='IDENTIFIER':
                    #     if self.fileTokenizer.tokenType()=='KEYWORD' and (self.fileTokenizer.keyword() == 'INT' or self.fileTokenizer.keyword() == 'BOOLEAN' or self.fileTokenizer.keyword() == 'CHAR'):
                    #         self.writeInFile(self.fileTokenizer.tokenType(),self.fileTokenizer.keyword())
                    #     else:
                    #         # TODO: do we need to check if the string is something????
                    #         self.writeInFile(self.fileTokenizer.tokenType(),self.fileTokenizer.identifier())
                    if self.writeType():
                        self.fileTokenizer.advance()
                        while True:
                            if self.fileTokenizer.tokenType()=='IDENTIFIER':
                                self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.identifier())
                                self.fileTokenizer.advance()
                                if self.fileTokenizer.tokenType()=='SYMBOL':
                                    if self.fileTokenizer.symbol()==",":
                                        self.writeInFile(self.fileTokenizer.tokenType(),self.fileTokenizer.symbol())
                                    elif self.fileTokenizer.symbol() == ";":
                                        self.writeInFile("symbol",";")
                                        break
                        self.CompileClassVarDec()

    def CompileSubRoutine(self):
        if self.fileTokenizer.tokenType()=="KEYWORD":
            if self.fileTokenizer.keyword()=="CONSTRUCTOR" or self.fileTokenizer.keyword()=="FUNCTION" or self.fileTokenizer.keyword()=="METHOD":
                self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.keyword())
                self.fileTokenizer.advance()
                if self.fileTokenizer.tokenType()=="KEYWORD":
                   if self.fileTokenizer.keyword()=="VOID" or self.writeType():
                        if self.fileTokenizer.keyword() == "VOID":
                            self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.keyword())
                        self.fileTokenizer.advance()
                        if self.fileTokenizer.tokenType() == 'IDENTIFIER':
                            # todo : should i check it?????
                            self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.identifier())
                            self.fileTokenizer.advance()
                            if self.fileTokenizer.tokenType() == 'SYMBOL':
                                if self.fileTokenizer.symbol() == '{':
                                    self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                                    self.CompileParameterList()
                                    if self.fileTokenizer.tokenType() == 'SYMBOL':
                                        if self.fileTokenizer.symbol() == '}':
                                            self.writeInFile(self.fileTokenizer.tokenType(),
                                                             self.fileTokenizer.symbol())
                                            self.fileTokenizer.advance()
                                            self.CompileSubroutineBody()

    def CompileParameterList(self):
        if self.writeType():
            if self.fileTokenizer.tokenType()=="IDENTIFIER":
                self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.identifier())
                self.fileTokenizer.advance()
                if self.fileTokenizer.tokenType() == 'SYMBOL':
                    if self.fileTokenizer.symbol() == ",":
                        self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                        self.fileTokenizer.advance()
                        self.CompileParameterList()

    def CompileSubroutineBody(self):
        if self.fileTokenizer.tokenType() == 'SYMBOL':
            if self.fileTokenizer.symbol() == '{':
                self.writeInFile(self.fileTokenizer.tokenType(), self.fileTokenizer.symbol())
                self.fileTokenizer.advance()
                self.CompileVarDec()
                self.CompileStatements()
                if self.fileTokenizer.tokenType() == 'SYMBOL':
                    if self.fileTokenizer.symbol() == '}':
                        self.writeInFile(self.fileTokenizer.tokenType(),
                                         self.fileTokenizer.symbol())
                        self.fileTokenizer.advance()

    def CompileVarDec(self):


    def CompileStatements(self):
        fd













