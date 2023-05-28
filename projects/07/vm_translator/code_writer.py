import sys

class CodeWriter:
  def __init__(self, fn):
    self.f = open(fn, 'w')
    print("generate output to file %s" % fn)
    self._code = []
    self._binary = {'add':'+', 'sub':'-', 'eq':'-', 'gt':'-', 'lt':'-', 'and':'&', 'or':'|'}
    self._unary = {'neg':'-', 'not':'!'}
    self._memory = {
      'temp':     {'from': 5,     'to': 12},
      'pointer':  {'from': 3,     'to': 4},
      'general':  {'from': 13,    'to': 15},
      'static':   {'from': 16,    'to': 255},
      'stack':    {'from': 256,   'to': 2047},
      'heap':     {'from': 2048,  'to': 16483}, 
      'local':    {'from': 2048,  'to': 2048+100, 'symbol': 'LCL'},
      'argument': {'from': 2048+101,  'to': 2048+101+100, 'symbol': 'ARG'}, 
      'this':     {'from': 2048+101+101,  'to': 2048+101+101+100, 'symbol': 'THIS'}, 
      'that':     {'from': 2048+101+101+101,  'to': 2048+101+101+101+100, 'symbol': 'THAT'} 
    }
    self._label_idx = 0
    self._static_idx = 0

  def setFileName(self, fileName):
    self._fn=fileName
    self._static_idx = 0

  def writeArithmetic(self, command):
    if command in self._binary:
      self._binaryCmd(command)
    elif command in self._unary:
      self._unaryCmd(command)    
    else:
      self._error("command '%s' not found." % command)

    self._write()

  def writePushPop(self, command, segment, index):
    if command == 'C_PUSH':
      self._push(segment, int(index))
    else: # C_POP
      self._pop(segment, int(index))

    self._write()

  def _push(self, segment, index):
    if segment == 'constant':
      # D=index
      self._cmd('@' + str(index))
      self._cmd('D=A')
      self._pushD()
    else:
      # todo: may be this could be optimized.
      self._posToReg(segment, index)
      self._regToA()
      self._cmd('D=M')
      self._pushD()
      
  def _pop(self, segment, index):
    if segment == 'constant':
      # just adjust sp
      self._cmd('@SP')
      self._cmd('M=M-1')
    else:
      # put d into ram[segment+index] wow: M=D
      self._posToReg(segment, index)
      self._popTo('D')
      self._regToA()
      self._cmd('M=D')

  def _pushD(self):
    # result is in d so push d
    self._cmd('@SP')
    self._cmd('A=M')
    self._cmd('M=D')
    # adjust sp
    self._cmd('@SP')
    self._cmd('M=M+1')
    
  def _posToReg(self, segment, index): 
    if segment in ['temp', 'pointer']: 
      pos = self._memory[segment]['from'] + index
      self._cmd('@' + str(pos))
      self._cmd('D=A')
    elif segment in ['local', 'argument', 'this', 'that']:
      # add base + index
      # get base @LCL
      self._cmd('@' + self._memory[segment]['symbol'])
      self._cmd('D=M')
      self._cmd('@' + str(index))
      self._cmd('D=D+A')
    elif segment == 'static':
      pos = self._getStaticPos(index)
      self._cmd('@' + str(pos))
      self._cmd('D=A')
    else: self._error("unknown segment: %s" % segement)

    # put D in reg 13 -> segment+index is in reg13
    self._cmd('@13')
    self._cmd('M=D')

  def _getStaticPos(self, index):
    return self._fn +str(index)
      
  def _regToA(self):    
    self._cmd('@13')
    self._cmd('A=M')

  def _error(self, msg):
    print(msg)
    sys.exit(1)

  def _write(self):
    self.f.writelines([l + '\n' for l in self._code])
    self._code = []

  def _popTo(self, register):
      # dec sp
      self._cmd('@SP')
      self._cmd('M=M-1')
      # register = ram[sp]
      self._cmd('A=M')
      self._cmd(register +'=M')

  def _unaryCmd(self, command):
    self._popTo('D')
    self._cmd('D=' + self._unary[command] + 'D')
    # result is in d so push d
    self._pushD()

  def _binaryCmd(self, command):
    self._popTo('D')
    self._popTo('A')

    # D=D cmd A
    # if the command is 'sub' operands have to be swaped since they are popped in reverse order.
    if command == 'sub': 
      self._cmd('D=A' + self._binary[command] + 'D')
    else:
      self._cmd('D=D' + self._binary[command] + 'A')

    # special treatment for =,>,<
    self._handleCompare(command)

    # result is in d so push d
    self._pushD()
    
  def _handleCompare(self, command):
      if not command in ['eq', 'lt', 'gt']: return
    
      # Pre: assume result of the diff is in D , so perform jump based on compare op
      # Post: needs to put -1(true) or 0(false) in D 

      # lt and gt are swaped since their operands are accessed in lifo
      jumpMap = {'eq':'JEQ', 'lt':'JGT', 'gt':'JLT'}
      jump = jumpMap[command]

      self._cmd(self._emit('@IF_TRUE'))
      self._cmd('D;' + jump)
      # false
      self._cmd('D=0')
      self._cmd(self._emit('@END_IF'))
      self._cmd('0;JMP')
      self._cmd('(' + self._emit('IF_TRUE') +')')
      # true
      self._cmd('D=-1')
      self._cmd('(' + self._emit('END_IF') +')')
      # continue where left.
      self._label_idx += 1

  def _emit(self, label):
    return label + '_' + self._fn +str(self._label_idx)

  def _cmd(self, code): self._code.append(code) 

  def close(self):
    self.f.close()

if __name__ == '__main__':
    fn = sys.argv[1]
    c = CodeWriter(fn)
    # add
    #c.writePushPop('C_PUSH', 'constant', 14)
    #c.writePushPop('C_PUSH', 'constant', 3)
    #c.writeArithmetic('add')
    #c.writePushPop('C_PUSH', 'constant', 5)
    #c.writeArithmetic('add')
    # sub
    #c.writePushPop('C_PUSH', 'constant', 22)
    #c.writePushPop('C_PUSH', 'constant', 22)
    #c.writeArithmetic('sub')
    # comp or, and 
    #c.writePushPop('C_PUSH', 'constant', 1)
    #c.writePushPop('C_PUSH', 'constant', 2)
    #c.writePushPop('C_PUSH', 'constant', 3)
    #c.writeArithmetic('or')
    #c.writeArithmetic('and')
    # comp eq, lt, gt
    #c.writePushPop('C_PUSH', 'constant', 0)
    #c.writePushPop('C_PUSH', 'constant', 0)
    #c.writePushPop('C_PUSH', 'constant', 3)
    #c.writePushPop('C_PUSH', 'constant', 14)
    #c.writeArithmetic('lt')
    #c.writeArithmetic('gt')
    #c.writeArithmetic('eq')
    # unary not, neg
    # neg
    #c.writePushPop('C_PUSH', 'constant', 1)
    #c.writeArithmetic('neg')
    # not
    #c.writePushPop('C_PUSH', 'constant', 0)
    #c.writeArithmetic('not')
    #c.writePushPop('C_PUSH', 'constant', 57)
    #c.writePushPop('C_PUSH', 'constant', 31)
    #c.writePushPop('C_PUSH', 'constant', 53)
    #c.writeArithmetic('add')
    #c.writePushPop('C_PUSH', 'local', 5)
    c.writePushPop('C_POP', 'local', 5)
    #c.writeArithmetic('sub')
    c.close()