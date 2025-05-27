from TypeCheckers import *

class Mod:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModManager, cls).__new__(cls)
        return cls._instance
    
    dependencies = []
    reverseDependencies = []

    def __init__(self):
        for dep in self.dependencies:
            EnsureIsType(dep, Mod)
            dep.reverseDependencies.append(self)


    def onConstructInit(self, construct, **kwargs):
        pass
    def onExprInit(self, expr, *subExprs, **kwargs):
        pass
    def onVarInit(self, var, **kwargs):
        pass



class ModManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.mods = []

    # Returns true if mods were successfully turned on
    def turnOnMods(self, *mods):
        EnsureIsListOf(mods, Mod)
        for mod in mods:
            if mod not in self.mods:
                self.turnOnMods(mod.dependencies)
                self.mods.append(mod)
        return True


    # Returns true if mods were successfully turned off
    def turnOffMods(self, *mods):
        EnsureIsListOf(mods, Mod)
        for mod in mods:
            if mod in self.mods:
                for revdep in mod.reverseDependencies:
                    if revdep in self.mods and not revdep in mods:
                            print(f"Warning: {revdep} is a dependency of {mod} but is not being turned off. As a result no mods will be turned off.")
                            return False
        for mod in mods:
            if mod in self.mods:
                self.mods.remove(mod)

    def ConstructInit(self, construct, **kwargs):
        for mod in self.mods:
            mod.onConstructInit(construct, **kwargs)
    
    def ExprInit(self, expr, *subExprs, **kwargs):
        for mod in self.mods:
            mod.onConstructInit(expr, *subExprs, **kwargs)

    def onVarInit(self, var, **kwargs):
        for mod in self.mods:
            mod.onVarInit(var, **kwargs)
