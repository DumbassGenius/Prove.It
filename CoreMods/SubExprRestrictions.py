from CoreBackend.ModManager import *
from CoreBackend.Expressions import *



class ExprType:
    def __init__(self, name:str, *parents):
        if len(parents) == 0 and name!= "any":
            self.parents = [AnyType()]
        else:
            self.parents = EnsureIsListOf(parents, ExprType)
        self.name = EnsureIsType(name, str)

    def subTypeOf(self, exprType):
        if self is exprType:
            return True
        else: return any([parent.subTypeOf(exprType) for parent in self.parents])

    def __le__(self, exprType):
        return self.subTypeOf(exprType)

    # Return a Variable of this type
    def __call__(self, symbol, context: Context = None):
        if context != None and (to_ret := context.GetVar(symbol)) != None:
            return to_ret
        else:
            to_ret = Var(self, symbol)
            if context != None:
                context.addVarToContext(to_ret)
            return to_ret
        
    def __repr__(self):
        return self.name

class AnyType(ExprType):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return
        super().__init__("any")
        self._initialized = True
        self._immutable = True

    def __setattr__(self, key, value):
        if hasattr(self, "_immutable") and self._immutable:
            raise AttributeError("Global anyType is immutable.")
        super().__setattr__(key, value)


class BasicRestrictions(Mod):
    dependencies = []
    reverseDependencies = []

    def onConstructInit(self, construct, **kwargs):
        EnsureIsType(construct, Construct)
        if "numSubExprs" in kwargs:
            EnsureIsType(kwargs["numSubExprs"], int)
            construct.numSubExprs = kwargs["numSubExprs"]
        else:
            construct.numSubExprs = None

    def onExprInit(self, expr, *subExprs, **kwargs):
        EnsureIsType(expr, Expr) 
        if expr.construct.numSubExprs is not None and len(subExprs) != expr.construct.numSubExprs:
            raise ValueError(f"Expression {expr} requires {expr.construct.numSubExprs} sub-expressions, but got {len(subExprs)}.")
        
        
