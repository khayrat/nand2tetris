class Parser:
  A_INSTRUCTION = 0
  C_INSTRUCTION = 1
  L_INSTRUCTION = 2
  
  def __init__(self, fh):
    self.fh = fh
    self._lookahead()
    self.currentInstruction = None
    self.pc = 0

  def hasMoreLines(self):
    return True if self.lookaheadLine else False

  def _lookahead(self):
    while True:
      tmpLine = self.fh.readline()

      if not tmpLine: break

      # ignore comment on instruction line
      idx = tmpLine.find("//")
      if idx != -1: tmpLine = tmpLine[:idx]

      # clean ws
      tmpLine = ''.join(tmpLine.split())

      if not tmpLine: continue

      # skip comment lines
      if tmpLine.startswith('//'): continue
      else: break

    self.lookaheadLine = tmpLine

  def _parse_instruction(self):
    def parse_dest():
      idx = self.currentLine.find('=')
      if (idx != -1): instruction["dest"] = self.currentLine[:idx]
      else: instruction["dest"] = 'null'

    def parse_jump():
      idx = self.currentLine.find(';')
      if (idx != -1): instruction["jump"] = self.currentLine[idx+1:]
      else: instruction["jump"] = 'null'

    def parse_comp():
      start_idx = self.currentLine.find('=')
      if (start_idx == -1): start_idx = 0
      else: start_idx += 1
      end_idx = self.currentLine.find(';')
      if (end_idx == -1): end_idx = None
      instruction["comp"] = self.currentLine[start_idx:end_idx]

    instruction = dict()
    if self.currentLine.startswith("@"):
      self.pc += 1
      instruction["type"] = Parser.A_INSTRUCTION
      instruction["symbol"] = self.currentLine[1:]
    elif self.currentLine.startswith("("):
      instruction["type"] = Parser.L_INSTRUCTION
      instruction["symbol"] = self.currentLine[1:-1]
    else:
      self.pc += 1
      instruction["type"] = Parser.C_INSTRUCTION
      parse_dest()
      parse_jump()
      parse_comp()

    self.currentInstruction = instruction

  def advance(self):
    self.currentLine = self.lookaheadLine
    self._lookahead()

    self._parse_instruction()

  def instructionType(self):
    return self.currentInstruction["type"]

  def symbol(self):
    return self.currentInstruction["symbol"]

  def dest(self):
    return self.currentInstruction["dest"]

  def comp(self):
    return self.currentInstruction["comp"]

  def jump(self):
    return self.currentInstruction["jump"]

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

    def test_skipWhiteSpaces():
      try:
        # setup
        lines_w_ws = ["  @123", "\t 0001", " dest = ; jump  "]
        lines_clean = ["@123", "0001", "dest=;jump"]
        self.prepare_file(lines_w_ws)
        parser = Parser(self.fd)
        
        for expectedLine in lines_clean:
          # action
          parser.advance()
          # check
    #      print("'%s'" % parser.currentLine)
          assert parser.currentLine == expectedLine
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
          assert parser.currentLine == lines_clean[i-1]

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
        assert parser.currentLine == "123"
        assert parser.hasMoreLines()

        # action
        parser.advance()

        # check
        assert parser.currentLine == "@546"
        assert not parser.hasMoreLines()

      finally:
        # tear down
        self.clean_file()
    test_oneLine()
    test_twoLines()
    test_skipWhiteSpaces()
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

  def test_instructionType(self):
    def test_a_instruction():
      try:
        # setup
        a_instruction_line = ["@123"]
        self.prepare_file(a_instruction_line)
        parser = Parser(self.fd)

        # action
        parser.advance()

        # check
        assert parser.instructionType() == Parser.A_INSTRUCTION

      finally:
        # teardown
        self.clean_file()

    def test_c_instruction():
      try:
        # setup
        c_instruction_line = ["M = D + 1; JMP"]
        self.prepare_file(c_instruction_line)
        parser = Parser(self.fd)

        # action
        parser.advance()

        # check
        assert parser.instructionType() == Parser.C_INSTRUCTION

      finally:
        # teardown
        self.clean_file()

    def test_l_instruction():
      try:
        # setup
        instruction_line = ["(LOOP)"]
        self.prepare_file(instruction_line)
        parser = Parser(self.fd)

        # action
        parser.advance()

        # check
        assert parser.instructionType() == Parser.L_INSTRUCTION

      finally:
        # teardown
        self.clean_file()

    test_a_instruction()
    test_c_instruction()
    test_l_instruction()

  def test_symbol(self):
    def test_l_instruction():
      try:
        # setup
        instruction_line = ["(LOOP)"]
        self.prepare_file(instruction_line)
        parser = Parser(self.fd)

        # action
        parser.advance()

        # check
        assert parser.instructionType() == Parser.L_INSTRUCTION
        assert parser.symbol() == "LOOP"

      finally:
        # teardown
        self.clean_file()

    def test_a_instruction_var():
      try:
        # setup
        instruction_line = ["@xxx"]
        self.prepare_file(instruction_line)
        parser = Parser(self.fd)

        # action
        parser.advance()

        # check
        assert parser.instructionType() == Parser.A_INSTRUCTION
        assert parser.symbol() == "xxx"

      finally:
        # teardown
        self.clean_file()

    def test_a_instruction_num():
      try:
        # setup
        instruction_line = ["@123"]
        self.prepare_file(instruction_line)
        parser = Parser(self.fd)

        # action
        parser.advance()

        # check
        assert parser.instructionType() == Parser.A_INSTRUCTION
        assert parser.symbol() == "123"

      finally:
        # teardown
        self.clean_file()

    test_l_instruction()
    test_a_instruction_var()
    test_a_instruction_num()

  def test_dest(self):
    dests = ['null', 'M', 'D', 'DM', 'A', 'AM', 'AD', 'ADM']
    instruction_lines = []
    try:
      # setup
      for dest in dests:
        instruction_lines.append("%s = comp; jmp" % dest)

      self.prepare_file(instruction_lines)
      parser = Parser(self.fd)

      for dest in dests:
        # action
        parser.advance()

        # check
        assert parser.instructionType() == Parser.C_INSTRUCTION
        assert parser.dest() == dest

    finally:
      # teardown
      self.clean_file()

  def test_jump(self):
    jumps = ['null', 'JGT', 'JEQ', 'JGE', 'JLT', 'JNE', 'JLE', 'JMP']
    instruction_lines = []
    try:
      # setup
      for jump in jumps:
        instruction_lines.append("comp; %s" % jump)

      self.prepare_file(instruction_lines)
      parser = Parser(self.fd)

      for jump in jumps:
        # action
        parser.advance()

        # check
        assert parser.instructionType() == Parser.C_INSTRUCTION
        assert parser.jump() == jump

    finally:
      # teardown
      self.clean_file()

  def test_comp(self):
    comps = ['0', '1', '-1', 'D', 'A', '!D', '!A', '-D', '-A', 'D+1', 'A+1']
    instruction_lines = []
    try:
      # setup
      for comp in comps:
        instruction_lines.append("dest = %s; jump" % comp)
        instruction_lines.append("%s; jump" % comp)

      self.prepare_file(instruction_lines)
      parser = Parser(self.fd)

      for comp in comps:
        # action
        parser.advance()

        # check
        assert parser.instructionType() == Parser.C_INSTRUCTION
        assert parser.comp() == comp

        # action
        parser.advance()

        # check
        assert parser.instructionType() == Parser.C_INSTRUCTION
        assert parser.comp() == comp
    finally:
      # teardown
      self.clean_file()

def test_suite():
  test = Test()

  test.test_hasMoreLines()
  test.test_advance()
  test.test_instructionType()
  test.test_symbol()
  test.test_dest()
  test.test_jump()
  test.test_comp()

if __name__ == "__main__":
  test_suite()
