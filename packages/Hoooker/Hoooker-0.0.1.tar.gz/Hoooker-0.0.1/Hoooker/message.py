class MessageBase:
    def __init__(self, message_type: str):
        self.message_type = message_type

    def to_line_format(self) -> dict:
        raise NotImplementedError


class TextMessage(MessageBase):
    def __init__(self, message_content):
        super().__init__('text')
        self.message_content = message_content

    def to_line_format(self):
        return {"type": self.message_type, "text": self.message_content}