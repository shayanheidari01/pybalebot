<p align="center">
    <a href="github.address">
        <img src="https://dev.bale.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Farea7.e362c612.png&w=1080&q=75" alt="pybalebot" width="128">
    </a>
    <br>
    <b>Bale API Framework for Python</b>
    <br>
    <a href="https://github.com/shayanheidari01/pybalebot">
        Homepage
    </a>
    •
    <a href="https://docs.pybalebot.site/">
        Documentation
    </a>
    •
    <a href="https://pypi.org/project/pybalebot/#history">
        Releases
    </a>
    •
    <a href="https://t.me/rubika_library">
        News
    </a>
</p>

## PyBaleBot (ربات پیامرسان بله با پایتون)

> Modern and fully asynchronous framework for Bale Bot API

### Using Async
```python
from pybalebot import Client, filters
from pybalebot.types import Message

bot_token = "123456789:**********************"

app = Client("my_bot", bot_token=bot_token)

@app.on_message(filters.text)
async def hello(client, message: Message):
    await message.reply("Hello from PyBaleBot!")

app.run()
```


**PyBaleBot** is a modern, elegant and asynchronous framework. It enables you to easily interact with the main Bale API through a user account (custom client) or a bot
identity (bot API alternative) using Python.


### Key Features

- **Ready**: Install PyBaleBot with pip and start building your applications right away.
- **Easy**: Makes the Bale API simple and intuitive, while still allowing advanced usages.
- **Elegant**: Low-level details are abstracted and re-presented in a more convenient way.
- **Fast**: Boosted up by aiohttp, a high-performance http library written in C.
- **Async**: Fully asynchronous (also usable synchronously if wanted, for convenience).
- **Powerful**: Full access to Bale's API to execute any official client action and more.

### Installing

``` bash
pip3 install -U pybalebot
```
