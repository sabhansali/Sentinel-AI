from parser import parse_code
from obfuscator import CodeObfuscator
from mapper import ast_to_code

code = """

class PaymentService:

    def process_payment(self, user_id, credit_card_number):

        transaction = charge_card(credit_card_number)

        self.save_transaction(user_id, transaction)

    def save_transaction(self, user_id, transaction):

        database.insert_transaction(user_id, transaction)

"""

tree = parse_code(code)

obfuscator = CodeObfuscator()

new_tree = obfuscator.visit(tree)

sanitized_code = ast_to_code(new_tree)

print("\nOriginal Code:\n")
print(code)

print("\nSanitized Code:\n")
print(sanitized_code)