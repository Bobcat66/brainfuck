import re

statements = {
    'LOAD' : re.compile(r'LOAD C?([0-9]+)'),
    'ADD' : re.compile(r'ADD ([0-9]+)'),
    'OUT' : re.compile(r'OUT'),
    'SET' : re.compile(r'SET ([0-9]+)'),
    'SUBTRACT' : re.compile(r'SUBTRACT ([0-9]+)'),
    'MOVELEFT' : re.compile(r'LEFT ([0-9]+)'),
    'MOVERIGHT' : re.compile(r'RIGHT ([0-9]+)'),
    'IN' : re.compile(r'IN'),
    'LEFTBRACKET' : re.compile(r'\['),
    'RIGHTBRACKET' : re.compile(r'\]'),
}
 
tokens = re.compile(r'(?:[A-Z]+(?: C?[0-9]+)?)|(?:\[|\])') #Syntax <Capital Letters><space><C<Numbers>> or <left or right bracket>
cells = dict()


class loop:
    def __init__(self, startPos, endPos):
        self.startPos = startPos
        self.endPos = endPos


class cell:
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return str(self.value)
    
    def increment(self):
        self.value += 1
    
    def decrement(self):
        self.value -= 1
    
    def str(self):
        return chr(self.value)


class pointer:
    def __init__(self, position):
        self.cell = None
        self.position = position
        self.setCell()
    
    def setCell(self):
        newCell = cells.get(self.position)
        if newCell is None:
            #checks if cell exists, and creates new cell if cell doesn't exist
            cells[self.position] = cell(0)
            newCell = cells.get(self.position)
        self.cell = newCell
    
    def moveFwd(self, repeats):
        for i in range(int(repeats)):
            self.position += 1
        self.setCell()
    
    def moveBack(self, repeats):
        for i in range(int(repeats)):
            self.position -= 1
        self.setCell()
    
    def setPosition(self, position):
        self.position = position
        self.setCell()
    
    def cellAdd(self, addNum):
        for i in range(int(addNum)):
            self.cell.increment()
    
    def cellSubtract(self, subtractNum):
        for i in range(int(subtractNum)):
            self.cell.decrement()

class Execute:
    def __init__(self, pointer, inCode):
        self.pointer = pointer
        self.tokens = tokens.findall(inCode)
        self.parseCode = self.parse()
        print("BF# Interpreter")
    
    def parse(self):
        """
        Parses and tokenizes statements and creates an Abstract Syntax Tree
        """
        parsedStatements = []
        for token in self.tokens:
            for statement in statements.items():
                stateSearch = re.search(statement[1],token)
                if stateSearch is not None:
                    try:
                        command = (statement[0],stateSearch.group(1))
                    except IndexError:
                        #Sometimes statements will only contain their name, and if stateSearch.group(1) is called it will raise an IndexError
                        command = (statement[0],)
                    parsedStatements.append(command)
        return parsedStatements


    def execute(self):
        i = 0
        looplist = []
        self.parseCode
        while i < len(self.parseCode):
            command = self.parseCode[i]
            if command[0] == 'LOAD':
                pass
            
