from vm_parser import Parser

class CodeWriter():
  def __init__(self, fh, fn, bootStrap=False):
    self.fh = fh
    self.fn = fn
    self.currentFunction = None
    self.jmpIdx = 0
    self.retAdresses = dict()

    if bootStrap: self.addBootStrapCode()

#### API

  def writeArithmetic(self, command):
    def handle_command_uni():
      asm = CodeWriter.popD()
      if command == "not": asm += ["D=!D"]
      else               : asm += ["D=-D"] 
      asm += CodeWriter.pushD()

      return asm 

    def handle_command_bin():
      def compare_command():
        self.jmpIdx += 1
        #print(command, self.jmpIdx)
        asm = [
          "// BEGIN if D %s A goto %s" % (command, command.upper()),
          "D=D-A",
          "@%s.%d" % (command.upper(), self.jmpIdx),
          "D;J%s" % command.upper(),
          "// D = False (0 represents False)",
          "D=0",
          "@RESULT.%d" % self.jmpIdx,
          "0;JMP",
          "(%s.%d)" % (command.upper(), self.jmpIdx),
          "// D = True (-1 represents True)",
          "D=-1",
          "(RESULT.%d)" % self.jmpIdx,
          "// END  if D %s A goto %s" % (command, command.upper()),
        ]
        return asm

      command2asm = {
        "add" : lambda : ["D=D+A"],
        "sub" : lambda : ["D=D-A"],
        "and" : lambda : ["D=D&A"],
        "or"  : lambda : ["D=D|A"],
        "eq"  : compare_command,
        "gt"  : compare_command,
        "lt"  : compare_command,
      }

      asm = []
      asm += CodeWriter.popD()
      asm += CodeWriter.D_to_Reg("R13")
      asm += CodeWriter.popD()
      asm += CodeWriter.Reg_to_A("R13")

      asm += command2asm[command]()

      asm += CodeWriter.pushD()

      return asm

    asm =  ['// ### BEGIN %s:' % command]

    if command in ['not', 'neg']: asm += handle_command_uni()
    else                        : asm += handle_command_bin()

    asm += ['// ### END   %s:' % command]
    self.write_asm(asm)

  def writePushPop(self, command, segment, index):
    if command == Parser.C_PUSH: asm = self.push(segment, index)
    else:                        asm = self.pop(segment, index)

    self.write_asm(asm)

  def setFileName(self, fn):
    self.fn = fn

  def writeLabel(self, label):
    asm = ['(' + self.addScope(label) +')']
    self.write_asm(asm)

  def writeGoto(self, label):
    asm = [
      '@' + self.addScope(label),
      '0;JMP'
    ]
    self.write_asm(asm)

  def writeIf(self, label):
    asm = []
    asm += CodeWriter.popD()

    asm += [
      '@' + self.addScope(label),
      '// since -1 represents True which is lt zero',
      'D;JLT'
    ]
    self.write_asm(asm)

  def writeFunction(self, functionName, nVars):
    self.currentFunction = functionName
    asm = []
    asm += ['//### BEGIN writeFunction %s %d' % (functionName, nVars)]
    asm += ['(' + functionName + ')']
    for i in range(nVars): asm += self.push("constant", 0)
    asm += ['//### END   writeFunction %s %d' % (functionName, nVars)]
    self.write_asm(asm)

  def writeCall(self, functionName, nArgs):
    retAdr = self.genReturnAddress()
    asm = []
    asm += ['//### BEGIN writeCall %s %d' % (functionName, nArgs)]
    asm += CodeWriter.pushLabel(retAdr)
    asm += CodeWriter.pushReg("LCL")
    asm += CodeWriter.pushReg("ARG")
    asm += CodeWriter.pushReg("THIS")
    asm += CodeWriter.pushReg("THAT")
    # ARG = SP - 5 - nArgs
    asm += CodeWriter.regPointer_with_offset_to_reg(src="SP", offset=(-5-nArgs), dst="ARG")
    # LCL = SP
    asm += CodeWriter.Reg_to_Reg(src="SP", dst="LCL")
    # goto functionName
    asm += CodeWriter.gotoFunction(functionName)
    # inject (retAdr)
    asm += ['(' + retAdr + ')']
    asm += ['//### END   writeCall %s %d' % (functionName, nArgs)]

    self.write_asm(asm)

  def writeReturn(self):
    asm = []

    asm += ['//### BEGIN writeReturn - %s' % (self.currentFunction)]
    # frame = LCL // frame is stored in R14
    frame = "R14"
    asm += CodeWriter.Reg_to_Reg(src="LCL", dst=frame)
    # retAdr = *(frame-5) // retAdr is stored in R15
    retAdr = "R15"
    asm += CodeWriter.reg_with_offset_to_reg(src=frame, offset=-5, dst=retAdr)
    # *ARG = pop() // reposition the return value for the caller
    asm += self.pop("argument", 0)
    # SP = ARG + 1 // reposition SP for the caller
    asm += CodeWriter.Reg_to_Reg(src="ARG", dst="SP")
    asm += CodeWriter.SP_inc()
    # THAT = *(frame-1) // restore THAT for the caller
    asm += CodeWriter.reg_with_offset_to_reg(src=frame, offset=-1, dst="THAT")
    # THIS = *(frame-2) // restore THIS for the caller
    asm += CodeWriter.reg_with_offset_to_reg(src=frame, offset=-2, dst="THIS")
    # ARG = *(frame-3) // restore ARG for the caller
    asm += CodeWriter.reg_with_offset_to_reg(src=frame, offset=-3, dst="ARG")
    # LCL = *(frame-4) // restore LCL for the caller
    asm += CodeWriter.reg_with_offset_to_reg(src=frame, offset=-4, dst="LCL")
    # goto retAdr
    asm += CodeWriter.Reg_to_A("R15")
    asm += ['0;JMP']
    asm += ['//### END   writeReturn - %s' % (self.currentFunction)]
    self.write_asm(asm)

  def close(self):
    self.fh.close()

