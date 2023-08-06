class TemplateError(Exception):
    pass

class TemplateContextError(TemplateError):
    def __init__(self, var: str):
        self.var = var
    
    def __str__(self) -> str:
        return "'%s' is not resolvable" % self.var


class TemplateSyntaxError(TemplateError):

    def __init__(self, error):
        self.error = error

    def __str__(self) -> str:
        return "invalid syntax: %s" % self.error


        
