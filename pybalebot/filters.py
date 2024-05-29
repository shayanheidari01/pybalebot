import re
import inspect
from typing import Union, List, Callable, Awaitable, Pattern
from .types import Message

COMMAND_RE = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")

class Filter:
    def __init__(self, func: Union[Callable, Awaitable]):
        """
        Initialize a Filter instance.

        :param func: The function to be used as the filter.
        """
        self.func = func

    async def __call__(self, client, message):
        """
        Call the filter function.

        :param client: The client instance.
        :param message: The message instance.
        :return: The result of the filter function.
        """
        if inspect.iscoroutinefunction(self.func):
            return await self.func(client, message)
        return self.func(client, message)

    def __and__(self, other):
        """
        Combine this filter with another using logical AND.

        :param other: The other filter.
        :return: A new combined filter.
        """
        async def combined(client, message):
            return await self(client, message) and await other(client, message)
        return Filter(combined)

    def __or__(self, other):
        """
        Combine this filter with another using logical OR.

        :param other: The other filter.
        :return: A new combined filter.
        """
        async def combined(client, message):
            return await self(client, message) or await other(client, message)
        return Filter(combined)

    def __invert__(self):
        """
        Invert this filter.

        :return: A new inverted filter.
        """
        async def inverted(client, message):
            return not await self(client, message)
        return Filter(inverted)

    def __eq__(self, other) -> bool:
        """
        Check if this filter is equal to another.

        :param other: The other filter or string.
        :return: A new equality check filter.
        """
        async def equaled(client, message):
            return await self(client, message) == (other if isinstance(other, str) else await other(client, message))
        return Filter(equaled)
    
    def __ne__(self, other) -> bool:
        """
        Check if this filter is not equal to another.

        :param other: The other filter or string.
        :return: A new inequality check filter.
        """
        async def unequal(client, message):
            return await self(client, message) != (await other(client, message) if inspect.iscoroutinefunction(other) else other)
        return Filter(unequal)