#### Helper

  def addBootStrapCode(self):
    functionName = "Sys.init"
    sp = 261
    #sp = 256

    # SP = 256|261 depending on compare script
    asm = [
      "@%d" % sp,
      "D=A",
      "@SP",
      "M=D"
    ]
    # call Sys.init
    asm += CodeWriter.gotoFunction(functionName)

    self.write_asm(asm)

  def pushReg(reg):
    asm = []
    asm += CodeWriter.Reg_to_D(reg)
    asm += CodeWriter.pushD()
    return asm
  
  def pushLabel(label):
    asm = []
    asm += CodeWriter.A_to_D(label)
    asm += CodeWriter.pushD()
    return asm

  def addScope(self, label):
    return "%s$%s" % (self.currentFunction, label)

  def genReturnAddress(self):
    if self.currentFunction not in self.retAdresses:
      self.retAdresses[self.currentFunction] = 0

    index = self.retAdresses[self.currentFunction]

    label = "%s$ret.%d" % (self.currentFunction, index)
    self.retAdresses[self.currentFunction] += 1
    return label

  def gotoFunction(functionName):
    asm = [
      '@' + functionName,
      '0;JMP'
    ]
    return asm

  def write_asm(self, asm):
    #[print(line) for line in asm]
    self.fh.write('\n'.join(asm))
    self.fh.write('\n')

  segment_base_map = {
    "argrument": "ARG",
    "local"    : "LCL",
    "this"     : "THIS",
    "that"     : "THAT"
  }

  def D_to_Reg(reg):
    asm = [
      "// BEGIN %s = D" % reg,
      "@" + reg,
      "M=D",
      "// END %s = D" % reg
    ]
    return asm

  def SP_inc():
    return [
      "// BEGIN SP++",
      "@SP",
      "M=M+1",
      "// END   SP++",
    ]

  def D_to_Stack():
    asm = [
      "// BEGIN RAM[SP] = D",
      "@SP",
      "A=M",
      "M=D",
      "// END   RAM[SP] = D",
    ]
    return asm

  def pushD():
    asm = []
    
    asm += ["// BEGIN push D: RAM[SP++] = D"]
    asm += CodeWriter.D_to_Stack()
    asm += CodeWriter.SP_inc()
    asm += ["// END   push D: RAM[SP++] = D"]

    return asm

  def Stack_to_D(loadSP=True):
    asm = ["// BEGIN D = RAM[SP]"]

    if loadSP: asm += ["@SP"]

    asm += [
      "A=M",
      "D=M",
    ]

    asm += ["// END D = RAM[SP]"]
    return asm

  def popD():
    asm = []

    asm += ["// BEGIN pop D = RAM[--SP]"]
    asm += CodeWriter.SP_dec()
    asm += CodeWriter.Stack_to_D(loadSP=False)
    asm += ["// END pop D = RAM[--SP]"]

    return asm
  
  def SP_dec():
    asm = [
      "// BEGIN --SP",
      "@SP",
      "M=M-1",
      "// END --SP",
    ]
    return asm

  def basePlusOffset_to_A(base, offset):
    asm = []
    asm += ["// BEGIN A = RAM[%s] + %d" % (base, offset),]
    asm += [
      "@%s" % base,
      "A = M",
    ]

    if offset > 0:
      asm += [
        "D = A",
        "@%d" % offset,
        "A = D + A",
      ]
    elif offset < 0:
      asm += [
        "D = A",
        "@%d" % -offset,
        "A = D - A"
      ]
    asm += ["// END   A = RAM[%s] + %d" % (base, offset),]
    return asm

  def Mem_to_D():
    asm = [
      "// BEGIN D = RAM[A]",
      "D = M",
      "// END   D = RAM[A]"
    ]
    return asm 

  def push_standard(segment):
    def _push(self, index):
      asm = []

      asm += ["// BEGIN push %s %d" % (segment, index),]

      asm += CodeWriter.basePlusOffset_to_A(segment, index)
      asm += CodeWriter.Mem_to_D()
      asm += CodeWriter.pushD()

      asm += ["// END   push %s %d" % (segment, index),]

      return asm
    
    return _push

  def push_pointer():
    def _push(self, index):
      reg = "THIS" if index == 0 else "THAT"
      asm = CodeWriter.Reg_to_D(reg)
      asm += CodeWriter.pushD()
      return asm
    
    return _push

  def push_static():
    def _push(self, index):
      reg = "%s.%d" % (self.fn, index)
      asm = []

      asm += ["// BEGIN RAM[SP++] = RAM[@%s]" % reg]
      asm += CodeWriter.Reg_to_D(reg)
      asm += CodeWriter.pushD()
      asm += ["// END   RAM[SP++] = RAM[@%s]" % reg]

      return asm
    
    return _push

  def push_constant():
    def _push(self, const):
      # D = const
      asm = [
        "// BEGIN D = %d" %const,
        "@%d" %const,
        "D = A",
        "// END D = %d" %const,
      ]

      asm += CodeWriter.pushD()

      return asm
    
    return _push

  def push_temp():
    def _push(self, index):
      reg_offset = 5
      reg = "R%d" % (reg_offset + index)

      asm = []

      asm += ["// BEGIN RAM[SP++] = %s" % reg]
      asm += CodeWriter.Reg_to_D(reg)
      asm += CodeWriter.pushD()
      asm += ["// END   RAM[SP++] = %s" % reg]

      return asm

    return _push

  def pop_standard(segment):
    def _pop(self, index):
      asm = []
      
      asm += ["// BEGIN pop %s %d" % (segment, index),]

      asm += ["// BEGIN R13 = RAM[%s] + %d" % (segment, index)]
      asm += CodeWriter.basePlusOffset_to_D(segment, index)
      asm += CodeWriter.D_to_Reg("R13")
      asm += ["// END R13 = RAM[%s] + %d" % (segment, index)]

      asm += ["// BEGIN RAM[R13] = RAM[--SP]"]
      asm += CodeWriter.popD()
      asm += CodeWriter.D_to_Mem("R13")
      asm += ["// END RAM[R13] = RAM[--SP]"]

      asm += ["// END pop %s %d" % (segment, index),]

      return asm
    
    return _pop

  def _basePlusOffset_to_D_depricated(base, offset):
    asm = []
    asm += ["// BEGIN D = RAM[%s] + %d" % (base, offset)]
    asm += [
      "@" + base,
      "D = M",
    ]

    if offset > 0: 
      asm += [
        "@%d" % offset,
        "D = D + A"
      ]

    asm += ["// END   D = RAM[%s] + %d" % (base, offset)]
    return asm

  def regPointer_with_offset_to_reg(src, offset, dst):
    asm = []
    asm += CodeWriter.basePlusOffset_to_A(base=src, offset=offset)
    asm += ['D=A']
    asm += CodeWriter.D_to_Reg(dst)
    return asm
  
  def reg_with_offset_to_reg(src, offset, dst):
    asm = []
    asm += CodeWriter.basePlusOffset_to_A(base=src, offset=offset)
    asm += CodeWriter.Mem_to_D()
    asm += CodeWriter.D_to_Reg(dst)
    return asm
  
  def basePlusOffset_to_D(base, offset):
    asm = []
    asm += ["// BEGIN D = RAM[%s] + %d" % (base, offset)]
    asm += [
      "@" + base,
      "D = M",
    ]

    if offset > 0: 
      asm += [
        "@%d" % offset,
        "D = D + A"
      ]
    elif offset < 0:
      asm += [
        "@%d" % -offset,
        "D = D - A"
      ]

    asm += ["// END   D = RAM[%s] + %d" % (base, offset)]
    return asm

  def D_to_Mem(reg):
    asm = ["// BEGIN RAM[%s] = D" % reg]
    asm += [
      "@" + reg,
      "A=M",
      "M=D",
    ]
    asm += ["// END RAM[%s] = D" % reg]
    return asm

  def pop_pointer():
    def _pop(self, index):
      reg = "THIS" if index == 0 else "THAT"
      asm = CodeWriter.popD()
      asm += CodeWriter.D_to_Reg(reg)
      return asm
    
    return _pop

  def pop_static():
    def _pop(self, index):
      reg = "%s.%d" % (self.fn, index)
      asm = []
      
      asm += ["// BEGIN RAM[@%s] = RAM[--SP]" % reg]
      asm += CodeWriter.popD()
      asm += CodeWriter.D_to_Reg(reg)
      asm += ["// END   RAM[@%s] = RAM[--SP]" % reg]

      return asm
    
    return _pop
  
  def pop_constant():
    def _pop(self, index):
      return [
        "// pop constant %d - doesn't make sence!!" % index
      ]
    
    return _pop
  
  def pop_temp():
    def _pop(self, index):
      reg_offset = 5
      reg = "R%d" % (reg_offset + index)

      asm = []

      asm += ["// BEGIN %s = RAM[--SP]" % reg]
      asm += CodeWriter.popD()
      asm += CodeWriter.D_to_Reg(reg)
      asm += ["// END %s = RAM[--SP]" % reg]

      return asm
    
    return _pop

  def A_to_D(reg):
    asm = [
      "// BEGIN D = @%s" % reg,
      "@%s" % reg,
      "D=A",
      "// END D = @%s" % reg
    ]
    return asm

  def Reg_to_D(reg):
    asm = [
      "// BEGIN D = %s" % reg,
      "@%s" % reg,
      "D=M",
      "// END D = %s" % reg
    ]
    return asm

  def Reg_to_A(reg):
    asm = [
      "// BEGIN A = %s" % reg,
      "@%s" % reg,
      "A=M",
      "// END A = %s" % reg
    ]
    return asm

  def Reg_to_Reg(src , dst):
    asm =  [] 

    asm += ["// BEGIN R%s = R%s" % (dst, src)]
    asm += CodeWriter.Reg_to_D(src)
    asm += CodeWriter.D_to_Reg(dst)
    asm += ["// END   R%s = R%s" % (dst, src)]

    return asm    

  push_map = {
    "argument":  push_standard("ARG"),
    "local"    : push_standard("LCL"),
    "this"     : push_standard("THIS"),
    "that"     : push_standard("THAT"),
    "pointer"  : push_pointer(),
    "static"   : push_static(),
    "constant" : push_constant(),
    "temp"     : push_temp()
  }

  pop_map = {
    "argument":  pop_standard("ARG"),
    "local"    : pop_standard("LCL"),
    "this"     : pop_standard("THIS"),
    "that"     : pop_standard("THAT"),
    "pointer"  : pop_pointer(),
    "static"   : pop_static(),
    "constant" : pop_constant(),
    "temp"     : pop_temp()
  }

  def push(self, segment, index):
    asm = ["// ### BEGIN push %s %d" % (segment, index)]
    asm += CodeWriter.push_map[segment](self, index)
    asm += ["// ### END push %s %d" % (segment, index)]
    return asm

  def pop(self, segment, index):
    asm = ["// ### BEGIN pop %s %d" % (segment, index)]
    asm += CodeWriter.pop_map[segment](self, index)
    asm += ["// ### END pop %s %d" % (segment, index)]
    return asm

