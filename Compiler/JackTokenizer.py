import re


class JackTokenizer:
    def __init__(self, Ifile):
        """
        init JackTokenaizer
        """
        inputF = Ifile
        lines = inputF.read()
        p = re.compile(r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)", re.MULTILINE|re.DOTALL)
        x = lambda m: "" if m.group(2) is not None else m.group(1)
        line_without_comments = p.sub(x, lines)
        s = ""
        for l in line_without_comments:
            s = s+l.replace("\n", " ")
        self.lines = s
        self.token = ""
        self._tokenType = ""

    def hasMoreTokens(self):
        """
        return true if there is more tokens
        """
        return len(self.lines) != 0

    def isNextSymbol(self):
        """
        return true if next is symbol
        """
        reg = re.compile("^(\{|}|\(|\)|\[|\.|]|,|;|\+|-|\*|/|<|>|=|~|\||&)", re.DOTALL)
        match = re.search(reg, self.lines)
        if match is None:
            return
        start , end = match.regs[0]
        if start == 0 and end != 0:
            self.token = self.lines[start:end].replace(" ",'')
            self.lines = self.lines[end:]
            self._tokenType = "SYMBOL"
            return True

    def isNextKeyword(self):
        """
        return true if next is keyword
        """
        reg = re.compile("^(class|constructor|function|method|field|static|var|int|char|boolean|void|"
                        "true|false|null|this|let|do|if|else|while|return)"
                        "(\\s|\\{|\\}|\\(|\\)|\\[|\\]|\\.|,|;|\\+|-|\\*|/|&|\\||<|>|=|~.*)", re.DOTALL)
        match = re.search(reg, self.lines)
        if match is None:
            return
        start, end = match.regs[0]
        if start == 0 and end != 0:
            self.token = self.lines[start:end-1].replace(" ",'')
            self.lines = self.lines[end-1:]
            self._tokenType = "KEYWORD"
            return True

    def isNextString(self):
        """
        return true if next is string
        """
        reg = re.compile('^(\"[^\"]*\")', re.DOTALL)
        match = re.search(reg, self.lines)
        if match is None:
            return
        start , end = match.regs[0]
        if start == 0 and end != 0:
            self.token = self.lines[start+1:end-1]
            self.lines = self.lines[end:]
            self._tokenType = "STRING_CONST"
            return True

    def isNextIdentifier(self):
        """
        return true if next is identifier
        """
        reg = re.compile("^([a-zA-Z_][a-zA-Z_0-9]*)", re.DOTALL)
        match = re.search(reg, self.lines)
        if match is None:
            return
        start, end = match.regs[0]
        if start == 0 and end != 0:
            self.token = self.lines[start:end].replace(" ",'')
            self.lines = self.lines[end:]
            self._tokenType = "IDENTIFIER"
            return True

    def isNextInteger(self):
        """
        return true if next is integer
        """
        reg = re.compile("^([0-9]*)", re.DOTALL)
        match = re.search(reg, self.lines)
        if match is None:
            return
        start, end = match.regs[0]
        if start == 0 and end != 0:
            self.token = self.lines[start:end].replace(" ",'')
            self.lines = self.lines[end:]
            self._tokenType = "INT_CONST"
            return True

    def advance(self):
        """
        advance to next token
        """
        if self.lines == "":
            return
        while self.lines[0] == ' 'or self.lines[0]=='\t':
            self.lines = self.lines[1:]
        if self.isNextSymbol():
            return
        if self.isNextKeyword():
            return
        if self.isNextString():
            return
        if self.isNextInteger():
            return
        if self.isNextIdentifier():
            return

    def tokenType(self):
        """
        return token type
        """
        return self._tokenType

    def keyword(self):
        """
        return current keybord token
        """
        return self.token

    def symbol(self):
        """
        return current symbol token
        """
        return self.token.replace("\t","")

    def identifier(self):
        """
        return current identifier token
        """
        return self.token.replace("\t","")

    def intVal(self):
        """
        return current intval token
        """
        return self.token.replace("\t","")

    def stringVal(self):
        """
        return current stringval token
        """
        return self.token
