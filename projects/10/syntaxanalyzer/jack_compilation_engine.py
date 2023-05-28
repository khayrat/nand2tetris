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
       # self.process('}')
        
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

            # void | type
            if t.tokenType() == JackTockenizer.KEYWORD: self.process("void")
            else:
                assert t.tokenType() == JackTockenizer.IDENTIFIER
                self.process(t.identifier())
                
            assert t.tokenType() == JackTockenizer.IDENTIFIER
            self.process(t.identifier())

            self.process('(')
            self.compileParameterList()
            self.process(')')

            self.compileSubroutineBody()

            self.end("subroutineDec")
        return found
        
    def compileParameterList(self):
      self.begin("parameterList")
      self.end("parameterList")
    
    def compileSubroutineBody(self):
      self.begin("subroutineBody")

      self.process('{')
      while self.compileVarDec(): pass
      self.compileStatements()
      #self.process('}')

      self.end("subroutineBody")
    
    def compileStatements(self):
      self.begin("statements")
      self.end("statements")

    def compileVarDec(self):
      self.begin("varDec")
      self.end("varDec")
    
    def compileLet(self):
        pass
    
    def compileIf(self):
        pass
    
    def compileWhile(self):
        pass
    
    def compileDo(self):
        pass
    
    def compileReturn(self):
        pass
    
    def compileExpression(self):
        pass
    
    def compileTerm(self):
        pass

    # return the number of expressions in the list.
    def compileExpressionList(self):
        pass
    
    def compileReturn(self):
        pass
    

#### helper
    def printKeyWord(self, token):
        self.printToken("keyword", token.lexeme)

    def printIdentifier(self, token):
        self.printToken("identifier", token.lexeme)

    def printSymbol(self, token):
        self.printToken("symbol", token.lexeme)

    emitt_map = {
        JackTockenizer.KEYWORD: printKeyWord,
        JackTockenizer.IDENTIFIER: printIdentifier,
        JackTockenizer.SYMBOL: printSymbol,
    }

    def process(self, lexeme):
        token = self.tokenizer.currentToken
        assert token.lexeme == lexeme

        CompilationEngine.emitt_map[token.type](self, token)

        self.tokenizer.advance()

    def printToken(self, type, lexeme, padding=0):
      self.fout.write(padding * ' ')
      self.fout.write('<%s> %s </%s>\n' %(type, lexeme, type))

    def begin(self, s, padding=0):
      self.fout.write(padding * ' ' + '<' + s + '>\n')

    def end(self, s, padding=0):
      self.fout.write(padding * ' ' + '</' + s + '>\n')