##### testing

import os, tempfile
class Test():
  def prepare_file(self):
    _, path = tempfile.mkstemp()
    self.path = path  
    self.fn = os.path.basename(path)
    self.fh = open(path, 'w')
    print("writing to file '%s'" % path)  
    
  def clean_file(self):
    os.remove(self.path)

  def test_writeArithmetic(self):
    def test_uni_command():
      vm_commands = [
        "not",
        "neg"
      ]

      for vm_command in vm_commands:
        cw.writeArithmetic(vm_command)

    def test_bi_command():
      _vm_commands = [
        "eq",
      ]
      vm_commands = [
        "add",
        "sub",
        "and",
        "or",
        "eq",
        "lt",
        "gt"
      ]

      for vm_command in vm_commands:
        cw.writeArithmetic(vm_command)

    self.prepare_file()
    cw = CodeWriter(fh=self.fh, fn=self.fn)

    test_uni_command()
    test_bi_command()

    cw.close()
    self.clean_file()

  def test_writePushPop(self):
    def test_pop():
      for tuple in lotuple: 
        cw.writePushPop(command=Parser.C_POP, segment=tuple[0], index=tuple[1])

    def test_push():
      for tuple in lotuple: 
        cw.writePushPop(command=Parser.C_PUSH, segment=tuple[0], index=tuple[1])

    _segemnts = ["argument"]
    _segemnts = ["local"]
    _segemnts = ["this"]
    _segemnts = ["that"]
    _segemnts = ["pointer"]
    _segemnts = ["temp"]
    _segemnts = ["constant"]
    _segemnts = ["static"]
    segemnts = ["argument", "local", "this", "that", "pointer", "static", "constant", "temp"]
    indexes = range(0,3)
    lotuple = [(segment, index) for segment in segemnts for index in indexes]

    self.prepare_file()

    cw = CodeWriter(fh=self.fh, fn=self.fn)

    test_push()
    test_pop()

    cw.close()
    self.clean_file()

  def test_writeLabel(self):
    ### prepare
    self.prepare_file()
    cw = CodeWriter(fh=self.fh, fn=self.fn)

    ### test
    label = "LOOP_START"
    cw.writeLabel(label)

    ### cleanup
    cw.close()
    self.clean_file()

  def test_writeGoto(self):
    ### prepare
    self.prepare_file()
    cw = CodeWriter(fh=self.fh, fn=self.fn)

    ### test
    label = "LOOP_START"
    cw.writeGoto(label)

    ### cleanup
    cw.close()
    self.clean_file()

  def test_writeIf(self):
    ### prepare
    self.prepare_file()
    cw = CodeWriter(fh=self.fh, fn=self.fn)

    ### test
    label = "LOOP_START"
    cw.writeIf(label)

    ### cleanup
    cw.close()
    self.clean_file()

  def test_wirteFunction(self):
    ### prepare
    self.prepare_file()
    cw = CodeWriter(fh=self.fh, fn=self.fn)

    ### test
    fn = "Foo.f1"
    args = 5
    cw.writeFunction(fn, args)

    ### cleanup
    cw.close()
    #self.clean_file()

  def test_writeCall():
    pass
  
  def test_wirteReturn(self):
    pass

def test_suite():
  test = Test()

  #test.test_writeArithmetic()
  #test.test_writePushPop()
  #test.test_writeLabel()
  #test.test_writeGoto()
  #test.test_writeIf()
  test.test_wirteFunction()
  #test.test_writeCall()
  #test.test_wirteReturn()
  
if __name__ == "__main__":
  test_suite()