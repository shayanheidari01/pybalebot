from .send_message import SendMessage
from .edit_message_text import EditMessageText


class Messages(
    SendMessage,
    EditMessageText
):
    pass