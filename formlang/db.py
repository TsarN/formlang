import io
import os

from formlang.algo.regex import productions_from_regex
from formlang.contextfree import Grammar, Production
from formlang.graph import read_graph_from_file
from formlang.query.ast import *


class FileDatabase:
    def __init__(self):
        self.path = None

    def get_graph(self, name):
        with open(os.path.join(self.path, name)) as f:
            return read_graph_from_file(f)

    def list_graphs(self):
        return sorted(os.listdir(self.path))


class DictDatabase:
    def __init__(self, data):
        self.data = data
        self.path = None

    def get_graph(self, name):
        return read_graph_from_file(io.StringIO(self.data[name]))

    def list_graphs(self):
        return sorted(list(self.data))


class Executor:
    def __init__(self, db):
        self.db = db
        self.ctx = Grammar()

    def execute(self, statement):
        if type(statement) == ConnectStatement:
            self.db.path = statement.path
        elif type(statement) == ListGraphsStatement:
            print("\n".join(self.db.list_graphs()))
        elif type(statement) == RuleStatement:
            self.ctx.productions += productions_from_regex(statement.lhs, statement.rhs)
        elif type(statement) == SelectStatement:
            tmp = Nonterminal()
            prods = productions_from_regex(tmp, statement.path_expr)
            self.ctx.productions += prods
            self.ctx.start = tmp
            graph = self.db.get_graph(statement.graph_name)
            result = self.ctx.path_query(graph)
            # TODO: do something more sophisticated
            if result:
                print("TRUE")
            else:
                print("FALSE")
        else:
            raise ValueError("Invalid statement")

    def execute_many(self, statements):
        for statement in statements:
            self.execute(statement)
