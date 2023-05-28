class JackTockenizer:
    # token types
    KEYWORD      = 0
    SYMBOL       = 1
    IDENTIFIER   = 2
    INT_CONST    = 3
    STRING_CONST = 4

    # key words
    CLASS = 5
    METHOD = 6
    FUNCTION = 7
    CONSTRUCTOR = 8
    INT = 9
    BOOLEAN = 10
    CHAR = 11
    VOID = 12
    VAR = 13
    STATIC = 14
    FIELD = 15
    LET = 16
    DO = 17
    IF = 18
    ELSE = 19
    WHILE = 20
    RETURN = 21
    TRUE = 22
    FALSE = 23
    NULL = 24
    THIS = 25

    keywords = [
      'class', 'constructor', 'function', 'method', 'field', 
      'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 
      'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 
      'return'
    ]
    symbols = [
      '{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', 
      '/', '&', '|', '>', '<', '=', '~'
    ]

    LexicalElements = {
       'keyword': keywords,
       'symbol': symbols     
    }

    def __init__(self, fh):
      self.fh = fh
      self.more = True
      self.currentToken = None
      self.lookahead = None
      self.lookaheadSecond = None
      self._lookahead()

    def hasMoreTokens(self):
       return self.lookahead
    
    def advance(self):
      lexElems = JackTockenizer.LexicalElements
      if self.lookahead in lexElems['symbol']:
          self.currentToken = Token(JackTockenizer.SYMBOL, self.lookahead)
      elif self.lookahead == '"':
        self.currentToken = Token(JackTockenizer.STRING_CONST, self.readString())
      else:
        word = self.lookahead + self.readWord()         
        if word in lexElems['keyword']: self.currentToken = Token(JackTockenizer.KEYWORD, word)
        elif word.isdigit(): self.currentToken = Token(JackTockenizer.INT_CONST, word)
        else: self.currentToken = Token(JackTockenizer.IDENTIFIER, word)
      # prepare next lookup and advance
      if self.lookaheadSecond:
        self.lookahead = self.lookaheadSecond
        self.lookaheadSecond = None
      else: 
        self.lookahead = None
        self._lookahead()

    def tokenType(self):
     return self.currentToken.type
    
    def keyWord(self):
     return self.currentToken.lexeme
    
    def symbol(self):
     return self.currentToken.lexeme

    def identifier(self):
      return self.currentToken.lexeme
    
    def intVal(self):
      return int(self.currentToken.lexeme)

    def stringVal(self):
      return self.currentToken.lexeme
    
    #### helper

    def _lookahead(self):
      ws = ['\t', ' ', '\n', '\r']
      while True:
        c = self.fh.read(1)

        if not c: break # EOF

        # skip ws and comments

        if c in ws: continue

        if c == '/':
          lookahead = self.fh.read(1)
          if lookahead == '/': self.skipToNL()
          elif lookahead == '*': self.skipComment()
          elif lookahead in ws: 
            self.lookahead = c
            break
          else: 
            self.lookahead = c
            self.lookaheadSecond = lookahead # we must handel constructs as 'x/123'
            break

        else: 
           self.lookahead = c
           break


    def skipToNL(self):
      while True:
        c = self.fh.read(1)
        if c in ['\n', '\r']: break

    def skipComment(self):
      while True:
        if self.fh.read(1) == '*' and self.fh.read(1) == '/': break

    def readWord(self):
      word = ''
      ws = ['\t', ' ', '\n', '\r']
      while True:
        c = self.fh.read(1)
        if not c or c in ws: return word
        elif c in JackTockenizer.symbols: 
          self.lookaheadSecond = c
          return word
        word += c
    
    def readString(self):
      s = ''
      while True:
        c = self.fh.read(1)
        if not c or c == '"': return s
        s += c

class Token:
   def __init__(self, type, lexeme):
      self.type = type
      self.lexeme = lexeme