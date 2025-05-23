from Expressions import *
def defaultConstructionCreater(inputTypes, outputType):
    EnsureIsType(outputType, ExprType)
    EnsureIsListOf(inputTypes, ExprType)
    def defaultConstruction(self: Expr, *subExprs):
        self.subExprs = EnsureIsListOf(subExprs, Expr)
        self.numSubExprs = len(subExprs)

        if self.numSubExprs != len(inputTypes):
            raise ValueError(f"Expected {len(inputTypes)} subexpressions, but got {self.numSubExprs}")

        for subExpr, inputType in zip(self.subExprs, inputTypes):
            if not subExpr.type <= inputType:
                raise ValueError(f"Subexpression {subExpr} is not of type {inputType}")        

        self.type = outputType
        print(type(self.type))
        self.freevars = set().union(*[subExpr.freevars for subExpr in subExprs])
    defaultConstruction.inputTypes = inputTypes
    defaultConstruction.outputType = outputType
    return defaultConstruction

def quantifierConstructionCreater(vartype, exprtype):
    def quantifierConstruction(self: Expr, var: Var, expr: Expr):
        subExprs = [expr, var]
        self.subExprs = EnsureIsListOf(subExprs, Expr)
        self.numSubExprs = 2

        if expr.type != exprtype:
            raise ValueError(f"Expression {expr} is not of type {exprtype}")

        
        if var.type != vartype:
            raise ValueError(f"Variable {var} is not of type {vartype}")        

        self.type = exprtype

        self.freevars = expr.freevars - {var}
        self.isvar = True

    return quantifierConstruction
