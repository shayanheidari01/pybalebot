from pybalebot import Client, filters
from pybalebot.types import Message

app = Client('my_bot', bot_token='1234567890:Jj2hM8yaRaD*********************')

@app.on_message()
async def hello(client, message: Message):
    await message.reply('Hello from PyBaleBot!')

app.run()
