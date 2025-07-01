class Node:
    """Base class for all AST nodes."""
    pass


class Program(Node):
    def __init__(self, statements):
        self.statements = statements


class VarDecl(Node):
    def __init__(self, name, type_, value):
        self.name = name
        # Can be None
        self.type_ = type_
        # Can be None
        self.value = value


class ConstDecl(Node):
    def __init__(self, name, type_, value):
        self.name = name
        self.type_ = type_
        self.value = value


class FunctionDef(Node):
    def __init__(self, name, params, return_type, body):
        self.name = name
        self.params = params
        self.return_type = return_type
        # Block
        self.body = body


class Param(Node):
    def __init__(self, name, type_, default):
        self.name = name
        self.type_ = type_
        self.default = default


class Block(Node):
    def __init__(self, statements):
        self.statements = statements


class IfStmt(Node):
    def __init__(self, condition, then_block, else_block):
        self.condition = condition
        self.then_block = then_block
        # Can be None
        self.else_block = else_block


class ForStmt(Node):
    def __init__(self, var_name, iterable, body):
        self.var_name = var_name
        self.iterable = iterable
        self.body = body


class MatchStmt(Node):
    def __init__(self, expr, cases, else_block):
        self.expr = expr
        # List of (case_value, case_block)
        self.cases = cases
        # Can be None
        self.else_block = else_block


class FunctionCall(Node):
    def __init__(self, name, args):
        self.name = name
        # List of expressions
        self.args = args


class ReturnStmt(Node):
    def __init__(self, value):
        self.value = value


class RaiseStmt(Node):
    def __init__(self, exception_type, message):
        self.exception_type = exception_type
        self.message = message


class TryStmt(Node):
    def __init__(self, try_block, except_blocks):
        self.try_block = try_block
        # List of (exception_type(s), block)
        self.except_blocks = except_blocks


class Expression(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Literal(Node):
    def __init__(self, value):
        self.value = value


class Identifier(Node):
    def __init__(self, name):
        self.name = name


class CodeBlock(Node):
    def __init__(self, params, body):
        self.params = params  # List of Param
        self.body = body


class MacroDef(Node):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body


class ComptimeDef(Node):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body


class TypeDef(Node):
    def __init__(self, name, base_type, fields, methods):
        self.name = name
        self.base_type = base_type  # Can be None
        self.fields = fields  # List of VarDecl
        self.methods = methods  # List of FunctionDef
