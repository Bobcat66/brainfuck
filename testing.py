import BFSharp

dataPointer = BFSharp.pointer(0)
code = """
LOAD C2 ADD 72 OUT
LOAD C3 ADD 101 OUT
LOAD C4 ADD 108 OUT
LOAD C5 ADD 108 OUT
LOAD C6 ADD 111 OUT
LOAD C7 ADD 32 OUT
LOAD C8 ADD 87 OUT
LOAD C9 ADD 111 OUT
LOAD C10 ADD 114 OUT
LOAD C11 ADD 108 OUT
LOAD C12 ADD 100 OUT"""
program = BFSharp.Execute(dataPointer, code)
print(program.parseCode)
program.execute()

