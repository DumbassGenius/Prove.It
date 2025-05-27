from CoreBackend.ModManager import *
from CoreBackend.Expressions import *

class LatexRender(Mod):
    dependencies = []
    reverseDependencies = []

    def onConstructInit(self, construct, **kwargs):
        EnsureIsType(construct, Construct)
        if not "latex" in kwargs or not isinstance(kwargs["latex"], str):
            raise ValueError("LatexRender mod requires latex string to be passed in kwargs.")
        construct.latex = kwargs["latex"]

    def onExprInit(self, expr, *subExprs, **kwargs):
        EnsureIsType(expr, Expr)
        expr.latexRender = lambda: expr.construct.latex.format(*[subExpr.latexRender() for subExpr in subExprs])

    def onVarInit(self, var, **kwargs):
        EnsureIsType(var, Var)
        if not "symbol" in kwargs or not isinstance(kwargs["symbol"], str):
            raise ValueError("LatexRender mod requires symbol to be passed in kwargs.")
        var.symbol = kwargs["symbol"]
        var.latexRender = lambda: var.symbol