STATIC = 'STATIC'
FIELD = 'FIELD'
VAR = 'LOCAL'
ARG = 'ARG'

class SymbolTable:

    def __init__(self):
        """
        init symboltable
        """
        self.static_index = 0
        self.field_index = 0
        self.arg_index = 0
        self.var_index = 0
        self.cur_class = {}
        self.subroutine = {}

    def startSubroutine(self):
        """
        init subroutine
        """
        self.subroutine = {}
        self.arg_index = 0
        self.var_index = 0

    def define(self,name,type,kind):
        """
        define new variable
        """
        if kind == STATIC:
            self.cur_class[name] = [type,kind,self.static_index]
            self.static_index+=1
        if kind == FIELD:
            self.cur_class[name] = [type, kind, self.field_index]
            self.field_index+=1
        if kind == "VAR":
            self.subroutine[name] = [type, VAR, self.var_index]
            self.var_index+=1
        if kind == ARG:
            self.subroutine[name] = [type, kind, self.arg_index]
            self.arg_index+=1

    def varCount(self, kind):
        """
        return count of variable of given kind
        """
        if kind == STATIC:
            return self.static_index
        if kind == FIELD:
            return self.field_index
        if kind == VAR:
            return self.var_index
        if kind == ARG:
            return self.arg_index

    def kindOf(self,name):
        """
        return kind of variable that given his name
        """
        if name in self.subroutine.keys():
            return self.subroutine[name][1]
        if name in self.cur_class.keys():
            return self.cur_class[name][1]

    def typeOf(self,name):
        """
        return type of variable that given  his name
        """
        if name in self.subroutine.keys():
            return self.subroutine[name][0]
        if name in self.cur_class.keys():
            return self.cur_class[name][0]

    def indexOf(self,name):
        """
        return index of variable that given his name
        """
        if name in self.subroutine.keys():
            return self.subroutine[name][2]
        if name in self.cur_class.keys():
            return self.cur_class[name][2]