class Filters:
    @property
    def text(self):
        """
        Check if the message contains text.

        :return: A text filter.
        """
        async def func(client, message):
            return message.text
        return Filter(func)

    @property
    def forward(self):
        """
        Check if the message is a forwarded message.

        :return: A forward filter.
        """
        async def func(client, message):
            return message.find_keys(['forward_from', 'forward_from_chat'])
        return Filter(func)
    
    @property
    def animation(self):
        """
        Check if the message contains an animation.

        :return: An animation filter.
        """
        async def func(client, message):
            return message.animation is not None
        return Filter(func)

    @property
    def audio(self):
        """
        Check if the message contains audio.

        :return: An audio filter.
        """
        async def func(client, message):
            return message.audio is not None
        return Filter(func)

    @property
    def document(self):
        """
        Check if the message contains a document.

        :return: A document filter.
        """
        async def func(client, message):
            return message.document is not None
        return Filter(func)
    
    @property
    def photo(self):
        """
        Check if the message contains a photo.

        :return: A photo filter.
        """
        async def func(client, message):
            return message.document is not None and message.document.mime_type.split('/')[0] == 'image'
        return Filter(func)
    
    @property
    def sticker(self):
        """
        Check if the message contains a sticker.

        :return: A sticker filter.
        """
        async def func(client, message):
            return message.sticker is not None
        return Filter(func)
    
    @property
    def video(self):
        """
        Check if the message contains a video.

        :return: A video filter.
        """
        async def func(client, message):
            return message.video is not None
        return Filter(func)
    
    @property
    def voice(self):
        """
        Check if the message contains a voice message.

        :return: A voice filter.
        """
        async def func(client, message):
            return message.document is not None and message.document.mime_type.split('/')[0] == 'audio'
        return Filter(func)
    
    @property
    def contact(self):
        """
        Check if the message contains a contact.

        :return: A contact filter.
        """
        async def func(client, message):
            return message.contact is not None
        return Filter(func)
    
    @property
    def location(self):
        """
        Check if the message contains a location.

        :return: A location filter.
        """
        async def func(client, message):
            return message.location is not None
        return Filter(func)

    @property
    def new_chat_members(self):
        """
        Check if the message indicates new chat members.

        :return: A new chat members filter.
        """
        async def func(client, message):
            return bool(message.new_chat_members)
        return Filter(func)

    @property
    def left_chat_member(self):
        """
        Check if the message indicates a left chat member.

        :return: A left chat member filter.
        """
        async def func(client, message):
            return bool(message.left_chat_member)
        return Filter(func)

    @property
    def invoice(self):
        """
        Check if the message contains an invoice.

        :return: An invoice filter.
        """
        async def func(client, message):
            return bool(message.invoice)
        return Filter(func)

    @property
    def bot(self):
        """
        Check if the message is from a bot.

        :return: A bot filter.
        """
        async def func(client, message):
            return message['from']['is_bot']
        return Filter(func)

    @property
    def private(self):
        """
        Check if the message is from a private chat.

        :return: A private chat filter.
        """
        async def func(client, message):
            return message.chat.type == 'private'
        return Filter(func)

    @property
    def group(self):
        """
        Check if the message is from a group chat.

        :return: A group chat filter.
        """
        async def func(client, message):
            return message.chat.type == 'group'
        return Filter(func)

    @property
    def channel(self):
        """
        Check if the message is from a channel.

        :return: A channel filter.
        """
        async def func(client, message):
            return message.chat.type == 'channel'
        return Filter(func)

    @property
    def reply(self):
        """
        Check if the message is a reply to another message.

        :return: A reply filter.
        """
        async def func(client, message):
            return isinstance(message.reply_to_message, dict)
        return Filter(func)

    def command(self, commands: Union[str, List[str]], prefixes: Union[str, List[str]] = "/", case_sensitive: bool = False):
        """
        Check if the message contains a command.

        :param commands: The commands to check.
        :param prefixes: The prefixes to check.
        :param case_sensitive: Whether the command check should be case sensitive.
        :return: A command filter.
        """
        if isinstance(commands, str):
            commands = [commands]
        if isinstance(prefixes, str):
            prefixes = [prefixes]

        commands = set(c if case_sensitive else c.lower() for c in commands)
        prefixes = set(prefixes)

        async def func(client, message):
            username = client.me.username or ""
            text = message.text or message.caption
            message['command'] = None

            if not text:
                return False

            for prefix in prefixes:
                if not text.startswith(prefix):
                    continue

                without_prefix = text[len(prefix):]

                for cmd in commands:
                    if not re.match(rf"^(?:{cmd}(?:@?{username})?)(?:\s|$)", without_prefix,
                                    flags=re.IGNORECASE if not case_sensitive else 0):
                        continue

                    without_command = re.sub(rf"{cmd}(?:@?{username})?\s?", "", without_prefix, count=1,
                                             flags=re.IGNORECASE if not case_sensitive else 0)

                    message['command'] = [cmd] + [
                        re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                        for m in COMMAND_RE.finditer(without_command)
                    ]

                    return True

            return False

        return Filter(func)
    
    def regex(self, pattern: Pattern, flags: int = 0):
        """
        Check if the message matches a regex pattern.

        :param pattern: The regex pattern to match.
        :param flags: The regex flags to use.
        :return: A regex filter.
        """
        compiled_pattern = re.compile(pattern, flags)
        
        async def func(client, message: Message) -> bool:
            if message.text is None:
                return False
            message['pattern_match'] = compiled_pattern.match(message.text)
            return bool(message['pattern_match'])
        
        return Filter(func)

    def chat(self, chats: Union[str, int, List[Union[str, int]]]):
        """
        Check if the message is from a specific chat or chats.

        :param chats: The chat or list of chats to check.
        :return: A chat filter.
        """
        chat_ids = chats if isinstance(chats, list) else [chats]
        
        async def func(client, message: Message) -> bool:
            return message.chat.id in chat_ids
        
        return Filter(func)

filters = Filters()
