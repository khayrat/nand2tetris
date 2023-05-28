import sys
from hack_parser import Parser
from hack_code_gen import CodeGen

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
    def dec2bin(dec_str):
        return bin(int(dec_str)).replace("0b", "")
    def add_padding(bin_str):
      max_len = 16
      act_len = len(bin_str)
      padding = max_len - act_len
      return '0' * padding + bin_str

    symbol = parser.symbol()
    if symbol.isdigit():
      return add_padding(dec2bin(symbol))
    else: 
      assert False # not jet implemented

  def handle_lable():
    pass

  def generate_fn(fn):
    idx = fn.find(".asm")
    base = fn[:idx]
    return base + ".hack"

  fn_in = sys.argv[1]
  #fn_in = "../max/MaxL.asm"
  fn_out = generate_fn(fn_in)
  print(fn_out)
  with open(fn_out, 'w') as fout:
    with open(fn_in, 'r') as fin:
      parser = Parser(fin)
      gen = CodeGen()

      while (parser.hasMoreLines()):
        parser.advance()

        instruction = ''

        if (parser.instructionType()) == Parser.A_INSTRUCTION:
          instruction = assemble_a_instruction()

        elif (parser.instructionType()) == Parser.L_INSTRUCTION:
          handle_lable()
        else:
          instruction = assemble_comp()

#        print(instruction)
        fout.write(instruction + '\n')
        instruction = ''

if __name__ == "__main__":
  main()