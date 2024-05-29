import pybalebot

class EditMessageText:
    async def edit_message_text(self: "pybalebot.Client", text: str, chat_id: int = None, message_id: int = None, reply_markup: dict = None):
        data = dict(
            text=text,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=reply_markup
        )
        return await self.api.execute('editMessageText', data=data)