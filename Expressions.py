from TypeCheckers import *

constructs = {}

types = {}

context = [{}]

def addVarToContext(var):
    context[-1][var.symbol] = var

def pushLocalContext(local:dict = None):
    local:dict = Initiate(local)
    context.append(local)

def popLocalContext():
    return context.pop()

def GetVar(symbol):
    for scope in reversed(context):
        if symbol in scope:
            return scope[symbol]
    return None



class ExprType:
    def __init__(self, name:str, *parents):
        if len(parents) == 0 and name!= "any":
            parents = [anyType]
        else:
            self.parents = EnsureIsListOf(parents, ExprType)
        self.name = EnsureIsType(name, str)

        types[name] = self

    def subTypeOf(self, exprType):
        if self == exprType:
            return True
        else: return any([parent.subTypeOf(exprType) for parent in self.parents])

    # Return a Variable of this type
    def __call__(self, symbol):
        inContext = GetVar(symbol)
        if inContext:
            return inContext
        else:
            return Var()

anyType = ExprType("any", )

class Construct:
    def __init__(self, call: str, inputTypes: list, outputType: ExprType, renderFunct):
        self.call = EnsureIsType(call, str)
        self.inputTypes = EnsureIsListOf(inputTypes, ExprType)
        self.numInputs = len(inputTypes)

        self.outputType = EnsureIsType(outputType, ExprType)

        if isinstance(renderFunct, function):        
            self.renderFunct = EnsureIsType(renderFunct, function)
        elif isinstance(renderFunct, str):
            lambda renderedSubExprs: renderFunct.format(*renderedSubExprs)
        else:
            raise TypeError(renderFunct, "must be a str or function")
        constructs[call] = self

    def __call__(self, *subExprs):
        EnsureIsListOf(subExprs, Expr)
        return Expr(self, *subExprs)
        

class Expr:
    def __init__(self, construct: Construct, *subExprs):
        self.subExprs = EnsureIsListOf(subExprs, Expr)
        self.numSubExprs = len(subExprs)

        if self.numSubExprs != construct.numInputs:
            raise ValueError(subExprs, "must have length", construct.numInputs)

        for subExpr, inputType in zip(self.subExprs, construct.inputTypes):
            if subExpr.type != inputType:
                raise ValueError(subExpr, "is not a", inputType)


        self.construct = EnsureIsType(construct, Construct)

        self.type = construct.outputType

        self.vars = set().update(*[subExpr.vars for subExpr in subExprs])
    
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
        return self.subExprs
    
    def __len__(self):
        return self.numSubExprs


class Var(Expr):
    def __init__(self, type: ExprType, symbol):
        self.subExprs = []
        self.numSubExprs = 0
        self.construct = None
        self.type: ExprType = EnsureIsType(type, ExprType)
        self.symbol: str = EnsureIsType(symbol, str)

        addVarToContext(self)

    def render(self):
        return self.symbol
    
    # Variables are equal iff their id is equal, it is NOT dependent on the symbol used. 
    def __eq__(self, value):
        return id(self) == id(value)
