from enum import Enum


class DefaultUtils:
    def remove_html_tags(text: str) -> str:
        return text.replace('<', '').replace('>', '')

class CustomBase:
    def __init__(self, original):
        for attr in dir(original):
            if not attr.startswith('_'):
                setattr(self, attr, getattr(original, attr))

class CustomCall(CustomBase):
    def __init__(self, original_call):
        super().__init__(original_call)
        self.answer = original_call.message.edit_text

class CustomMessage(CustomBase):
    def __init__(self, original_call):
        super().__init__(original_call)
        self.answer = original_call.edit_text

class BalanceOperation(Enum):
    ADD = "+"
    SUBTRACT = "-"
    SET = "="