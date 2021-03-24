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
        self.lines = [l.replace(" ", "") if l.find("//") == -1 else l[:l.find("//")].replace(" ", "") for l in self.lines] ## remove space and remarks
        self.lines = [l.replace("\n","") for l in self.lines if l!=''and l!='\n'] ##remove empty line
        self.cur_line = -1

    def hasMoreCommands(self):
        """
        has more commands
        :return: true if there are
        """
        return self.cur_line < len(self.lines) -1

    def advance(self):
        """
        advance  for next line in file
        :return: nothing
        """
        self.cur_line = self.cur_line+1

    def commandType(self):
        """
        check the command type of current command
        :return: the type 'A_COMMAND' 'L_COMMAND' or 'C_COMMAND'
        """
        return 'A_COMMAND' if self.lines[self.cur_line][0] == '@' else 'L_COMMAND'\
            if self.lines[self.cur_line][0] == '(' and self.lines[self.cur_line][-1] == ')' else 'C_COMMAND'

    def special_c(self):
        """
        special c for shift command
        :return: true for special
        """
        return self.lines[self.cur_line].find('<') != -1 or self.lines[self.cur_line].find('>') != -1

    def symbol(self):
        """
        :return: symbol in command
        """
        if self.commandType() == "A_COMMAND":
            return self.lines[self.cur_line][1:]
        else:
            return self.lines[self.cur_line][1:-1]

    def dest(self):
        """
        :return: dest in command
        """
        splitByEqual = self.lines[self.cur_line].split('=')
        return splitByEqual[0] if len(splitByEqual) != 1 else ""

    def comp(self):
        """

        :return: comp in command
        """
        instruction = self.lines[self.cur_line].split('=')
        c_j = instruction[-1].split(';')
        comp = c_j[0]
        return comp

    def jump(self):
        """

        :return: the jump in command
        """
        instruction = self.lines[self.cur_line].split('=')
        c_j = instruction[-1].split(';')
        jump = c_j[1] if len(c_j)==2 else ""
        return jump

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
        self.cur_line=-1

