# mapper.py
import ast

def ast_to_code(tree: ast.AST) -> str:
    try:
        return ast.unparse(tree)
    except Exception as e:
        print("AST Unparse Error:", e)
        return ""