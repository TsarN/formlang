# Generated from query.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .queryParser import queryParser
else:
    from queryParser import queryParser

# This class defines a complete listener for a parse tree produced by queryParser.
class queryListener(ParseTreeListener):

    # Enter a parse tree produced by queryParser#script.
    def enterScript(self, ctx:queryParser.ScriptContext):
        pass

    # Exit a parse tree produced by queryParser#script.
    def exitScript(self, ctx:queryParser.ScriptContext):
        pass


    # Enter a parse tree produced by queryParser#statement.
    def enterStatement(self, ctx:queryParser.StatementContext):
        pass

    # Exit a parse tree produced by queryParser#statement.
    def exitStatement(self, ctx:queryParser.StatementContext):
        pass


    # Enter a parse tree produced by queryParser#connect_statement.
    def enterConnect_statement(self, ctx:queryParser.Connect_statementContext):
        pass

    # Exit a parse tree produced by queryParser#connect_statement.
    def exitConnect_statement(self, ctx:queryParser.Connect_statementContext):
        pass


    # Enter a parse tree produced by queryParser#list_graphs_statement.
    def enterList_graphs_statement(self, ctx:queryParser.List_graphs_statementContext):
        pass

    # Exit a parse tree produced by queryParser#list_graphs_statement.
    def exitList_graphs_statement(self, ctx:queryParser.List_graphs_statementContext):
        pass


    # Enter a parse tree produced by queryParser#rule_statement.
    def enterRule_statement(self, ctx:queryParser.Rule_statementContext):
        pass

    # Exit a parse tree produced by queryParser#rule_statement.
    def exitRule_statement(self, ctx:queryParser.Rule_statementContext):
        pass


    # Enter a parse tree produced by queryParser#select_statement.
    def enterSelect_statement(self, ctx:queryParser.Select_statementContext):
        pass

    # Exit a parse tree produced by queryParser#select_statement.
    def exitSelect_statement(self, ctx:queryParser.Select_statementContext):
        pass


    # Enter a parse tree produced by queryParser#objexpr.
    def enterObjexpr(self, ctx:queryParser.ObjexprContext):
        pass

    # Exit a parse tree produced by queryParser#objexpr.
    def exitObjexpr(self, ctx:queryParser.ObjexprContext):
        pass


    # Enter a parse tree produced by queryParser#vsinfo.
    def enterVsinfo(self, ctx:queryParser.VsinfoContext):
        pass

    # Exit a parse tree produced by queryParser#vsinfo.
    def exitVsinfo(self, ctx:queryParser.VsinfoContext):
        pass


    # Enter a parse tree produced by queryParser#whereexpr.
    def enterWhereexpr(self, ctx:queryParser.WhereexprContext):
        pass

    # Exit a parse tree produced by queryParser#whereexpr.
    def exitWhereexpr(self, ctx:queryParser.WhereexprContext):
        pass


    # Enter a parse tree produced by queryParser#vexpr.
    def enterVexpr(self, ctx:queryParser.VexprContext):
        pass

    # Exit a parse tree produced by queryParser#vexpr.
    def exitVexpr(self, ctx:queryParser.VexprContext):
        pass


    # Enter a parse tree produced by queryParser#pattern.
    def enterPattern(self, ctx:queryParser.PatternContext):
        pass

    # Exit a parse tree produced by queryParser#pattern.
    def exitPattern(self, ctx:queryParser.PatternContext):
        pass


    # Enter a parse tree produced by queryParser#seq.
    def enterSeq(self, ctx:queryParser.SeqContext):
        pass

    # Exit a parse tree produced by queryParser#seq.
    def exitSeq(self, ctx:queryParser.SeqContext):
        pass


    # Enter a parse tree produced by queryParser#star.
    def enterStar(self, ctx:queryParser.StarContext):
        pass

    # Exit a parse tree produced by queryParser#star.
    def exitStar(self, ctx:queryParser.StarContext):
        pass


    # Enter a parse tree produced by queryParser#unit.
    def enterUnit(self, ctx:queryParser.UnitContext):
        pass

    # Exit a parse tree produced by queryParser#unit.
    def exitUnit(self, ctx:queryParser.UnitContext):
        pass



del queryParser