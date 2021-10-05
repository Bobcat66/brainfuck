import brainfuck

fibTerm = int(input("Which term of the fibonacci sequence should be calculated? "))
fibTerm -= 3
pluses = ""
for i in range(fibTerm):
    pluses += '+'
code = f"{pluses}>+>+<<[>[>>+<<-]>[>+<<+>-]>[<+>-]<<<-]"

dataPointer = brainfuck.pointer(0)

brainfuck.Execute(code, dataPointer)
