class Parser:
  C_ARITHMETIC = 0
  C_PUSH       = 1
  C_POP        = 2
  C_LABEL      = 3
  C_GOTO       = 4
  C_IF         = 5
  C_FUNCTION   = 6
  C_RETURN     = 7
  C_CALL       = 8
  
  def __init__(self, fh):
    self.fh = fh
    self.lookaheadLineParts = None
    self._lookahead()
    self.currentCommand = None

  def hasMoreLines(self):
    return True if self.lookaheadLineParts else False

  def _lookahead(self):
    while True:
      tmpLine = self.fh.readline()

      if not tmpLine: break # EOF

      # ignore comment on instruction line
      idx = tmpLine.find("//")
      if idx != -1: tmpLine = tmpLine[:idx]

      # split line into tokens
      lineParts = tmpLine.split()

      if len(lineParts) == 0: continue

      # skip comment lines
      if lineParts[0] == '//': continue
      else: self.lookaheadLineParts = lineParts; break

  def _parse_command(self):
    self.currentCommand = dict()

    def parse_arithmetic_logical():
      self.currentCommand['type'] = Parser.C_ARITHMETIC
      self.currentCommand['arg1'] = self.currentLineParts[0]

    def parse_push_pop():
      #print("### push and pop")
      if self.currentLineParts[0] == "push": self.currentCommand['type'] = Parser.C_PUSH
      else:                                 self.currentCommand['type'] = Parser.C_POP
      self.currentCommand['arg1'] = self.currentLineParts[1]
      self.currentCommand['arg2'] = self.currentLineParts[2]

    assert self.currentLineParts
    arithmetic_logic = ["add", "sub", "neg", "eq", "gt", "lt", "and" , "or", "not"]
    if self.currentLineParts[0] in arithmetic_logic: parse_arithmetic_logical(); return

    push_pop = ["push", "pop"]
    if self.currentLineParts[0] in push_pop: parse_push_pop(); return

  def advance(self):
    self.currentLineParts = self.lookaheadLineParts
    self.lookaheadLineParts = None
    self._lookahead()

    self._parse_command()

  def commandType(self):
    return self.currentCommand["type"]

  def arg1(self):
    return self.currentCommand["arg1"]

  def arg2(self):
    return self.currentCommand["arg2"]

##### tests ######

