from  jack_compilation_engine import CompilationEngine
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
      fn_out =  base + "AA.xml"
      return fn_out

    def process(self):
      for i in range(len(self.fns)):
        fn = self.fns[i]
        fn_out = self.fns_out[i]
        with open(fn, 'r') as fin:
          with open(fn_out, 'w') as fout:
            compiler = CompilationEngine(fin, fout)
            compiler.compileClass()


def main():
  fn = '/Users/glende/Projects/aktuell/nand2tetris/projects/10/ExpressionLessSquare'
  #fn = 'Test.jack'
  #fn = sys.argv[1]
  analyzer = JackAnalyzer(fn)
  analyzer.process()

if __name__ == '__main__':
   main()