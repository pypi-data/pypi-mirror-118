from tex_engine.fragment import Fragment
from tex_engine.node import Root, If, Each, Call, Else, Variable, Text
from tex_engine.exceptions import TemplateError, TemplateSyntaxError
from tex_engine.vars import TOK_REGEX, CLOSE_BLOCK_FRAGMENT, TEXT_FRAGMENT, VAR_TOKEN_START, OPEN_BLOCK_FRAGMENT, VAR_FRAGMENT

class Compiler(object):
    def __init__(self, template_string):
        self.template_string = template_string

    def each_fragment(self):
        for fragment in TOK_REGEX.split(self.template_string):
            if fragment:
                yield Fragment(fragment)

    def compile(self):
        root = Root()
        scope_stack = [root]
        for fragment in self.each_fragment():
            if not scope_stack:
                raise TemplateError('nesting issues')
            parent_scope = scope_stack[-1]
            if fragment.type == CLOSE_BLOCK_FRAGMENT:
                parent_scope.exit_scope()
                scope_stack.pop()
                continue
            new_node = self.create_node(fragment)
            if new_node:
                parent_scope.children.append(new_node)
                if new_node.create_scope:
                    scope_stack.append(new_node)
                    new_node.enter_scope()
        return root

    def create_node(self, fragment):
        node_class = None
        if fragment.type == TEXT_FRAGMENT:
            node_class = Text
        elif fragment.type == VAR_FRAGMENT:
            node_class = Variable
        elif fragment.type == OPEN_BLOCK_FRAGMENT:
            cmd = fragment.clean.split()[0]
            if cmd == 'each':
                node_class = Each
            elif cmd == 'if':
                node_class = If
            elif cmd == 'else':
                node_class = Else
            elif cmd == 'call':
                node_class = Call
        if node_class is None:
            raise TemplateSyntaxError(fragment)
        return node_class(fragment.clean)