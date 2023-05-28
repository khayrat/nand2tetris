from jack_tockenizer import JackTockenizer

class CompilationEngine:
    def __init__(self, fin, fout):
        self.tokenizer = JackTockenizer(fin)
        self.fout = fout

        assert self.tokenizer.hasMoreTokens()
        self.tokenizer.advance()
    
    def compileClass(self):
        tokenizer = self.tokenizer
        self.begin("class")
        self.process("class")
        self.process(tokenizer.identifier())

        self.process('{')
        while (self.compileClassVarDec()): pass
        while (self.compileSubroutineDec()): pass
        self.process('}')
        
        self.end("class")

    def compileClassVarDec(self):
        found = False
        t = self.tokenizer
        if t.tokenType() == JackTockenizer.KEYWORD and t.keyWord() in ['static', 'filed']:
            found = True 
        return found
        
    def compileSubroutineDec(self):
        found = False
        t = self.tokenizer
        if t.tokenType() == JackTockenizer.KEYWORD and t.keyWord() in ['contructor', 'function', 'method']:
            found = True 
            self.begin("subroutineDec")
            self.process(t.keyWord())

            # 'void' | type
            if t.tokenType() == JackTockenizer.KEYWORD and t.keyWord() == 'void': 
               self.process('void')
            else:
               self.processType()

            # varName        
            assert t.tokenType() == JackTockenizer.IDENTIFIER
            self.process(t.identifier())

            self.process('(')
            self.compileParameterList()
            self.process(')')

            self.compileSubroutineBody()

            self.end("subroutineDec")
        return found
        
    def compileParameterList(self):
      t = self.tokenizer
      self.begin("parameterList")
      # ((type varName) (',' type varName)*)?
      if t.tokenType() != JackTockenizer.SYMBOL: # if its not ')' it must be a type
        self.processType()
        assert t.tokenType() == JackTockenizer.IDENTIFIER
        self.process(t.identifier())

        # (',' type varName)*
        while t.symbol() == ',':
          assert t.tokenType == JackTockenizer.SYMBOL
          self.process(',')
          self.processType()
          assert t.tokenType() == JackTockenizer.IDENTIFIER
          self.process(t.identifier())

      self.end("parameterList")

    def processType(self):
       t = self.tokenizer
       if t.tokenType() == JackTockenizer.KEYWORD:
          assert t.keyWord() in ['int', 'char', 'boolean']
          self.process(t.keyWord())
       else:
          assert t.tokenType() == JackTockenizer.IDENTIFIER
          self.process(t.identifier())
    
    def compileSubroutineBody(self):
      t = self.tokenizer
      self.begin("subroutineBody")

      self.process('{')

      # varDec*
      while t.tokenType() == JackTockenizer.KEYWORD and t.keyWord() == 'var':
         self.compileVarDec()

      self.compileStatements()

      self.process('}')

      self.end("subroutineBody")

    def compileStatements(self):
      t = self.tokenizer

      self.begin("statements")

      while t.tokenType() == JackTockenizer.KEYWORD:
        k = t.keyWord()
        assert k in ['let', 'if', 'while', 'do', 'return']
        CompilationEngine.statement_map[k](self)
        
      self.end("statements")

    def compileVarDec(self):
      t = self.tokenizer
      self.begin("varDec")

      self.process('var')
      self.processType()
      assert t.tokenType() == JackTockenizer.IDENTIFIER
      self.process(t.identifier())

      # (',' varName)*
      while t.tokenType() == JackTockenizer.SYMBOL and t.symbol() == ',':
         self.process(',')
         assert t.tokenType() == JackTockenizer.IDENTIFIER
         self.process(t.identifier())

      self.process(';')

      self.end("varDec")
    
    def compileLet(self):
      t = self.tokenizer
      self.begin('letStatement')

      self.process('let')
      assert t.tokenType() == JackTockenizer.IDENTIFIER
      self.process(t.identifier())

      # ('[' expression ']')?
      if t.tokenType() == JackTockenizer.SYMBOL and t.symbol() == '[':
        self.process('[')
        self.compileExpression()
        self.process(']')

      self.process('=')
      self.compileExpression()
      self.process(';')
    
      self.end('letStatement')

    def compileIf(self):
       self.begin('ifStatement')

       self.process('if')
       self.process('(')
       self.compileExpression()
       self.process(')')

       self.process('{')
       self.compileStatements()
       self.process('}')

       self.process('else')

       self.process('{')
       self.compileStatements()
       self.process('}')

       self.end('ifStatement')
    
    def compileWhile(self):
       t = self.tokenizer
       self.begin('whileStatement')

       self.process('while')

       self.process('(')
       self.compileExpression()
       self.process(')')

       self.process('{')
       self.compileStatements()
       self.process('}')
    
       self.end('whileStatement')
    
    def compileDo(self):
       t = self.tokenizer
       self.begin('doStatement')

       self.process('do')
       self.processSubroutineCall()
       self.process(';')

       self.end('doStatement')

    def compileReturn(self):
       t = self.tokenizer
       self.begin('returnStatement')

       self.process('return')

       if t.tokenType() == JackTockenizer.SYMBOL and t.symbol() == ';':
         self.process(';')
       else:
         self.compileExpression()
         self.process(';')

       self.end('returnStatement')
    
    def compileExpression(self):
        t = self.tokenizer
        self.begin('expression')

        # term (op term)*
        self.compileTerm()

        op = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
        while t.tokenType() == JackTockenizer.SYMBOL and t.symbol() in op:
           self.process(t.symbol())
           self.compileTerm()

        self.end('expression')

    def compileTerm(self):
      t = self.tokenizer
      type = t.tokenType()
      self.begin('term')

      if type == JackTockenizer.INT_CONST:
         self.process(str(t.intVal()))
      elif type == JackTockenizer.STRING_CONST:
         self.process(t.stringVal())
      elif type == JackTockenizer.KEYWORD:
         k = t.keyWord()
         # keywordConstant
         assert k in ['true', 'false', 'null', 'this']
         self.process(k)
         self.compileTerm()
      elif type == JackTockenizer.SYMBOL:
        s = t.symbol()
        # '(' expression ')' | (unaryOp term)
        if s == '(':
           self.process('(')
           self.compileExpression()
           self.process(')')
        elif s in ['-', '~']:
          self.process(s)
          self.compileTerm()
      elif type == JackTockenizer.IDENTIFIER:
         # varName | varName '[' expression ']' | subroutineCall
         # varName: identifier
         # subroutineCall: identifier '(' ... | identifier '.' ...
         self.process(t.identifier())
         if t.tokenType() == JackTockenizer.SYMBOL:
            if t.symbol() == '[':
               self.process('[')
               self.compileExpression()
               self.process(']')
            elif t.symbol() == '(':
               self.process('(')
               self.compileExpressionList()
               self.process(')')
            elif t.symbol() == '.':
               self.process('.')
               assert t.tokenType() == JackTockenizer.IDENTIFIER
               self.process(t.identifier())
               self.process('(')
               self.compileExpressionList()
               self.process(')')

      self.end('term')

    # return the number of expressions in the list.
    def compileExpressionList(self):
       expressions = 0
       t = self.tokenizer
       self.begin('expressionList')

       # lookup if we have an expression at all
       if t.tokenType() == JackTockenizer.SYMBOL and t.symbol() == ')':
          self.end('expressionList')
          return 0

       expressions += 1
       self.compileExpression()
       self.foundTerm = False

       while t.tokenType() == JackTockenizer.SYMBOL and t.symbol() == ',':
          self.process(',')
          self.compileExpression()
          expressions += 1

       self.end('expressionList')
       return expressions
    
