from pybalebot import Router
from pybalebot.filters import Filter
from pybalebot.types import Message

router = Router()


class MyFilter(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text

    async def __call__(self, message: Message) -> bool:
        return message.text == self.my_text


@router.message(MyFilter("hello"))
async def my_handler(message: Message):
    ...
