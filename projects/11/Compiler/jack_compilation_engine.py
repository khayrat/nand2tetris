from jack_tockenizer import JackTockenizer
from jack_symbol_table import SymbolTable

class CompilationEngine:
    def __init__(self, fin, fout):
        self.tokenizer = JackTockenizer(fin)
        self.fout = fout

        self.classST = None
        self.methodST = None
        self.usage = None

        assert self.tokenizer.hasMoreTokens()
        self.tokenizer.advance()
    
    def compileClass(self):
        t = self.tokenizer
        self.begin("class")
        self.process("class")
        self.classST = SymbolTable(name=t.identifier())
        self.usage = "declared"
        self.process(t.identifier())
        self.usage = "used"
        self.process('{')

        while t.tokenType() == JackTockenizer.KEYWORD and t.keyWord() in ['static', 'field']:
         self.compileClassVarDec()

        while t.tokenType() == JackTockenizer.KEYWORD and t.keyWord() in ['constructor', 'function', 'method']:
         self.compileSubroutineDec()

        self.process('}')
        
        self.end("class")

    def compileClassVarDec(self):
        self.begin("classVarDec")
        t = self.tokenizer

        kind = t.keyWord()
        self.process(t.keyWord())

        type = self.processType()

        assert t.tokenType() == JackTockenizer.IDENTIFIER
        name = t.identifier()

        self.classST.define(name=name, type=type, kind=kind)
        self.usage = 'declared'
        self.process(t.identifier())
        self.usage = 'usage'

        while t.tokenType() == JackTockenizer.SYMBOL and t.symbol() == ',':
           self.process(',')
           assert t.tokenType() == JackTockenizer.IDENTIFIER
           self.classST.define(name=t.identifier(), type=type, kind=kind)
           self.usage = 'declared'
           self.process(t.identifier())
           self.usage = 'usage'

        self.process(';')

        self.end("classVarDec")
        
    def compileSubroutineDec(self):
        t = self.tokenizer
        self.methodST = SymbolTable(parent=self.classST)
        st = self.methodST

        if t.keyWord() == 'method':
           st.define(name='this', type=st.parent.name, kind='arg')

        self.begin("subroutineDec")
        self.process(t.keyWord())

        # 'void' | type
        if t.tokenType() == JackTockenizer.KEYWORD and t.keyWord() == 'void': 
           self.process('void')
        else:
           self.processType()

        # varName        
        assert t.tokenType() == JackTockenizer.IDENTIFIER
        self.usage = "declared"
        st.name = t.identifier()
        self.process(t.identifier())
        self.usage = "usage"

        self.process('(')
        self.compileParameterList()
        self.process(')')

        self.compileSubroutineBody()

        self.end("subroutineDec")
        
    def compileParameterList(self):
      t = self.tokenizer
      st = self.methodST
      self.begin("parameterList")
      # ((type varName) (',' type varName)*)?
      if t.tokenType() != JackTockenizer.SYMBOL: # if its not ')' it must be a type
        type = self.processType()
        assert t.tokenType() == JackTockenizer.IDENTIFIER
        st.define(name=t.identifier(), type=type, kind='arg')
        self.usage = 'declare'
        self.process(t.identifier())

        # (',' type varName)*
        while t.symbol() == ',':
          assert t.tokenType() == JackTockenizer.SYMBOL
          self.process(',')
          type =  self.processType()
          assert t.tokenType() == JackTockenizer.IDENTIFIER
          st.define(name=t.identifier(), type=type, kind='arg')
          self.usage = 'declare'
          self.process(t.identifier())

      self.end("parameterList")

    def processType(self):
       type = None
       t = self.tokenizer
       if t.tokenType() == JackTockenizer.KEYWORD:
          assert t.keyWord() in ['int', 'char', 'boolean']
          type = t.keyWord()
          self.process(t.keyWord())
       else:
          assert t.tokenType() == JackTockenizer.IDENTIFIER
          type = t.identifier()
          self.process(t.identifier())

       return type
    
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
      type = self.processType()
      assert t.tokenType() == JackTockenizer.IDENTIFIER
      self.methodST.define(name=t.identifier(), type=type, kind='var')
      self.usage = 'declared'
      self.process(t.identifier())
      self.usage = 'usage'

      # (',' varName)*
      while t.tokenType() == JackTockenizer.SYMBOL and t.symbol() == ',':
         self.methodST.define(name=t.identifier(), type=type, kind='var')
         self.usage = 'declared'
         self.process(',')
         assert t.tokenType() == JackTockenizer.IDENTIFIER
         self.process(t.identifier())
         self.usage = 'usage'

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
       t = self.tokenizer
       self.begin('ifStatement')

       self.process('if')
       self.process('(')
       self.compileExpression()
       self.process(')')

       self.process('{')
       self.compileStatements()
       self.process('}')

       # (else '{' statement '}')?
       if t.tokenType() == JackTockenizer.KEYWORD and t.keyWord() == 'else':
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
         op = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
         if t.tokenType() == JackTockenizer.SYMBOL and t.symbol() in op:
            self.process(t.symbol())
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
        st = None
        usage = self.usage
        identifier = self.tokenizer.identifier()
        if self.methodST and identifier in self.methodST.st:
           st = self.methodST
        elif identifier in self.classST.st:
           st = self.classST

        if st:
         identifier = {
            "name": identifier,
            "type": st.typeOf(identifier),
            "category": st.kindOf(identifier),
            "index": st.indexOf(identifier),
            "usage": usage
         }
        else:
         if identifier == self.classST.name   : category = "class"
         elif self.methodST and identifier == self.methodST.name: category = "subroutine"
         else                                 : category = "class"
         identifier = {
            "name": identifier,
            "category": category,
            "usage": usage
         }
        self.printToken("identifier", str(identifier))

    def printSymbol(self):
        symbol = self.tokenizer.symbol()
        if symbol in CompilationEngine.special_symbols:
         symbol = CompilationEngine.special_symbols[symbol]
        self.printToken("symbol", symbol)

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

    special_symbols = {
      '>': '&gt;',
      '<': '&lt;',
      '&': '&amp;',
      '"': '&quot;',
    } 