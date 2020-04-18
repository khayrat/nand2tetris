import symboltable

def test():
    st=symboltable.SymbolTable()

    assert st.contains('KBD')
    assert st.contains('SCREEN')
    assert st.contains('R10')

    assert st.getAddress('R14') == '14'
    assert st.getAddress('THIS') == '3'

    assert not st.contains('BLUBS')
    st.addEntry('BLUBS', '4711')
    assert st.getAddress('BLUBS') == '4711'
