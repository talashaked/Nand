class VMWriter:
    def __init__(self, output):
        """
        init VMWriter
        """
        self.oFile = output
        self.label_count = 0
        self.convert_segment = {'CONST': 'constant','ARG':'argument', 'LOCAL':'local', 'STATIC':'static',
                                'THAT':'that', 'POINTER':'pointer','TEMP':'temp','THIS':'this'}

    def writePush(self,segment, index):
        """
        write push
        """
        self.oFile.write('push '+self.convert_segment[segment]+' '+str(index)+'\n')

    def writePop(self, segment, index):
        """
        write pop
        """
        self.oFile.write('pop '+self.convert_segment[segment]+' '+str(index)+'\n')

    def WriteArithmetic(self,command):
        """
        write arithmetic
        """
        self.oFile.write(command.lower()+'\n')

    def WriteLabel(self, label):
        """
        write label
        """
        self.oFile.write('label '+label+'\n')

    def WriteGoto(self, label):
        """
        write label
        """
        self.oFile.write('goto '+label+'\n')

    def WriteIf(self, label):
        """
        write if
        """
        self.oFile.write('if-goto '+label+'\n')

    def WriteCall(self, name, nArgs):
        """
        write call
        """
        self.oFile.write('call '+name+' '+str(nArgs)+'\n')

    def writeFunction(self, name, nLocals):
        """
        write function
        """
        self.oFile.write('function '+name+' '+str(nLocals)+'\n')

    def writeReturn(self):
        """
        write return
        """
        self.oFile.write('return\n')

    def close(self):
        """
        write close
        """
        self.oFile.close()
