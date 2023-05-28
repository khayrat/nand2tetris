class SymbolTable():
  def __init__(self):
    sb = {'R'+ str(i): i for i in range(16)}
    sb['SP']     = 0
    sb['LCL']    = 1
    sb['ARG']    = 2
    sb['THIS']   = 3
    sb['THAT']   = 4
    sb['SCREEN'] = 16384
    sb['KBD']    = 24576
    self.sb = sb
    self.next_address = 16

  def addEntry(self, symbol, address=None):
    if not address:
      address = self.next_address
      self.next_address += 1

    self.sb[symbol] = address

  def contains(self, symbol): 
    return symbol in self.sb

  def getAddress(self, symbol):
    return self.sb[symbol]
