
from TypeCheckers import *
from Contexts import *


class Construct:
# Constructs define symbolic relations. They behave as a user defined class for expressions. Calling a construct returns an expression, with the input expressions as it's subexpressions. 
# The construction function will define how expressions are created. The mods will add additional functionality to expressions. They will act on expressions and return nothing, or raise an error. 
    def __init__(self, construction, *mods):
        self.construction = EnsureIsType(construction, function)

    # Creates a new expression, applies the construction function to it, and returns it. 
    def __call__(self, *subExprs):
        EnsureIsListOf(subExprs, Expr)
        newexpr = Expr(self)
        self.construction(newexpr, *subExprs)
        for mod in self.mods: 
            mod(newexpr)
        return newexpr
        
# These are instances of symbolic relations, defined via constructs. 
class Expr:

    # Expressions are partially initialized, and then the construction function will finish initiaizing it. 
    def __init__(self, construct: Construct):
        self.construct = EnsureIsType(construct, Construct)
        self.subExprs = []
        self.numSubExprs = 0
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

    def __repr__(self):
        return f"Expr({self.construct}, {self.subExprs}"

# These are the bass instances of Expressions, used to create other expressions. 
class Var(Expr):
    def __init__(self, symbol):
        self.subExprs = []
        self.numSubExprs = 0
        self.construct = None
        self.symbol: str = EnsureIsType(symbol, str)
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
        return f"Var({self.symbol}, {id(self)})"



