class Parser:
    destTab = {
        ""   : "000", 
        "M"  : "001", 
        "D"  : "010", 
        "MD" : "011", 
        "A"  : "100", 
        "AM" : "101", 
        "AD" : "110", 
        "AMD": "111" 
    }

    jumpTab = {
        ""   : "000", 
        "JGT": "001", 
        "JEQ": "010", 
        "JGE": "011", 
        "JLT": "100", 
        "JNE": "101", 
        "JLE": "110", 
        "JMP": "111" 
    }

    compTab = {
        "0"    : "0101010",
        "1"    : "0111111",
        "-1"   : "0111010",
        "D"    : "0001100",
        "A"    : "0110000",
        "M"    : "1110000",
        "!D"   : "0001101",
        "!A"   : "0110001",
        "!M"   : "1110001",
        "-D"   : "0001111",
        "-A"   : "0110011",
        "-M"   : "1110011",
        "D+1"  : "0011111",
        "A+1"  : "0110111",
        "M+1"  : "1110111",
        "D-1"  : "0001110",
        "A-1"  : "0110010",
        "M-1"  : "1110010",
        "D+A"  : "0000010",
        "D+M"  : "1000010",
        "D-A"  : "0010011",
        "D-M"  : "1010011",
        "A-D"  : "0000111",
        "M-D"  : "1000111",
        "D&A"  : "0000000",
        "D&M"  : "1000000",
        "D|A"  : "0010101",
        "D|M"  : "1010101",
    }

    def __init__(self, filename):
        # open file and store fh
        self.fh = open(filename, 'r')
        self.currentCommand = self._readCommand()
        self._parseCommand()

    def _parseCommand(self):
        if not self.currentCommand:
            self._commandType = None
            return

        # set command type
        if   self.currentCommand.startswith('@'): self._commandType = 'A_COMMAND'
        elif self.currentCommand.startswith('('): self._commandType = 'L_COMMAND'
        else:                                     self._commandType = 'C_COMMAND'


    def _readCommand(self):
        line = self.fh.readline()

        # did we reach eof?
        if not line: return None

        line = line.strip()

        # skip empty lines
        if not line: return self._readCommand()

        # skip comment lines
        if line.startswith('//'): return self._readCommand()

        # still has to strip off comment parts of a command line: 'command // some comment'
        idx = line.find('//')
        if idx != -1: return line[:idx].strip()
        else:         return line

    def hasMoreCommands(self):
        '''
        Are there more commands in the input?
        '''
        print("command: '%s'" % self.currentCommand)
        return self.currentCommand != None

    def advance(self):
        ''' 
        Reads the next command from the input and makes it the current command. 
        Should be called only if hasMoreCommands() is true. 
        Initially there is no current command.
        ''' 
        self.currentCommand = self._readCommand()
        self._parseCommand()

    def commandType(self):
        '''
        Returns the type of the current command:
        m A_COMMAND for @Xxx where Xxx is either a symbol or a decimal number
        m C_COMMAND for dest=comp;jump
        m L_COMMAND (actually, pseudo- command) for (Xxx) where Xxx is a symbol.
        '''
        return self._commandType

    def symbol(self):
        '''
        -> string
        Returns the symbol or decimal Xxx of the current command @Xxx or (Xxx). 
        Should be called only when commandType() is A_COMMAND or L_COMMAND.
        '''

        if not self._commandType in ['A_COMMAND', 'L_COMMAND']: raise ('wrong command type') 

        if self.currentCommand.startswith('@'): return self.currentCommand[1:]
        else:                                   return self.currentCommand[1:-1]

    def dest(self):
        '''
        -> string
        Returns the dest mnemonic in the current C-command (8 possi- bilities). 
        Should be called only when commandType() is C_COMMAND.
        '''
        if not self._commandType in ['C_COMMAND']: raise ('wrong command type') 
       
        # chop dest part if any
        idx = self.currentCommand.find('=')
        if idx < 1: return Parser.destTab['']
        dest_part = self.currentCommand[:idx].strip()

        return Parser.destTab[dest_part]

    def comp(self):
        '''
        -> string
        Returns the comp mnemonic in the current C-command (28 pos- sibilities). 
        Should be called only when commandType() is C_COMMAND.
        '''

        if not self._commandType in ['C_COMMAND']: raise ('wrong command type') 
        
        # chop comp part if any
        pre = self.currentCommand.find('=')
        if pre >= 0: pre = pre + 1 
        else: pre = 0

        post = self.currentCommand.find(';')
        if post < 0: comp_part = self.currentCommand[pre:].strip()
        else:        comp_part = self.currentCommand[pre:post].strip()

        return Parser.compTab[comp_part]

    def jump(self):
        '''
        -> string
        Returns the jump mnemonic in the current C-command (8 pos- sibilities).
        Should be called only when commandType() is C_COMMAND.
        '''

        if not self._commandType in ['C_COMMAND']: raise ('wrong command type') 

        # chop jump part if any
        idx = self.currentCommand.find(';')
        if idx < 1: return Parser.destTab['']
        jump_part = self.currentCommand[idx+1:].strip()

        return Parser.jumpTab[jump_part]
