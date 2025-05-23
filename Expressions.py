from types import FunctionType as function
from TypeCheckers import *
from Contexts import *

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


class Construct:
    def __init__(self, renderFunct, construction):
        self.construction = EnsureIsType(construction, function)

        if isinstance(renderFunct, function):        
            self.renderFunct = renderFunct
        elif isinstance(renderFunct, str):
            self.renderFunct = lambda renderedSubExprs: renderFunct.format(*renderedSubExprs)
        else:
            raise TypeError(f"renderFunct must be a function or a string, got {type(renderFunct).__name__}")


    def __call__(self, *subExprs):
        EnsureIsListOf(subExprs, Expr)
        newexpr = Expr(self)
        self.construction(newexpr, *subExprs)
        return newexpr
        

class Expr:
    def __init__(self, construct: Construct):
        self.construct = EnsureIsType(construct, Construct)
        self.subExprs = []
        self.numSubExprs = 0
        self.type = AnyType()
        self.renderFunct = lambda renderedSubExprs: "UNINITIALIZED"
        self.freevars = set()
        self.isvar = False
    
    # First subexprs are all rendered, then plugged into the rendering function of the construct
    def render(self):
        renderedSubExprs = [subExpr.render() for subExpr in self.subExprs]
        return self.construct.renderFunct(renderedSubExprs)
    
    # Expressions are equal when they have the same construct, and their subexpressions are equal. 
    def __eq__(self, value):
        if not isinstance(value, Expr) or value.construct != self.construct:
            return False
        return all([selfSubExpr == valueSubExpr for selfSubExpr, valueSubExpr in zip(self.subExprs, value.subExprs)])

    def __getitem__(self, num: int):
        return self.subExprs[num]
    
    def __iter__(self):
        return iter(self.subExprs)
    
    def __len__(self):
        return self.numSubExprs

    def display(self):
        print(self.render())

    def __repr__(self):
        return f"Expr({self.construct}, {self.subExprs}"

class Var(Expr):
    def __init__(self, type: ExprType, symbol):
        self.subExprs = []
        self.numSubExprs = 0
        self.construct = None
        self.type: ExprType = EnsureIsType(type, ExprType)
        self.symbol: str = EnsureIsType(symbol, str)
        self.freevars = {self}
        self.renderFunct = lambda renderedSubExprs: symbol
        self.isvar = True

    def render(self):
        return self.symbol
    
    # Variables are equal iff their id is equal, it is NOT dependent on the symbol used. 
    def __eq__(self, value):
        return id(self) == id(value)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return f"Var({self.type}, {self.symbol}, {id(self)})"