import os, tempfile
class Test():
  def prepare_file(self, lol):
    fd, path = tempfile.mkstemp()
    self.path = path    
    fd = open(path, 'w')
    fd.write('\n'.join(lol))
    fd.flush()
    fd.close()
    self.fd = open(path, 'r')

  def clean_file(self):
    self.fd.close()
    os.remove(self.path)

  def test_advance(self):
    def test_oneLine():
      try:
        # setup
        one_line = ["one liner"]
        self.prepare_file(one_line)
        parser = Parser(self.fd)

        # action
        parser.advance()
        # check
        assert parser.hasMoreLines() == False
      finally:
        # tear down
        self.clean_file()

    def test_twoLines():
      try:
        # setup
        two_lines = ["line 1", "line 2"]
        self.prepare_file(two_lines)
        parser = Parser(self.fd)

        # action
        parser.advance()
        # check
        assert parser.hasMoreLines() == True

        # action
        parser.advance()
        # check
        assert parser.hasMoreLines() == False
      finally:
        # tear down
        self.clean_file()

    def test_skipCommentsOnly():
      try:
        # setup
        lines_w_comments = [
          "// hallo das ist ein Kommentar", 
          "//@546"
        ]
        lines_clean = [
        ]
        self.prepare_file(lines_w_comments)
        parser = Parser(self.fd)

        i = 0
        while parser.hasMoreLines():
          i += 1
          # action
          parser.advance()

          # check
          assert parser.currentLine == lines_clean[i-1]

        assert len(lines_clean) == i
      finally:
        # tear down
        self.clean_file()

    def test_skipComments():
      try:
        # setup
        lines_w_comments = [
          "// hallo das ist ein Kommentar", 
          "@123",
          "//@546",
          "0011010101"
        ]
        lines_clean = [
          "@123", 
          "0011010101"
        ]
        self.prepare_file(lines_w_comments)
        parser = Parser(self.fd)

        i = 0
        while parser.hasMoreLines():
          i += 1
          # action
          parser.advance()

          # check
          assert parser.currentLineParts[0] == lines_clean[i-1]

        assert len(lines_clean) == i
      finally:
        # tear down
        self.clean_file()

    def test_skipEmptyLines():
      try:
        # setup
        lines_w_newlines = [
          "123", 
          "\n", 
          "@546"
        ]
        lines_clean = [
        ]
        self.prepare_file(lines_w_newlines)
        parser = Parser(self.fd)

        # action
        parser.advance()

        # check
        assert parser.currentLineParts[0] == "123"
        assert parser.hasMoreLines()

        # action
        parser.advance()

        # check
        assert parser.currentLineParts[0] == "@546"
        assert not parser.hasMoreLines()

      finally:
        # tear down
        self.clean_file()
    test_oneLine()
    test_twoLines()
    test_skipComments()
    test_skipCommentsOnly()
    test_skipEmptyLines()

  def test_hasMoreLines(self):
    def test_noLine():
      try:
        # setup
        one_line = []
        self.prepare_file(one_line)
        parser = Parser(self.fd)

        # check
        assert parser.hasMoreLines() == False

      finally:
        # teardown
        self.clean_file()

    def test_oneLine():
      try:
        # setup
        one_line = ["one liner"]
        self.prepare_file(one_line)
        parser = Parser(self.fd)

        # check
        assert parser.hasMoreLines() == True
      finally:
        # tear down
        self.clean_file()

    test_noLine()
    test_oneLine()

  def test_commandType(self):
    def test_arithmetic_command():
      try:
        # setup
        arithmetic_lines = ["add", "sub", "neg", "eq", "gt", "lt", "and" , "or", "not"]
        self.prepare_file(arithmetic_lines)
        parser = Parser(self.fd)

        for _ in arithmetic_lines:
          # action
          parser.advance()

          # check
          assert parser.commandType() == Parser.C_ARITHMETIC

      finally:
        # teardown
        self.clean_file()

    def test_push_pop_command():
      try:
        # setup
        segments = ["argument", "local", "static", "constant", "this", "that", "pointer", "temp"]
        push_lines = ["push %s 42" % segment for segment in segments]
        pop_lines  = ["pop %s 42" % segment for segment in segments]
        self.prepare_file(push_lines + pop_lines)
        parser = Parser(self.fd)

        for _ in push_lines:
          # action
          parser.advance()

          # check
          #print("checking: '%s'" % _)
          assert parser.commandType() == Parser.C_PUSH

        for _ in pop_lines:
          # action
          parser.advance()

          # check
          assert parser.commandType() == Parser.C_POP

      finally:
        # teardown
        self.clean_file()

    test_arithmetic_command()
    test_push_pop_command()

  def test_arg1(self):
    try:
      # setup
      arithmetic_lines = ["add", "sub", "neg", "eq", "gt", "lt", "and" , "or", "not"]
      self.prepare_file(arithmetic_lines)
      parser = Parser(self.fd)

      for _ in arithmetic_lines:
        # action
        parser.advance()

        # check
        assert parser.arg1() == _

    finally:
      # teardown
      self.clean_file()

  def test_arg2(self):
    try:
      # setup
      segments = ["argument", "local", "static", "constant", "this", "that", "pointer", "temp"]
      push_lines = ["push %s 42" % segment for segment in segments]
      pop_lines  = ["pop %s 42" % segment for segment in segments]
      self.prepare_file(push_lines + pop_lines)
      parser = Parser(self.fd)

      for _ in push_lines:
        # action
        parser.advance()

        # check
        #print("checking: '%s'" % _)
        assert parser.arg1() == _.split()[1]
        assert parser.arg2() == _.split()[2]

      for _ in pop_lines:
        # action
        parser.advance()

        # check
        #print("checking: '%s'" % _)
        assert parser.arg1() == _.split()[1]
        assert parser.arg2() == _.split()[2]

    finally:
      # teardown
      self.clean_file()

def test_suite():
  test = Test()

  test.test_hasMoreLines()
  test.test_advance()
  test.test_commandType()
  test.test_arg1()
  test.test_arg2()
  print("all tests passed.")

if __name__ == "__main__":
  test_suite()
