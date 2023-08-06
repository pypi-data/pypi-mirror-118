import typing
import ast
from tex_engine.exceptions import TemplateError, TemplateContextError, TemplateSyntaxError

def eval_expression(expr) -> typing.Tuple[str, typing.Any]:
    try:
        return "literal", ast.literal_eval(expr)
    except (ValueError, SyntaxError):
        return "name", expr

def resolve(name: str, context):
    if name.startswith(".."):
        context = context.get("..", {})
        name = name[2:]
    try:
        for token in name.split("."):
            context = context[token]
        return context
    except KeyError:
        raise TemplateContextError(name)

