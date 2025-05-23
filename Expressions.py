# Expressions.py

import TypeCheckers
import types

constructs = {}

exprTypes = {}

context = [{}]

def add_var_to_context(var):
    context[-1][var.symbol] = var

def push_local_context(local: dict = None):
    local = TypeCheckers.Initiate(local, dict)
    context.append(local)

def pop_local_context():
    return context.pop()

def get_var(symbol):
    for scope in reversed(context):
        if symbol in scope:
            return scope[symbol]
    return None

class ExprType:
    def __init__(self, name: str, *parents):
        self.name = TypeCheckers.EnsureIsType(name, str)
        if name == "any":
            self.parents = []
        elif len(parents) == 0:
            self.parents = [exprTypes["any"]]
        else:
            self.parents = TypeCheckers.EnsureIsListOf(list(parents), ExprType)
        exprTypes[name] = self

    def sub_type_of(self, expr_type):
        if self == expr_type:
            return True
        else:
            return any(parent.sub_type_of(expr_type) for parent in self.parents)

    # Return a variable of this type
    def __call__(self, symbol):
        in_context = get_var(symbol)
        if in_context:
            return in_context
        else:
            return Var(self, symbol)

    def __repr__(self):
        return f"ExprType({self.name})"

anyType = ExprType("any")

class Construct:
    def __init__(self, call: str, input_types: list, output_type: ExprType, render_funct):
        self.call = TypeCheckers.EnsureIsType(call, str)
        self.input_types = TypeCheckers.EnsureIsListOf(input_types, ExprType)
        self.num_inputs = len(input_types)

        self.output_type = TypeCheckers.EnsureIsType(output_type, ExprType)

        if isinstance(render_funct, types.FunctionType):
            self.render_funct = TypeCheckers.EnsureIsType(render_funct, types.FunctionType)
        elif isinstance(render_funct, str):
            self.render_funct = lambda rendered_sub_exprs: render_funct.format(*rendered_sub_exprs)
        else:
            raise TypeError(f"{render_funct} must be a str or function")
        constructs[call] = self

    def __call__(self, *sub_exprs):
        TypeCheckers.EnsureIsListOf(list(sub_exprs), Expr)
        return Expr(self, *sub_exprs)

    def __repr__(self):
        return f"Construct({self.call})"

class Expr:
    def __init__(self, construct: Construct, *sub_exprs):
        self.sub_exprs = TypeCheckers.EnsureIsListOf(list(sub_exprs), Expr)
        self.num_sub_exprs = len(sub_exprs)

        if self.num_sub_exprs != construct.num_inputs:
            raise ValueError(f"Expected {construct.num_inputs} subexpressions but got {self.num_sub_exprs}")

        for sub_expr, input_type in zip(self.sub_exprs, construct.input_types):
            if sub_expr.type != input_type:
                raise ValueError(f"Subexpression {sub_expr} is not of type {input_type}")

        self.construct = TypeCheckers.EnsureIsType(construct, Construct)
        self.type = construct.output_type

        # Collect variables from all subexpressions
        self.vars = set()
        for sub_expr in sub_exprs:
            self.vars.update(sub_expr.vars)

     # First subexprs are all rendered, then plugged into the rendering function of the construct
    def render(self):
        rendered_sub_exprs = [sub_expr.render() for sub_expr in self.sub_exprs]
        return self.construct.render_funct(rendered_sub_exprs)

     # Expressions are equal when they have the same construct, and their subexpressions are equal. 
    def __eq__(self, other):
        if not isinstance(other, Expr) or other.construct != self.construct:
            return False
        return all(s == o for s, o in zip(self.sub_exprs, other.sub_exprs))

    def __getitem__(self, num: int):
        return self.sub_exprs[num]

    def __iter__(self):
        return iter(self.sub_exprs)

    def __len__(self):
        return self.num_sub_exprs

    def __repr__(self):
        return f"Expr({self.construct.call}, {self.sub_exprs})"

class Var(Expr):
    def __init__(self, type_: ExprType, symbol: str):
        self.sub_exprs = []
        self.num_sub_exprs = 0
        self.construct = None
        self.type = TypeCheckers.EnsureIsType(type_, ExprType)
        self.symbol = TypeCheckers.EnsureIsType(symbol, str)
        add_var_to_context(self)
        self.vars = {self}

    def render(self):
        return self.symbol

    # Variables are equal iff their id is equal, it is NOT dependent on the symbol used. 
    def __eq__(self, other):
        return id(self) == id(other)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return f"Var({self.symbol}:{self.type.name})"
