class Code:
    
    def dest(self, mnemonic):
        m = mnemonic
        if m == None:   return '000'
        if m == 'M':    return '001'
        if m == 'D':    return '010'
        if m == 'MD':   return '011'
        if m == 'A':    return '100'
        if m == 'AM':   return '101'
        if m == 'AD':   return '110'
        if m == 'ADM':  return '111'
        return None

        
    def jump(self, mnemonic):
        m = mnemonic
        if m == None:  return '000'
        if m == 'JGT': return '001'
        if m == 'JEQ': return '010'
        if m == 'JGE': return '011'
        if m == 'JLT': return '100'
        if m == 'JNE': return '101'
        if m == 'JLE': return '110'
        if m == 'JMP': return '111'
        return None
        
    def comp(self, mnemonic):
        prefix = '111'
        m = mnemonic
        
        if   m == '0':                    comp = '101010'
        elif m == '1':                    comp = '111111'
        elif m == '-1':                   comp = '111010'
        elif m == 'D':                    comp = '001100'
        elif m == 'A' or m == 'M':        comp = '110000'
        elif m == '!D':                   comp = '001101'
        elif m == '!A' or m == '!M':      comp = '110001'
        elif m == '-D':                   comp = '001111'
        elif m == '-A' or m == '-M':      comp = '110011'
        elif m == 'D+1':                  comp = '011111'
        elif m == 'A+1' or m == 'M+1':    comp = '110111'
        elif m == 'D-1':                  comp = '001110'
        elif m == 'A-1' or m == 'M-1':    comp = '110010'
        elif m == 'D+A' or m == 'D+M':    comp = '000010'
        elif m == 'D-A' or m == 'D-M':    comp = '010011'
        elif m == 'A-D' or m == 'M-D':    comp = '000111'
        elif m == 'D&A' or m == 'D&M':    comp = '000000'
        elif m == 'D|A' or m == 'D|M':    comp = '010101'        
        else:                             return None

        return prefix + ('1' if 'M' in m else '0') + comp

if __name__ == '__main__':
    c = MyCode()
    r=c.comp('D')
    print(r)
