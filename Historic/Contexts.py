from TypeCheckers import *

class Context:
    def __init__(self):
        self.scopes = []
        self.currentScope = {}
        self.scopes.append(self.currentScope)

    def pushLocalScopes(self, local:dict = None):
        local:dict = Initiate(local)
        self.scopes.append(local)
        self.currentScope = local

    def popLocalScopes(self):
        if len(self.scopes) > 0:
            self.currentScope = self.scopes[-1]
        else:
            self.currentScope = {}
        self.scopes.pop()

    def addVarToContext(self, var):
        self.currentScope[var.symbol] = var

    def GetVar(self, symbol):
        for scope in reversed(self.scopes):
            if symbol in scope:
                return scope[symbol]
        return None