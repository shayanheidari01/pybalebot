import pybalebot

class GetUpdates:
    async def get_updates(
            self: "pybalebot.Client",
            offset: int = -1,
            limit: int = 1
    ):
        params = dict(offset=offset, limit=limit)
        return await self.api.execute('getUpdates', params, update=True)