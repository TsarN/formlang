from formlang.query.queryVisitor import queryVisitor
from formlang.query.queryParser import queryParser

from formlang.query.ast import *

from antlr4.tree.Tree import TerminalNodeImpl


class QueryVisitor(queryVisitor):
    def __init__(self):
        self.statements = []

    def visitPattern(self, ctx:queryParser.PatternContext):
        res = []
        for child in ctx.getChildren():
            if type(child) == TerminalNodeImpl:
                continue
            res.append(self.visit(child))
        return " | ".join(res)

    def visitSeq(self, ctx:queryParser.SeqContext):
        res = []
        for child in ctx.getChildren():
            if type(child) == TerminalNodeImpl:
                continue
            res.append(self.visit(child))
        return " ".join(res)

    def visitStar(self, ctx:queryParser.StarContext):
        ret = self.visit(ctx.unit())
        if ctx.STAR():
            ret = f"{ret}*"
        return ret

    def visitUnit(self, ctx:queryParser.UnitContext):
        if ctx.NONTERMINAL():
            return str(ctx.NONTERMINAL())
        if ctx.IDENT():
            return str(ctx.IDENT())
        pat = self.visit(ctx.pattern())
        return f"({pat})"

    def visitWhereexpr(self, ctx:queryParser.WhereexprContext):
        return (
            self.visit(ctx.vexpr(0)),
            self.visit(ctx.vexpr(1)),
            self.visit(ctx.pattern()),
        )

    def visitVsinfo(self, ctx:queryParser.VsinfoContext):
        return list(map(str, ctx.IDENT()))

    def visitObjexpr(self, ctx:queryParser.ObjexprContext):
        if ctx.KW_COUNT():
            op = Operator.COUNT
        elif ctx.KW_EXISTS():
            op = Operator.EXISTS
        else:
            op = Operator.NONE

        return (
            op,
            self.visit(ctx.vsinfo())
        )


    def visitVexpr(self, ctx:queryParser.VexprContext):
        vexpr = VertexExpr(str(ctx.IDENT()), None)
        if vexpr.name == "_":
            vexpr.name = None
        if ctx.KW_ID():
            vexpr.vid = int(str(ctx.INT()))
        return vexpr

    def visitConnect_statement(self, ctx:queryParser.Connect_statementContext):
        self.statements.append(ConnectStatement(str(ctx.STRING())[1:-1]))

    def visitList_graphs_statement(self, ctx:queryParser.List_graphs_statementContext):
        self.statements.append(ListGraphsStatement())

    def visitRule_statement(self, ctx:queryParser.Rule_statementContext):
        self.statements.append(RuleStatement(
            Nonterminal(str(ctx.NONTERMINAL())),
            self.visit(ctx.pattern())
        ))

    def visitSelect_statement(self, ctx:queryParser.Select_statementContext):
        self.statements.append(SelectStatement(
            str(ctx.STRING())[1:-1],
            *self.visit(ctx.objexpr()),
            *self.visit(ctx.whereexpr())
        ))