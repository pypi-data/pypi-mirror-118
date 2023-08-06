from tex.helper import resolve, eval_expression
from tex.exceptions import TemplateSyntaxError, TemplateError
from tex.vars import WHITESPACE, operator_lookup_table
import operator

class Node(object):
    create_scope: bool = False

    def __init__(self, fragment=None):
        print(fragment)
        self.children: list = []
        self.process_fragment(fragment)

    def process_fragment(self, fragment):
        pass

    def enter_scope(self):
        pass

    def render(self, context):
        pass

    def exit_scope(self):
        pass

    def render_children(self, context, children=None):
        print("render child ", context, children)
        if children is None:
            children = self.children

        def render_child(child):
            print(child)
            child_html = child.render(context)
            return '' if not child_html else str(child_html)
        return ''.join(map(render_child, children))


class ScopableNode(Node):
    create_scope: bool = True


class Root(Node):
    def render(self, context):
        return self.render_children(context)


class Variable(Node):
    def process_fragment(self, fragment):
        self.name = fragment

    def render(self, context):
        return resolve(self.name, context)


class Each(ScopableNode):
    def process_fragment(self, fragment):
        try:
            _, it = WHITESPACE.split(fragment, 1)
            self.it = eval_expression(it)
        except ValueError:
            raise TemplateSyntaxError(fragment)

    def render(self, context):
        items = items = self.it[1] if self.it[0] == 'literal' else resolve(
            self.it[1], context)
        def render_item(item):
            return self.render_children({'..': context, 'it': item})
        return ''.join(map(render_item, items))


class If(ScopableNode):
    def process_fragment(self, fragment):
        bits = fragment.split()[1:]
        if len(bits) not in (1, 3):
            raise TemplateSyntaxError(fragment)
        self.lhs = eval_expression(bits[0])
        if len(bits) == 3:
            self.op = bits[1]
            self.rhs = eval_expression(bits[2])

    def render(self, context):
        lhs = self.resolve_side(self.lhs, context)
        if hasattr(self, 'op'):
            op = operator_lookup_table.get(self.op)
            if op is None:
                raise TemplateSyntaxError(self.op)
            rhs = self.resolve_side(self.rhs, context)
            exec_if_branch = op(lhs, rhs)
        else:
            exec_if_branch = operator.truth(lhs)
        if_branch, else_branch = self.split_children()
        return self.render_children(context,
                                    self.if_branch if exec_if_branch else self.else_branch)

    def resolve_side(self, side, context):
        return side[1] if side[0] == 'literal' else resolve(side[1], context)

    def exit_scope(self):
        self.if_branch, self.else_branch = self.split_children()

    def split_children(self):
        if_branch, else_branch = [], []
        curr = if_branch
        for child in self.children:
            if isinstance(child,Else):
                curr = else_branch
                continue
            curr.append(child)
        return if_branch, else_branch

class Else(Node):
    def render(self, context):
        pass

class Call(Node):
    def process_fragment(self, fragment):
        try:
            bits = WHITESPACE.split(fragment)
            self.callable = bits[1]
            self.args, self.kwargs = self._parse_params(bits[2:])
        except (ValueError, IndexError):
            raise TemplateSyntaxError(fragment)

    def _parse_params(self, params):
        args, kwargs = [], {}
        for param in params:
            if '=' in param:
                name, value = param.split('=')
                kwargs[name] = eval_expression(value)
            else:
                args.append(eval_expression(param))
        return args, kwargs

    def render(self, context):
        resolved_args, resolved_kwargs = [], {}
        for kind, value in self.args:
            if kind == 'name':
                value = resolve(value, context)
            resolved_args.append(value)
        for key, (kind, value) in self.kwargs.items():
            if kind == 'name':
                value = resolve(value, context)
            resolved_kwargs[key] = value
        resolved_callable = resolve(self.callable, context)
        if hasattr(resolved_callable, '__call__'):
            return resolved_callable(*resolved_args, **resolved_kwargs)
        else:
            raise TemplateError("'%s' is not a callable" % self.callable)

class Text(Node):
    def process_fragment(self, fragment):
        self.text = fragment

    def render(self, context):
        return self.text