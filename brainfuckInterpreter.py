

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
    
    def moveFwd(self):
        self.position += 1
        self.setCell()
    
    def moveBack(self):
        self.position -= 1
        self.setCell()

class Execute():
    def __init__(self, string, pointer):
        self.pointer = pointer
        self.string = string
        self.execute(self.string)
    
    def execute(self, code):
        i = 0
        loopList = []
        while i < len(code):
            if code[i] == '<': self.pointer.moveBack()
            elif code[i] == '>': self.pointer.moveFwd()
            elif code[i] == '+': self.pointer.cell.increment()
            elif code[i] == '-': self.pointer.cell.decrement()
            elif code[i] == '.': print(self.pointer.cell.str(),end="")
            elif code[i] == ',':
                inputVar = input()
                if len(inputVar) > 1:
                    raise ValueError("Input should be exactly one character long")
                self.pointer.cell.value = ord(inputVar)
            elif code[i] == '[':
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
            elif code[i] == ']':
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

#EXECUTES PROGRAM

dataPointer = pointer(0)

fileOpen = input("Enter file directory: ")
with open(fileOpen, 'r') as f:
    codeFile = f.read()
    Execute(codeFile, dataPointer)