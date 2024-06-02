from pybalebot import Client, filters
from pybalebot.types import Message

BOT_TOKEN = 'your-bot-token'
GROUPS = [4465242698]

# Make PybaleBot Client
app = Client('anti-ads-bot', bot_token=BOT_TOKEN)

LINK_RE = r"(https?://[^\s]+)|(www\.[^\s]+)|([^\s]+\.(com|net|org|info|biz|ru|me|io|ir))"
USERNAME_RE = r"@\w{5,32}"

@app.on_message(filters.regex(LINK_RE), filters.chat(GROUPS))
async def has_link(client: Client, message: Message):
    if not (await message.get_member()).result.status in ['creator', 'administrator']:
        await message.delete()
        await message.reply(f"کاربر {message.find_keys('from').first_name} یک نام کاربری ارسال کرد و حذف شد\n• قدرت گرفته از [PybaleBot](https://github.com/shayanheidari01/pybalebot)")

@app.on_message(filters.regex(USERNAME_RE), filters.chat(GROUPS))
async def has_link(client: Client, message: Message):
    if not (await message.get_member()).result.status in ['creator', 'administrator']:
        await message.delete()
        await message.reply(f"کاربر {message.find_keys('from').first_name} یک لینک ارسال کرد و حذف شد\n• قدرت گرفته از [PybaleBot](https://github.com/shayanheidari01/pybalebot)")

@app.on_message(filters.forward, filters.chat(GROUPS))
async def forward_messages(client: Client, message: Message):
    if not (await message.get_member()).result.status in ['creator', 'administrator']:
        await message.delete()
        await message.reply(f"کاربر {message.find_keys('from').first_name} یک فوروارد ارسال کرد و حذف شد\n• قدرت گرفته از [PybaleBot](https://github.com/shayanheidari01/pybalebot)")

app.run()
