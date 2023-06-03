class SymbolTable:
    def __init__(self, parent=None, name=None):
        self.name = name
        self.parent = parent
        self._init()

    def _init(self):
        self.kinds = {kind: 0 for kind in ['STATIC', 'FIELD', 'ARG', 'VAR', 'NONE']}
        self.st = dict()

    def reset(self):
        self._init()

    def define(self, name, type, kind):
        kind = kind.upper()
        st = self.st
        st[name] = {
          "type": type,
          "kind": kind,
          "index": self.kinds[kind]
        }
        self.kinds[kind] += 1
        
    def varCount(self, kind):
        return self.kinds['kind']

    def kindOf(self, name):
        return self.st[name]['kind']

    def typeOf(self, name):
        return self.st[name]['type']

    def indexOf(self, name):
        return self.st[name]['index']