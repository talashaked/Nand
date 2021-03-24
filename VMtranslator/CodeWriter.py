import os
class CodeWriter:
    def __init__(self, ofileStr):
        self.ofile = open(ofileStr,'w')
        self.ArithmeticCommand = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']
        self.count =0  ## for the labels in the arithmetic functions
        self.countCall = 0
        self.curFuncName = ""



    def setFileName(self, fileName):
        """
        writes the current filename in the output file
        :param fileName:
        :return:
        """
        self.ofile.write("//"+fileName+"\n")
        self.cur_fileName = os.path.basename(fileName).split(".")[0]

    def writeArithmetic(self, s):
        """
        writes the matching arithmetic command in the output
        :param s: the arithmetic command given
        :return:
        """
        count = self.count
        if s == self.ArithmeticCommand[0]:
            self.ofile.write("@SP\nA=M\nA=A-1\nD=M\nA=A-1\nM=D+M\n@SP\nM=M-1\n")
        elif s == self.ArithmeticCommand[1]:
            self.ofile.write("@SP\nA=M\nA=A-1\nD=M\nA=A-1\nM=M-D\n@SP\nM=M-1\n")
        elif s==self.ArithmeticCommand[2]:
            self.ofile.write("@SP\nA=M\nA=A-1\nM=-M\n")
        elif s==self.ArithmeticCommand[3]:
            self.ofile.write("@SP\nA=M-1\nA=A-1\nD=M\n@FIRSTNONNEG"+str(count)+"\nD;JGE\n@FIRSTNEG"+str(count)+"\n0;JMP\n(FIRSTNONNEG"+str(count)+")\n"
                             "@SP\nA=M-1\nD=M\n@SAMESIGN"+str(count)+"\nD;JGE\n@SECONDNEGFIRSTNONNEG"+str(count)+"\n0;JMP\n(FIRSTNEG"+str(count)+")\n@SP\n"
                             "A=M-1\nD=M\n@SECONDNONNEGFIRSTNEG"+str(count)+"\nD;JGE\n@SAMESIGN"+str(count)+"\n0;JMP\n(SAMESIGN"+str(count)+")\n@SP\nA=M-1\n"
                             "D=M\nA=A-1\nD=M-D\n@TEMP\nM=-1\n@FINISH"+str(count)+"\nD;JEQ\n@TEMP\nM=0\n@FINISH"+str(count)+"\n0;JMP\n"
                             "(SECONDNEGFIRSTNONNEG"+str(count)+")\n@TEMP\nM=0\n@FINISH"+str(count)+"\n0;JMP\n(SECONDNONNEGFIRSTNEG"+str(count)+")\n@TEMP\nM=0\n"
                             "@FINISH"+str(count)+"\n0;JMP\n(FINISH"+str(count)+")\n@TEMP\nD=M\n@SP\nA=M\nA=A-1\nA=A-1\nM=D\n@SP\nM=M-1\n")
        elif s==self.ArithmeticCommand[4]:
            self.ofile.write("@SP\nA=M-1\nA=A-1\nD=M\n@FIRSTNONNEG"+str(count)+"\nD;JGE\n@FIRSTNEG"+str(count)+"\n0;JMP\n(FIRSTNONNEG"+str(count)+")\n"
                             "@SP\nA=M-1\nD=M\n@SAMESIGN"+str(count)+"\nD;JGE\n@SECONDNEGFIRSTNONNEG"+str(count)+"\n0;JMP\n(FIRSTNEG"+str(count)+")\n@SP\n"
                             "A=M-1\nD=M\n@SECONDNONNEGFIRSTNEG"+str(count)+"\nD;JGE\n@SAMESIGN"+str(count)+"\n0;JMP\n(SAMESIGN"+str(count)+")\n@SP\nA=M-1\n"
                             "D=M\nA=A-1\nD=M-D\n@TEMP\nM=-1\n@FINISH"+str(count)+"\nD;JGT\n@TEMP\nM=0\n@FINISH"+str(count)+"\n0;JMP\n"
                             "(SECONDNEGFIRSTNONNEG"+str(count)+")\n@TEMP\nM=-1\n@FINISH"+str(count)+"\n0;JMP\n(SECONDNONNEGFIRSTNEG"+str(count)+")\n@TEMP\nM=0\n"
                             "@FINISH"+str(count)+"\n0;JMP\n(FINISH"+str(count)+")\n@TEMP\nD=M\n@SP\nA=M\nA=A-1\nA=A-1\nM=D\n@SP\nM=M-1\n")
        elif s == self.ArithmeticCommand[5]:
            self.ofile.write("@SP\nA=M-1\nA=A-1\nD=M\n@FIRSTNONNEG"+str(count)+"\nD;JGE\n@FIRSTNEG"+str(count)+"\n0;JMP\n(FIRSTNONNEG"+str(count)+")\n"
                             "@SP\nA=M-1\nD=M\n@SAMESIGN"+str(count)+"\nD;JGE\n@SECONDNEGFIRSTNONNEG"+str(count)+"\n0;JMP\n(FIRSTNEG"+str(count)+")\n@SP\n"
                             "A=M-1\nD=M\n@SECONDNONNEGFIRSTNEG"+str(count)+"\nD;JGE\n@SAMESIGN"+str(count)+"\n0;JMP\n(SAMESIGN"+str(count)+")\n@SP\nA=M-1\n"
                             "D=M\nA=A-1\nD=M-D\n@TEMP\nM=-1\n@FINISH"+str(count)+"\nD;JLT\n@TEMP\nM=0\n@FINISH"+str(count)+"\n0;JMP\n"
                             "(SECONDNEGFIRSTNONNEG"+str(count)+")\n@TEMP\nM=0\n@FINISH"+str(count)+"\n0;JMP\n(SECONDNONNEGFIRSTNEG"+str(count)+")\n@TEMP\nM=-1\n"
                             "@FINISH"+str(count)+"\n0;JMP\n(FINISH"+str(count)+")\n@TEMP\nD=M\n@SP\nA=M\nA=A-1\nA=A-1\nM=D\n@SP\nM=M-1\n")
        elif s==self.ArithmeticCommand[6]:
            self.ofile.write("@SP\nA=M\nA=A-1\nD=M\nA=A-1\nM=D&M\n@SP\nM=M-1\n")
        elif s ==self.ArithmeticCommand[7]:
            self.ofile.write("@SP\nA=M\nA=A-1\nD=M\nA=A-1\nM=D|M\n@SP\nM=M-1\n")
        elif s==self.ArithmeticCommand[8]:
            self.ofile.write("@SP\nA=M\nA=A-1\nM=!M\n")
        self.count+=1

    def WritePushPop(self,command, segment, index):
        """
        if the commmand is push or pop, this function is called and writes the code
        :param command: push/pop
        :param segment: where to or from where
        :param index: which index of the segment
        :return:
        """
        if command == 'C_PUSH':
            self.push(segment,index)
        elif command == 'C_POP' and segment != 'const':
            self.pop(segment, index)

    def pop(self,segment, index):
        """
        writes the push command to the output file
        :param segment: where to or from where
        :param index: which index of the segment
        :return:
        """
        if segment =='static':
            self.ofile.write("@SP\nA=M-1\nD=M\n@" + str(self.cur_fileName)+"."+str(index)+"\nM=D\n@SP\nM=M-1\n")
        elif segment == 'local':
            self.ofile.write("@"+str(index)+"\nD=A\n@LCL\nD=M+D\n@TMP\nM=D\n@SP\nA=M-1\nD=M\n@TMP\nA=M\nM=D\n@SP\nM=M-1\n")
        elif segment == 'argument':
            self.ofile.write("@"+str(index)+"\nD=A\n@ARG\nD=M+D\n@TMP\nM=D\n@SP\nA=M-1\nD=M\n@TMP\nA=M\nM=D\n@SP\nM=M-1\n")
        elif segment == 'this':
            self.ofile.write("@"+str(index)+"\nD=A\n@THIS\nD=M+D\n@TMP\nM=D\n@SP\nA=M-1\nD=M\n@TMP\nA=M\nM=D\n@SP\nM=M-1\n")
        elif segment == 'that':
            self.ofile.write("@"+str(index)+"\nD=A\n@THAT\nD=M+D\n@TMP\nM=D\n@SP\nA=M-1\nD=M\n@TMP\nA=M\nM=D\n@SP\nM=M-1\n")
        elif segment == 'temp':
            mem = int(index) + 5
            self.ofile.write("@SP\nA=M-1\nD=M\n@+" + str(mem) + "\nM=D\n@SP\nM=M-1\n")
        elif segment == 'pointer':
            mem = int(index) + 3
            self.ofile.write("@SP\nA=M-1\nD=M\n@+" + str(mem) + "\nM=D\n@SP\nM=M-1\n")

    def push(self,segment, index):
        """
        writes the push command to the output file
        :param segment: where to or from where
        :param index: which index of the segment
        :return:
        """
        if segment == 'static':
            self.ofile.write("@" + str(self.cur_fileName)+"."+str(index)+"\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        elif segment == 'constant':
            self.ofile.write("@" + str(index) + "\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        elif segment == 'local':
            self.ofile.write("@" + str(index) + "\nD=A\n@LCL\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        elif segment == 'argument':
            self.ofile.write("@" + str(index) + "\nD=A\n@ARG\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        elif segment == 'this':
            self.ofile.write("@" + str(index) + "\nD=A\n@THIS\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        elif segment == 'that':
            self.ofile.write("@" + str(index) + "\nD=A\n@THAT\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        elif segment == 'temp':
            mem = int(index) + 5
            self.ofile.write("@" + str(mem) + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        elif segment == 'pointer':
            mem = int(index) + 3
            self.ofile.write("@" + str(mem) + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

    def writeGoto(self, label):
        """
        writes the goto command
        :param label: the lebel to jump to
        :return:
        """
        self.ofile.write("@" +self.curFuncName+"$"+label + "\n0;JMP\n")
    def writeIf(self,label):
        """
        writes the if command
        :param label: the label to jump to
        :return:
        """
        self.ofile.write("@SP\nM=M-1\nA=M\nD=M\n@" +self.curFuncName+"$"+label + "\nD;JNE\n")
    def writeLabel(self, label):
        """
        writes the label command
        :param label: the label itself
        :return:
        """
        self.ofile.write("("+self.curFuncName+"$"+label +")\n")

    def writeInit(self):
        """
        writes the bootstrap code
        :return:
        """
        self.ofile.write("@256\nD=A\n@SP\nM=D\n")
        self.writeCall("Sys.init","0")

    def writeCall(self, functionName, numArgs):
        """
        writes the call command to the output file
        :param functionName: the func name
        :param numArgs: number of args the function expects to get
        :return:
        """
        self.ofile.write("@return$"+functionName+"."+str(self.countCall)+"\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.ofile.write("@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.ofile.write("@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.ofile.write("@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.ofile.write("@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        i = int(numArgs)+5
        self.ofile.write("@"+str(i)+"\nD=A\n@SP\nD=M-D\n@ARG\nM=D\n")
        self.ofile.write("@SP\nD=M\n@LCL\nM=D\n")
        self.ofile.write("@"+functionName+"\n0;JMP\n")
        self.ofile.write("(return$"+functionName+"."+str(self.countCall)+")\n")
        self.countCall += 1

    def writeReturn(self):
        """
        writes the commands that should be written while 'return' is invoked
        :return:
        """
        self.ofile.write("@LCL\nD=M\n@FRAME\nM=D\n")
        self.ofile.write("@5\nD=A\n@FRAME\nD=M-D\nA=D\nD=M\n@RET\nM=D\n")
        self.ofile.write("@SP\nM=M-1\n@SP\nA=M\nD=M\n@ARG\nA=M\nM=D\n")
        self.ofile.write("@ARG\nD=M+1\n@SP\nM=D\n")
        self.ofile.write("@1\nD=A\n@FRAME\nD=M-D\nA=D\nD=M\n@THAT\nM=D\n")
        self.ofile.write("@2\nD=A\n@FRAME\nD=M-D\nA=D\nD=M\n@THIS\nM=D\n")
        self.ofile.write("@3\nD=A\n@FRAME\nD=M-D\nA=D\nD=M\n@ARG\nM=D\n")
        self.ofile.write("@4\nD=A\n@FRAME\nD=M-D\nA=D\nD=M\n@LCL\nM=D\n")
        self.ofile.write("@RET\nA=M\n0;JMP\n")

    def writeFunction(self, f, k):
        """
        writes the function command when a function label is shown
        :param f: the function name
        :param k: number of parameters the function expects to get
        :return:
        """
        self.ofile.write("(" + f+ ")\n")
        self.curFuncName=f
        for i in range(int(k)):
            self.push('constant', 0)

    def close(self):
        """
        closes the main output file
        :return:
        """
        self.ofile.close()



