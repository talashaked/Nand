class SymbolTable:
    """
    symbole table
    """
    def __init__(self):
        """
        init symbole table
        """
        self.symbols = {'SP':0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4,
               'R0':0, 'R1':1, 'R2':2, 'R3':3, 'R4':4, 'R5':5, 'R6':6, 'R7':7,
               'R8':8, 'R9':9, 'R10':10, 'R11':11, 'R12':12, 'R13':13, 'R14':14, 'R15':15,
               'SCREEN':16384 , 'KBD':24576}
        self.empty_memory = 16

    def addVariable(self, val):
        """
        add variable
        :param val: val
        :return: nothing
        """
        self.symbols[val] = self.empty_memory
        self.empty_memory += 1

    def get(self, symbol):
        """
        get binary symbol
        :param symbol: symbol
        :return: binary
        """
        return self.symbols.get(symbol)

    def addEntry(self,symbol, address):
        """
        add entry
        :param symbol: symbol
        :param address: address of symbol
        :return:
        """
        self.symbols[symbol] = address

    def contains(self, symbol):
        """
        contain symbol
        :param symbol: symbol
        :return: true if its contain
        """
        return self.symbols.__contains__(symbol)

    def getAddress(self, symbol):
        """
        get address of symbol
        :param symbol: symbol
        :return: address
        """
        return self.symbols[symbol]