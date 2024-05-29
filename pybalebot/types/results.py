import json

class Results:
    def __str__(self) -> str:
        return self.jsonify(indent=2)

    def __getattr__(self, name):
        return self.find_keys(keys=name)

    def __setitem__(self, key, value):
        self.original_update[key] = value

    def __getitem__(self, key):
        return self.original_update[key]

    def __lts__(self, update: list, *args, **kwargs):
        for index, element in enumerate(update):
            if isinstance(element, list):
                update[index] = self.__lts__(update=element)
            elif isinstance(element, dict):
                update[index] = Results(update=element)
            else:
                update[index] = element
        return update

    def __init__(self, update: dict, *args, **kwargs) -> None:
        self.client = update.get('client')
        self.original_update = update

    def jsonify(self, indent=None) -> str:
        result = self.original_update
        result['original_update'] = 'dict{...}'
        return json.dumps(result, indent=indent, ensure_ascii=False, default=lambda value: str(value))

    def find_keys(self, keys, original_update=None, *args, **kwargs):
        if original_update is None:
            original_update = self.original_update

        if not isinstance(keys, list):
            keys = [keys]

        if isinstance(original_update, dict):
            for key in keys:
                try:
                    update = original_update[key]
                    if isinstance(update, dict):
                        update = Results(update=update)
                    elif isinstance(update, list):
                        update = self.__lts__(update=update)
                    return update
                except KeyError:
                    pass
            original_update = original_update.values()

        for value in original_update:
            if isinstance(value, (dict, list)):
                try:
                    return self.find_keys(keys=keys, original_update=value)
                except AttributeError:
                    return None

        return None

    @property
    def command(self):
        return self.find_keys('command')

    @property
    def to_dict(self) -> dict:
        "Return the update as dict"
        return self.original_update

    @property
    def message(self):
        return self.find_keys('message')

    @property
    def is_me(self):
        return self.author_guid == self.client.guid

    @property
    def status(self):
        return self.find_keys('status')

    @property
    def action(self):
        return 'action' in self.original_update and self.original_update.get('action')

    @property
    def is_edited(self) -> bool:
        return self.message is not None and self.message.is_edited

    @property
    def type(self):
        return self.find_keys(keys=['type', 'author_type'])

    @property
    def title(self) -> str:
        return self.find_keys('title')

    @property
    def is_forward(self) -> bool:
        message = self.message
        return message is not None and 'forwarded_from' in message.original_update

    @property
    def forward_type_from(self):
        return self.message.find_keys('type_from')

    @property
    def is_event(self) -> bool:
        return self.message is not None and self.message.type == 'Event'

    @property
    def event_data(self):
        if self.is_event is True: 
            return self.message.find_keys('event_data')

    @property
    def is_file_inline(self):
        message = self.message
        return message.type in ['FileInline', 'FileInlineCaption']

    @property
    def file_inline(self):
        return self.find_keys('file_inline')

    @property
    def music(self):
        return self.file_inline is not None and self.file_inline.type == 'Music'

    @property
    def file(self):
        return self.file_inline is not None and self.file_inline.type == 'File'

    @property
    def photo(self):
        return self.file_inline is not None and self.file_inline.type == 'Image'

    @property
    def video(self):
        return self.file_inline is not None and self.file_inline.type == 'Video'

    @property
    def voice(self):
        return self.file_inline is not None and self.file_inline.type == 'Voice'

    @property
    def contact(self):
        return self.file_inline is not None and self.file_inline.type == 'Contact'

    @property
    def location(self):
        return self.file_inline is not None and self.file_inline.type == 'Location'

    @property
    def poll(self):
        return self.file_inline is not None and self.file_inline.type == 'Poll'

    @property
    def gif(self):
        return self.file_inline is not None and self.file_inline.type == 'Gif'

    @property
    def sticker(self):
        return self.find_keys('sticker')

    @property
    def text(self) -> str:
        return self.message.text

    @property
    def message_id(self):
        return self.find_keys(keys=['message_id', 'pinned_message_id'])

    @property
    def reply_message_id(self):
        return self.message.find_keys(keys='reply_to_message_id')

    @property
    def is_group(self):
        return self.type == 'Group'

    @property
    def is_channel(self):
        return self.type == 'Channel'

    @property
    def is_private(self):
        return self.type == 'User'

    @property
    def object_guid(self):
        return self.find_keys(keys=['group_guid', 'object_guid', 'channel_guid'])

    @property
    def author_guid(self):
        return self.message.author_object_guid

    @property
    def is_text(self):
        message = self.message
        return message is not None and message.type == 'Text'