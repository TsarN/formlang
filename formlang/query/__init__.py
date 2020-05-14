import io
import sys

from antlr4 import CommonTokenStream, BailErrorStrategy
from antlr4.error.Errors import ParseCancellationException
from antlr4.error.ErrorListener import ErrorListener
from antlr4.tree.Tree import TerminalNode

from formlang.contextfree import Grammar
from formlang.query.queryLexer import queryLexer
from formlang.query.queryParser import queryParser
from formlang.query.visitor import QueryVisitor


class ParseError(Exception):
    pass


class MyErrorListener( ErrorListener ):
    def __init__(self):
        super(MyErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise ParseError()

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        raise ParseError()

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        raise ParseError()

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        raise ParseError()



def parse_query(what):
    lexer = queryLexer(what)
    stream = CommonTokenStream(lexer)
    parser = queryParser(stream)
    tree = parser.script()
    visitor = QueryVisitor()
    visitor.visitScript(tree)
    return visitor.statements


def verify_query(what):
    lexer = queryLexer(what)
    stream = CommonTokenStream(lexer)
    parser = queryParser(stream)
    parser.removeErrorListeners()
    parser._errHandler = BailErrorStrategy()
    parser.buildParseTrees = False
    try:
        parser.script()
        return True
    except ParseCancellationException:
        return False


def print_tree_as_dot(tree, file_obj=sys.stdout):
    print("digraph {", file=file_obj)
    print("    rankdir=LR;", file=file_obj)

    n = 0

    def doit(node):
        nonlocal n
        idx = n
        n += 1

        if isinstance(node, TerminalNode):
            text = node.getText()
        else:
            for child in node.getChildren():
                print(f"    n{idx} -> n{doit(child)};")
            text = queryParser.ruleNames[node.getRuleIndex()]

        text = text.replace('"', '\\"')
        print(f"    n{idx} [label=\"{text}\"];", file=file_obj)

        return idx

    doit(tree)

    print("}", file=file_obj)
