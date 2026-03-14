# parser.py
import ast

def parse_code(code: str):
    try:
        tree = ast.parse(code)
        return tree
    except Exception as e:
        print("Parsing error:", e)
        return None