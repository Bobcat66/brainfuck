import re

statements = {
    'LOAD' : re.compile(r'LOAD C?([0-9]+)'),
    'ADD' : re.compile(r'ADD ([0-9]+)'),
    'OUT' : re.compile(r'OUT'),
    'SET' : re.compile(r'SET ([0-9]+)'),
    'SUBTRACT' : re.compile(r'SUBTRACT ([0-9]+)'),
    'MOVEFWD' : re.compile(r'FWD ([0-9]+)'),
    'MOVEBACK' : re.compile(r'BACK ([0-9]+)'),
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
    
    def setValue(self, value):
        self.cell.value = value

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
        loopList = []
        self.parseCode
        while i < len(self.parseCode):
            command = self.parseCode[i]
            if command[0] == 'LOAD': self.pointer.setPosition(int(command[1]))
            elif command[0] == 'ADD': self.pointer.cellAdd(int(command[1]))
            elif command[0] == 'OUT': print(self.pointer.cell.str(),end="")
            elif command[0] == 'SET': self.pointer.setValue(int(command[1]))
            elif command[0] == 'SUBTRACT': self.pointer.cellSubtract(int(command[1]))
            elif command[0] == 'MOVEFWD': self.pointer.moveFwd(int(command[1]))
            elif command[0] == 'MOVEBACK': self.pointer.moveBack(int(command[1]))
            elif command[0] == 'IN':
                inputVar = input()
                if len(inputVar) > 1:
                    raise ValueError("Input should be exactly one character long")
                self.pointer.cell.value = ord(inputVar)
            elif command[0] == 'LEFTBRACKET':
                #checks if loop exists
                loopExists = False
                for ele in loopList:
                    if ele.startPos == i: 
                        loopExists = True
                        break
                if not loopExists:
                    loopList.append(loop(i,None))
                #if the cell the pointer is on is equal to zero, jump to end bracket
                if self.pointer.cell.value == 0:
                    for ele in loopList:
                        if ele.startPos == i and ele.endPos is not None:
                            i = ele.endPos
            
            elif command[0] == 'RIGHTBRACKET':
                bracket = None

                #identifies this bracket's matching bracket
                for ele in reversed(loopList):
                    if ele.endPos is None:
                        ele.endPos = i
                        bracket = ele
                        break
                    if ele.endPos == i:
                        bracket = ele
                        break
                #sends execution pointer back to beginning of loop if data pointer's value is 0
                if self.pointer.cell.value != 0: 
                    i = bracket.startPos - 1 #subtracts one because i will still iterate at the end of the while loop
            
            i += 1
        
        print('\n')
        for cell in cells.items():
            outtext = f'Cell {cell[0]}: {cell[1]}'
            if cell[0] == self.pointer.position:
                outtext += ' <<<POINTER'
            print(outtext)
            
