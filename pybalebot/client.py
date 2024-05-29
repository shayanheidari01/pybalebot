import asyncio
from .api import BaleAPI
from .methods import Methods

class Client(Methods):
    def __init__(self, name: str, max_retry: int = 3, bot_token: str = None, base_url: str = None) -> None:
        """
        Initialize the Client instance.

        :param name: The name of the bot.
        :param bot_token: The bot token for authentication.
        :param base_url: The base URL for the Bale API.
        """
        super().__init__()
        self.bot_token = bot_token
        self.base_url = base_url
        self.max_retry = int(max_retry)
        self.name = name
        self.handlers = {}
        self.api = None

    async def start(self):
        """
        Start the client by connecting to the Bale API.
        """
        if self.api is None:
            await self.connect()

    async def connect(self):
        """
        Connect to the Bale API and retrieve bot information.
        """
        if self.bot_token is None:
            self.bot_token = input('Please enter your bot token: ')

        self.api = BaleAPI(client=self)
        self.me = await self.get_me()
        print(f'connect to  the Bale API with {self.me.username} bot\n')

    async def stop(self):
        """
        Stop the client by closing the Bale API session.
        """
        await self.api.close()

    def run(self):
        """
        Run the client to start receiving updates.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.start())
        loop.run_until_complete(self.api.get_updates())

    def on_message(self, *filters):
        """
        Decorator to register a message handler with optional filters.

        :param filters: Filters to apply to the handler.
        :return: The decorator function.
        """
        def decorator(func):
            self.handlers[func] = filters
            return func
        return decorator
