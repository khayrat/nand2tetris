class CodeGen():
  dest_dict = { 
    'null': '000',
    'M': '001',
    'D': '010',
    'DM': '011',
    'MD': '011',
    'A': '100',
    'AM': '101',
    'MA': '101',
    'AD': '110',
    'DA': '110',
    'ADM': '111',
    'AMD': '111',
    'DAM': '111',
    'DMA': '111',
    'MAD': '111',
    'MDA': '111'
  }
  jump_dict = { 
    'null': '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111'
  }
  comp_dict = { 
    '0':   '0101010',
    '1':   '0111111',
    '-1':  '0111010',
    'D':   '0001100',
    'A':   '0110000',
    '!D':  '0001101',
    '!A':  '0110001',
    '-D':  '0001111',
    '-A':  '0110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'D+A': '0000010',
    'D-A': '0010011',
    'A-D': '0010011',
    'D&A': '0000000',
    'D|A': '0010101',
    'M':   '1110000',
    '!M':  '1110001',
    '-M':  '1110011',
    'M+1': '1110111',
    'M-1': '1110010',
    'D+M': '1000010',
    'D-M': '1010011',
    'M-D': '1000111',
    'D&M': '1000000',
    'D|M': '1010101',
  }

  def dest(self, sym):
    return CodeGen.dest_dict[sym]

  def jump(self, sym):
    return CodeGen.jump_dict[sym]

  def comp(self, sym):
    return CodeGen.comp_dict[sym]

class Test():
  def test_dest(self):
    # setup
    dests = ['null', 'M',   'D',   'DM',  'A',   'AM',  'AD',  'ADM']
    codes = ['000',  '001', '010', '011', '100', '101', '110', '111']

    dest_dict = { 
      'null': '000',
      'M': '001',
      'D': '010',
      'DM': '011',
      'A': '100',
      'AM': '101',
      'AD': '110',
      'ADM': '111'
    }

    gen = CodeGen()

    for sym, code in dest_dict.items():
      assert gen.dest(sym) == code

  def test_comp(self):
    comp_dict = { 
      '0':   '0101010',
      '1':   '0111111',
      '-1':  '0111010',
      'D':   '0001100',
      'A':   '0110000',
      '!D':  '0001101',
      '!A':  '0110001',
      '-D':  '0001111',
      '-A':  '0110011',
      'D+1': '0011111',
      'A+1': '0110111',
      'D-1': '0001110',
      'A-1': '0110010',
      'D+A': '0000010',
      'D-A': '0010011',
      'A-D': '0010011',
      'D&A': '0000000',
      'D|A': '0010101',
      'M':   '1110000',
      '!M':  '1110001',
      'M+1': '1110111',
      'D+M': '1000010',
      'D-M': '1010011',
      'M-D': '1000111',
      'D&M': '1000000',
      'D|M': '1010101',
    }
    gen = CodeGen()

    for sym, code in comp_dict.items():
      assert gen.comp(sym) == code

  def test_jump(self):
    jump_dict = { 
      'null': '000',
      'JGT': '001',
      'JEQ': '010',
      'JGE': '011',
      'JLT': '100',
      'JNE': '101',
      'JLE': '110',
      'JMP': '111'
    }

    gen = CodeGen()

    for sym, code in jump_dict.items():
      assert gen.jump(sym) == code

def test_suite():
  test = Test()
  test.test_dest()
  test.test_comp()
  test.test_jump()
  
if __name__ == "__main__":
  test_suite()
