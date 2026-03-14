# sanitizer.py
class NameSanitizer:
    def __init__(self):
        self.mapping = {}
        self.counter = 1

    def get_name(self, original: str) -> str:
        if original not in self.mapping:
            new_name = f"id_{self.counter}"
            self.mapping[original] = new_name
            self.counter += 1
        return self.mapping[original]

    def get_mapping(self) -> dict:
        return self.mapping