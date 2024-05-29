import pybalebot

class GetMe:
    async def get_me(self: "pybalebot.Client"):
        return await self.api.execute('getMe')