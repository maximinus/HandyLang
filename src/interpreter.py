from src.ast_nodes import *


class Interpreter:
    def __init__(self, environment):
        self.env = environment


    def run(self, program):
        for stmt in program.statements:
            self.eval(stmt)


    def eval(self, node):
        if isinstance(node, VarDecl):
            value = self.eval(node.value) if node.value else self.default_value(node.type_)
            self.env.set_var(node.name, value)
        elif isinstance(node, ConstDecl):
            value = self.eval(node.value)
            self.env.set_const(node.name, value)
        elif isinstance(node, FunctionCall):
            if node.name == "print":
                for arg in node.args:
                    val = self.eval(arg)
                    print(val)
            else:
                raise NotImplementedError(f"Function '{node.name}' not implemented")
        elif isinstance(node, Literal):
            return self.parse_literal_value(node.value)
        elif isinstance(node, Identifier):
            return self.env.get_var(node.name)
        else:
            raise NotImplementedError(f"Node type {type(node)} not implemented yet")


    def parse_literal_value(self, value):
        # Convert string representations to actual Python types
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        if "." in value:
            return float(value)
        return int(value)


    def default_value(self, type_):
        if type_ == "int":
            return 0
        elif type_ == "float":
            return 0.0
        elif type_ == "string":
            return ""
        else:
            raise ValueError(f"No default value defined for type '{type_}'")
