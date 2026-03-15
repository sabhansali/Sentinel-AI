# engine.py
from .parser import parse_code
from .obfuscator import CodeObfuscator
from .mapper import ast_to_code

def sanitize_code(code: str):
    tree = parse_code(code)
    if tree is None:
        return {"status": "error", "message": "Code parsing failed"}

    obfuscator = CodeObfuscator()
    new_tree = obfuscator.visit(tree)
    sanitized_code = ast_to_code(new_tree)
    mapping = obfuscator.sanitizer.get_mapping()

    return {
        "status": "success",
        "sanitized_code": sanitized_code,
        "mapping": mapping
    }

def restore_names(text: str, mapping: dict):
    reverse = {v:k for k,v in mapping.items()}
    for safe,original in reverse.items():
        text = text.replace(safe,original)
    return text
    


# Example usage (optional, for testing)
if __name__ == "__main__":
    code = """
class PaymentService:
    def process_payment(self, user_id, credit_card_number):
        transaction = charge_card(credit_card_number)
        self.save_transaction(user_id, transaction)

    def save_transaction(self, user_id, transaction):
        database.insert_transaction(user_id, transaction)
"""
    result = sanitize_code(code)
    print("Sanitized Code:\n", result["sanitized_code"])
    print("Mapping:\n", result["mapping"])