import aiohttp
import inspect
import asyncio
from .errors import RPCError
from .filters import Filter
from .types import Results, Message

class BaleAPI:
    BASE_URL = 'https://tapi.bale.ai'

    def __init__(self, client=None) -> None:
        """
        Initialize the BaleAPI instance.
        
        :param client: The client instance which contains bot_token and other configurations.
        """
        self.client = client
        self.offset = 0
        self.session = aiohttp.ClientSession(
            base_url=client.base_url or self.BASE_URL,
            connector=aiohttp.TCPConnector(),
            timeout=aiohttp.ClientTimeout(total=20)
        )

    async def close(self):
        """
        Close the aiohttp session.
        """
        await self.session.close()

    async def execute(self, name: str, data: dict = None, update: bool = False):
        """
        Execute a command on the Bale API.

        :param name: The API method name.
        :param data: The data to be sent with the request.
        :param update: Whether the request is an update.
        :return: Results object if the request is successful.
        :raises: RPCError if the request fails.
        """
        path = f'/bot{self.client.bot_token}/{name}'
        for _ in range(self.client.max_retry):
            async with self.session.post(path, json=data) as response:
                response_data = await response.json()
                if response_data.get('ok'):
                    response_data.pop('ok')
                    return Results(response_data)
                error_code = response_data.get('error_code')
                description = response_data.get('description')
                raise RPCError(description, code=error_code)

    async def process_update(self, update: Results):
        """
        Process an update from the Bale API.

        :param update: The update data.
        """
        update_data = update.message.to_dict
        update_message = Message(update_data)
        update_message.client = self.client
        for handler, filters in self.client.handlers.copy().items():
            filter_results = []
            for filter_func in filters:
                if isinstance(filter_func, Filter):
                    result = await filter_func(client=self.client, message=update_message)
                else:
                    result = await filter_func(self.client, update_message) if inspect.iscoroutinefunction(filter_func) else filter_func(self.client, update_message)
                filter_results.append(result)
            if all(filter_results):
                await handler(self.client, update_message)

    async def get_updates(self):
        """
        Continuously fetch updates from the Bale API and process them.
        """
        while True:
            try:
                updates = await self.client.get_updates(offset=self.offset)
                updates_result = updates.result

                if updates_result:
                    self.offset = updates_result[-1].update_id + 1

                for update in updates_result:
                    asyncio.create_task(self.process_update(update=update))
            except Exception as e:
                await asyncio.sleep(3)
                print('Error in getting updates from Bale:', e)
