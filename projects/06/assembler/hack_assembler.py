import sys
from hack_parser import Parser
from hack_code_gen import CodeGen
from hack_symbol_table import SymbolTable

def main():
  def assemble_comp():
    dest_sym = parser.dest()
    comp_sym = parser.comp()
    jump_sym = parser.jump()
    dest = gen.dest(dest_sym)
    comp = gen.comp(comp_sym)
    jump = gen.jump(jump_sym)

    c_instruction = "111%s%s%s" % (comp, dest, jump)
    return (c_instruction)
        
  def assemble_a_instruction():
    def symbol2Address(symbol):
      if not symbol.isdigit():
        if not sb.contains(symbol): sb.addEntry(symbol)
        return sb.getAddress(symbol)
      else: return symbol
    def dec2bin(dec_str):
        return bin(int(dec_str)).replace("0b", "")
    def add_padding(bin_str):
      max_len = 16
      act_len = len(bin_str)
      padding = max_len - act_len
      return '0' * padding + bin_str

    return add_padding(dec2bin(symbol2Address(parser.symbol())))

  def populate_label():
    symbol = parser.symbol()
    sb.addEntry(symbol, parser.pc)

  def generate_fn(fn):
    idx = fn.find(".asm")
    base = fn[:idx]
    return base + ".hack"

  def first_pass():
    while (parser.hasMoreLines()):
      parser.advance()

      if (parser.instructionType()) == Parser.L_INSTRUCTION:
        populate_label()

  def second_pass():
    while (parser.hasMoreLines()):
      parser.advance()

      instruction = ''

      if (parser.instructionType()) == Parser.A_INSTRUCTION:
        instruction = assemble_a_instruction()

      elif (parser.instructionType()) == Parser.L_INSTRUCTION:
        continue # already handled in first pass
      else:
        instruction = assemble_comp()

      if instruction:
        fout.write(instruction + '\n')

  fn_in = sys.argv[1]
  #fn_in = "../max/Max.asm"
  fn_out = generate_fn(fn_in)
  print(fn_out)

  sb = SymbolTable()
  # first pass
  with open(fn_in, 'r') as fin:
    parser = Parser(fin)
    first_pass()

  # second pass
  with open(fn_out, 'w') as fout:
    with open(fn_in, 'r') as fin:
      parser = Parser(fin)
      gen = CodeGen()
      second_pass()

if __name__ == "__main__":
  main()