class Environment:
    def __init__(self):
        # name -> value
        self.vars = {}
        # name -> value
        self.consts = {}


    def set_var(self, name, value):
        self.vars[name] = value


    def get_var(self, name):
        if name in self.vars:
            return self.vars[name]
        if name in self.consts:
            return self.consts[name]
        raise NameError(f"Variable '{name}' not defined")


    def set_const(self, name, value):
        if name in self.consts:
            raise ValueError(f"Constant '{name}' already defined")
        self.consts[name] = value
