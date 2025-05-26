
from TypeCheckers import *
from ModManager import ModManager

manager = ModManager()

class Construct:
# Constructs define symbolic relations. They behave as a user defined class for expressions. Calling a construct returns an expression, with the input expressions as it's subexpressions. 
# Construct can be called with any kwargs, and all the attributes will be assigned to the construct, and passed on the plugins
    def __init__(self, **kwargs):
        manager.ConstructInit(self,**kwargs)

    # Creates a new expression, applies the construction function to it, and returns it. 
    def __call__(self, *subExprs, **kwargs):
        EnsureIsListOf(subExprs, Expr)
        return Expr(self, *subExprs, **kwargs)

# These are instances of symbolic relations, defined via constructs. 
class Expr:

    # Expressions are partially initialized, and then the construction function will finish initiaizing it. 
    def __init__(self, construct: Construct, *subExprs, **kwargs):
        self.construct = EnsureIsType(construct, Construct)
        self.subExprs = EnsureIsListOf(subExprs, Expr)
        self.numSubExprs = len(self.subExprs)
        self.isvar = False

        manager.ExprInit(self, *subExprs, **kwargs)
    
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
    def __init__(self, **kwargs):
        self.subExprs = []
        self.numSubExprs = 0
        self.construct = None
        self.isvar = True

        manager.onVarInit(self, **kwargs)
    
    # Variables are equal iff their id is equal
    def __eq__(self, value):
        return id(self) == id(value)

    def __repr__(self):
        return f"Var({id(self)})"



