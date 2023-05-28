from  jack_tockenizer import JackTockenizer
import sys, os, glob

class JackAnalyzer:
    def __init__(self, fn):
      self.fns, self.fns_out = self.getFiles(fn)

    def getFiles(self, fn):
      if os.path.isfile(fn): fns_in = [fn]
      else:                  fns_in = glob.glob(fn + '/*.jack')

      fns_out = [self.genFnOut(fn_in) for fn_in in fns_in]
      print("output: " + str(fns_out))
      return (fns_in, fns_out)
      
    def genFnOut(self, fn_in):
      idx = fn_in.find(".jack")
      base = fn_in[:idx]
      fn_out =  base + "TT.xml"
      return fn_out

    def process(self):
      for i in range(len(self.fns)):
        fn = self.fns[i]
        fn_out = self.fns_out[i]
        with open(fn, 'r') as fin:
          with open(fn_out, 'w') as fout:
            self.fout = fout
            self.tokenizer = JackTockenizer(fin)
            tokenizer = self.tokenizer
            self.tokensBegin()
            while tokenizer.hasMoreTokens():
              tokenizer.advance()
              self.processToken()
            self.tokensEnd()

    def tokensBegin(self):
      self.fout.write('<tokens>\n')

    def tokensEnd(self):
      self.fout.write('</tokens>\n')

    type_map = {
      JackTockenizer.KEYWORD      : 'keyword',
      JackTockenizer.SYMBOL       : 'symbol',
      JackTockenizer.IDENTIFIER   : 'identifier',
      JackTockenizer.INT_CONST    : 'integerConstant',
      JackTockenizer.STRING_CONST : 'stringConstant',
    }

    def beginTokenType(self, type):
      self.fout.write('<' + JackAnalyzer.type_map[type] +'>')

    def endTokenType(self, type):
      self.fout.write('</' + JackAnalyzer.type_map[type] +'>\n')

    def processToken(self):
      tokenizer = self.tokenizer
      type = tokenizer.tokenType()

      self.beginTokenType(type)

      if   type == JackTockenizer.KEYWORD     : self.processKeyword() 
      elif type == JackTockenizer.SYMBOL      : self.processSymbol() 
      elif type == JackTockenizer.IDENTIFIER  : self.processIdentifier() 
      elif type == JackTockenizer.INT_CONST   : self.processIntConst() 
      elif type == JackTockenizer.STRING_CONST: self.processStringConst() 

      self.endTokenType(type)

    special_symbols = {
      '>': '&gt;',
      '<': '&lt;',
      '&': '&amp;',
      '"': '&quot;',
    }

    def processKeyword(self):
      self.fout.write(' ' + self.tokenizer.keyWord() + ' ')

    def processIdentifier(self):
      self.fout.write(' ' + self.tokenizer.identifier() + ' ')

    def processSymbol(self):
      symbol = self.tokenizer.symbol()
      if symbol in JackAnalyzer.special_symbols:
        symbol = JackAnalyzer.special_symbols[symbol]
      self.fout.write(' ' + symbol + ' ')

    def processIntConst(self):
      self.fout.write(' ' + str(self.tokenizer.intVal()) + ' ')

    def processStringConst(self):
      self.fout.write(' ' + self.tokenizer.stringVal() + ' ')

def main():
  #fn = '../ArrayTest/Main.jack'
  #fn = 'Test.jack'
  fn = sys.argv[1]
  analyzer = JackAnalyzer(fn)
  analyzer.process()

if __name__ == '__main__':
   main()