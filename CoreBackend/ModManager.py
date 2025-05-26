from TypeCheckers import *

class Mod:
    def onConstructInit(self, construct, **kwargs):
        pass
    def onExprInit(self, expr, *subExprs, **kwargs):
        pass
    def onVarInit(self, var, **kwargs):
        pass



class ModManager:
    _instance = None  # Class variable to store the single instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.mods = []

    def turnOnMods(self, *mods):
        self.mods.extend(EnsureIsListOf(mods, Mod))

    def turnOffMods(self, *mods):
        EnsureIsListOf(mods, Mod)
        self.mods = [mod for mod in self.mods if mod not in mods]

    def ConstructInit(self, construct, **kwargs):
        for mod in self.mods:
            mod.onConstructInit(construct, **kwargs)
    
    def ExprInit(self, expr, *subExprs, **kwargs):
        for mod in self.mods:
            mod.onConstructInit(expr, *subExprs, **kwargs)

    def onVarInit(self, var, **kwargs):
        for mod in self.mods:
            mod.onVarInit(var, **kwargs)