#### helper
    def printKeyWord(self):
        self.printToken("keyword", self.tokenizer.keyWord())

    def printIdentifier(self):
        self.printToken("identifier", self.tokenizer.identifier())

    def printSymbol(self):
        self.printToken("symbol", self.tokenizer.symbol())

    def printInt(self):
        self.printToken("integerConstant", str(self.tokenizer.intVal()))

    def printString(self):
        self.printToken("stringConstant", self.tokenizer.stringVal())

    def processSubroutineCall(self):
      t = self.tokenizer
      # subroutineCall: identifier '(' ... | identifier '.' ...
      self.process(t.identifier())
      assert t.tokenType() == JackTockenizer.SYMBOL
      if t.symbol() == '(':
          self.process('(')
          self.compileExpressionList()
          self.process(')')
      elif t.symbol() == '.':
          self.process('.')
          assert t.tokenType() == JackTockenizer.IDENTIFIER
          self.process(t.identifier())
          self.process('(')
          self.compileExpressionList()
          self.process(')')

    def process(self, lexeme):
        token = self.tokenizer.currentToken
        assert token.lexeme == lexeme

        CompilationEngine.emitt_map[token.type](self)
        if self.tokenizer.hasMoreTokens(): self.tokenizer.advance()

    def printToken(self, type, lexeme, padding=0):
      self.fout.write(padding * ' ')
      self.fout.write('<%s> %s </%s>\n' %(type, lexeme, type))

    def begin(self, s, padding=0):
      self.fout.write(padding * ' ' + '<' + s + '>\n')

    def end(self, s, padding=0):
      self.fout.write(padding * ' ' + '</' + s + '>\n')

    emitt_map = {
        JackTockenizer.KEYWORD: printKeyWord,
        JackTockenizer.IDENTIFIER: printIdentifier,
        JackTockenizer.SYMBOL: printSymbol,
        JackTockenizer.INT_CONST: printInt,
        JackTockenizer.STRING_CONST: printString,
    }

    statement_map = {
       'let': compileLet,
       'if': compileIf,
       'while': compileWhile,
       'do': compileDo,
       'return': compileReturn,
    }    