class CodeWriter:
    segmentPointer = { 
        'local': 'LCL',
        'argument': 'ARG',
        'this': 'THIS',
        'that': 'THAT',
        'static': '16', 
        'temp': '5'
    }


    #segments = {'local', 'argument', 'this', 'that', 'static', 'constant', 'temp', 'pointer'}
    def __init__(self, fn):
        self.f = self._openOutput(fn)
        self.memFunctions = {
            'local': self.writeSegment,
            'argument': self.writeSegment,
            'this': self.writeSegment,
            'that': self.writeSegment,
            'static': self.writeStatic, 
            'constant': self.writeConstant,
            'temp': self.writeTemp, 
            'pointer': self.writePointer
        }

    def _openOutput(self, fn):
        return open(fn, 'w')

    def close(self):
        self.f.close()

    def writeArithmetic(self, cmd):
        '''
        Writes the assembly code that is the translation of the given arithmetic command.
        '''
        pass

    def writePushPop(self, cmd, segment, index):
        '''
        Writes the assembly code that is the translation of the given command, where command is either C_PUSH or C_POP.
        '''
        self._addComment(cmd, segment, index)
        if segment in self.memFunctions:
            self.memFunctions[segment](cmd, segment, index)
        else: raise Exception("no such segment: %s" % segment)

    def _write(self, output):
        if type(output) == list:
            for line in output: self.f.write("%s\n" % line)
        else:
            self.f.write("%s\n" % output)

    def _addComment(self, cmd, segment='', index=''):
        self._write("// %s %s %s" % (cmd, segment, index))

    def writeSegment(self, cmd, segment, index):
        '''
        push: addr = segmentPointer + i, *SP = *addr, SP++
        pop:  addr = segmentPointer + i, SP--, *addr = *SP
        '''
        print("writeSegment")
        segmentPointer = CodeWriter.segmentPointer[segment]
        output=[] 
        if cmd == 'C_PUSH': 
            # push: addr = segmentPointer + i, *SP = *addr, SP++ 
            output.append("// push general: addr = segementPointer + i, *SP = *addr, SP++")

            output.append("")

            output.append("// 1. addr = segementPointer + i")
            output.append("// addr = D=RAM[%s]+%s" % (segmentPointer, index))
            output.append("// D=RAM[%s]" % (segmentPointer))
            output.append("@%s" % segmentPointer)
            output.append("D=M")
            output.append("// addr = D=D+%s" % index)
            output.append("@%s" % index)
            output.append("D=D+A")

            output.append("")

            output.append("// 2. *SP = *addr")
            output.append("// *addr = D=RAM[D]")
            output.append("A=D")
            output.append("D=M")
            output.append("// *SP = D")
            output.append("@SP")
            output.append("A=M")
            output.append("M=D")

            output.append("")

            output.append("// 3. SP++")
            output.append("@SP")
            output.append("M=M+1")
            self._write(output)
        elif cmd == 'C_POP':
            #pop:  addr = segmentPointer + i, SP--, *addr = *SP
            #equals: SP--, addr = segementPoint + i, *addr = *SP
            output.append("// pop:  addr = segmentPointer + i, SP--, *addr = *SP")
            # addr = segementPointer + i
            # RAM[13] = segementPointer + i
            output.append("// 1. addr = segementPointer + i")
            output.append("// RAM[13] = addr")
            output.append("// D=RAM[%s]+%s" % (segmentPointer, index))
            output.append("@%s" % segmentPointer)
            output.append("D=M")
            output.append("// addr = D+%s" % index)
            output.append("@%s" % index)
            output.append("D=D+A")
            output.append("// RAM[13]=D")
            output.append("@13")
            output.append("M=D")

            output.append("")

            output.append("// 2. SP--:")
            output.append("@SP")
            output.append("M=M-1")

            output.append("")

            # *addr = *SP
            # D = *SP
            # *RAM[13] = D
            output.append("// 3. *addr=*SP")
            output.append("// *RAM[13]=*SP")
            output.append("// D=*SP")
            output.append("A=M")
            output.append("D=M")
            output.append("// *RAM[13]=D")
            output.append("@13")
            output.append("A=M")
            output.append("M=D")

            self._write(output)
        else: raise Exception("unknown command: %s" % cmd)


    def writeStatic(self, cmd, segemnt, index):
        print("writeStatic")

    def writeTemp(self, cmd, segemnt, index):
        print("writeTemp")
        
    def writePointer(self, cmd, segemnt, index):
        print("wirtePointer")

    def writeConstant(self, cmd, segemnt, index):
        print("writeConsant")
