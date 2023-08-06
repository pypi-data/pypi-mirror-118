from tex_engine.compiler import Compiler

class Template(object):
    def __init__(self, contents):
        self.contents = contents
        self.root = Compiler(contents).compile()

    def render(self, **kwargs):
        return bytes(self.root.render(kwargs), "utf-8")
