# obfuscator.py
import ast
from .sanitizer import NameSanitizer

class CodeObfuscator(ast.NodeTransformer):
    def __init__(self):
        self.sanitizer = NameSanitizer()

    # rename variables
    def visit_Name(self, node):
        node.id = self.sanitizer.get_name(node.id)
        return node

    # rename functions
    def visit_FunctionDef(self, node):
        node.name = self.sanitizer.get_name(node.name)
        self.generic_visit(node)
        return node

    # rename classes
    def visit_ClassDef(self, node):
        node.name = self.sanitizer.get_name(node.name)
        self.generic_visit(node)
        return node

    # rename attributes (object.property)
    def visit_Attribute(self, node):
        node.attr = self.sanitizer.get_name(node.attr)
        self.generic_visit(node)
        return node