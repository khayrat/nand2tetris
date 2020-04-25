from os import path
import re

class Parser:
    mem_commands = {'push': 'C_PUSH', 'pop': 'C_POP'}
    segments = {'local', 'argument', 'this', 'that', 'static', 'constant', 'temp', 'pointer'}

    arith_commands = {'add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not'}

    def __init__(self, fn):
        self.fn = fn
        self.inputLines=self._readInput(fn)
        self.inputLen = len(self.inputLines)
        self.index = 0
        self.line= ''
        self._skipCommentAndEmptyLines()
        self._parseCommand()

    def _readInput(self, fn):
        with open(fn, 'r') as f:
            return list(f)

    def _skipCommentAndEmptyLines(self):
        while not self._eof():
            self.line = self.inputLines[self.index].strip()
            if not self.line or self.line.startswith('//'): 
                self.index += 1
            else: 
                self._cleanLine()
                break

    def _cleanLine(self):
        self.line = re.sub('//.*$', '', self.line).strip()

    def _eof(self):
        return not self.index < self.inputLen

    def _parseCommand(self):
        if self._eof(): return

        parts = self.line.split()

        if len(parts) == 1: self._parseArithCommand(parts[0])
        elif len(parts) == 3: self._parseMemCommand(parts[0], parts[1], parts[2])
        else: self.error("not a valid command: '%s'" % self.line)

    def error(self, msg):
        raise Exception("file: %s, in line %d: %s" % (self.fn, self.index, msg))


    def _parseMemCommand(self, cmd, arg1, arg2):
        if cmd not in Parser.mem_commands: self.error("not a valid command: %s" % cmd)
        else: 
            if arg1 not in Parser.segments: self.error("invalid segment: %s" % arg1)

            self._currentCommand = Parser.mem_commands[cmd]
            self._arg1 = arg1
            self._arg2 = arg2
            
    def _parseArithCommand(self, cmd):
        if cmd not in Parser.arith_commands: error("not a valid command: %s" % cmd)
        self._currentCommand = 'C_ARITHMETIC' 
        self._arg1 = None
        self._arg2 = None

    def hasMoreCommands(self):
        '''
        Are there more commands in the input?
        '''
        if self._eof(): 
            return False
        else:
            return True

    def advance(self):
        '''
        Reads the next command from the input and makes it the current command. 
        Should be called only if hasMoreCommands() is true. Initially there is no current command.
        '''
        self.index += 1
        self._skipCommentAndEmptyLines()
        self._parseCommand()

    def commandType(self):
        '''
        Returns C_ARITHMETIC, C_PUSH, C_POP, C_LABEL, C_GOTO, C_IF, C_FUNCTION, C_RETURN, C_CALL
        Returns the type of the current VM command. C_ARITHMETIC is returned for all the arithmetic commands.
        '''
        return self._currentCommand

    def arg1(self):
        '''
        Returns the first argument of the current command. 
        In the case of C_ARITHMETIC, the command itself (add, sub, etc.) is returned. 
        Should not be called if the current command is C_RETURN.
        '''
        return self._arg1

    def arg2(self):
        '''
        Returns the second argument of the current command. 
        Should be called only if the current command is C_PUSH, C_POP, C_FUNCTION, or C_CALL.
        '''
        return self._arg2
