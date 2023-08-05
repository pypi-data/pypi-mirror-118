"""
Client model for krema.
"""

from dataclasses import dataclass
from typing import Union

from unikorn import kollektor
from ..utils import dict_to_query, image_to_data_uri


class Client:
    """Base class for client.

    Args:
        intents (int): Intents for your bot. Do not add any intent if you are using for self-bot.
        message_limit (int): Message cache limit for krema (default is 200). 
        channel_limit (int): Channel cache limit for krema (default is None). 
        guild_limit (int): Guild cache limit for krema (default is None). 

    Attributes:
        token (str): Bot token for http request.
        events (list): List of events for client.
        user (User): Client user.
        messages (kollektor.Kollektor): Message cache.
        guilds (kollektor.Kollektor): Guild cache.
        channels (kollektor.Kollektor): Channel cache.
        connection (Gateway): Client gateway.
        connection (HTTP): Client http class.
    """

    def __init__(self, intents: int = 0, message_limit: int = 200, channel_limit: int = None,
                 guild_limit: int = None) -> None:
        from .user import User

        self.intents: int = intents

        self.token: str = ""
        self.events: list = []
        self.user: Union[User, None] = None

        self.messages: kollektor.Kollektor = kollektor.Kollektor(
            limit=message_limit, items=())
        self.guilds: kollektor.Kollektor = kollektor.Kollektor(
            limit=guild_limit, items=())
        self.channels: kollektor.Kollektor = kollektor.Kollektor(
            limit=channel_limit, items=())

        self.connection = None
        self.http = None

        self.__add_cache_events()
        pass

    @property
    def formatted_token(self) -> str:
        """Returns formatted version of the token.

        Returns:
            str: Formatted version of the token.
        """

        if self.token.startswith("Bot "):
            return self.token.split(" ")[1]
        else:
            return self.token

    def event(self, event_name: str = None):
        """Event decorator for handle gateway events.

        Args:
            event_name (str, optional): Event name in lowercase. Example MESSAGE_CREATE is message_create for krema. If you don't add this argument, It will get the name from function name.
        """

        def decorator(fn):
            def wrapper():
                self.events.append(
                    (event_name or fn.__name__, fn)
                )

                return self.events

            return wrapper()

        return decorator

    async def check_token(self):
        """Check token status for client.

        Returns:
            None: Client token works.
        """

        from .user import User
        result = await self.http.request("GET", "/users/@me")
        self.user = User(self, result)

    def start(self, token: str, bot: bool = True):
        """Start the client.

        Args:
            token (str): Token for your bot / self-bot.
            bot (bool, optional): If you are using self-bot, make argument false.
        """

        from ..gateway import Gateway
        from ..http import HTTP

        self.token = f"Bot {token}" if bot else token

        self.connection = Gateway(self)
        self.http = HTTP(self)

        self.connection._event_loop.run_until_complete(self.check_token())
        self.connection._event_loop.run_until_complete(
            self.connection.start_connection())

    # Handler for Cache Events.
    def __add_cache_events(self):
        # Message Add Handler
        async def _message_create(message_packet):
            self.messages.append(message_packet)

        # Message Update Handler
        async def _message_update(message_packet):
            for index, message in enumerate(self.messages.items):
                if message.id == message_packet.id:
                    self.messages.update(index, message_packet)
                    break

        # Message Delete Handler
        async def _message_delete(packet):
            message_id = packet.get("id")

            if message_id is None:
                return
            else:
                message_id = int(message_id)
                self.messages.items = tuple(
                    i for i in self.messages.items if i.id != message_id)

        # Message Bulk Delete Handler
        async def _message_delete_bulk(packet):
            message_ids = packet.get("ids")

            if message_ids is None:
                return
            else:
                message_ids = tuple(int(i) for i in message_ids)
                self.messages.items = tuple(
                    i for i in self.messages.items if i.id not in message_ids)

        # Guild Create Handler
        async def _guild_create(guild):
            self.guilds.append(guild)

            # Add Guild Channels
            if guild.channels is not None:
                self.channels.append(*guild.channels)

        # Guild Update Handler
        async def _guild_update(guild_packet):
            for index, guild in enumerate(self.guilds.items):
                if guild.id == guild_packet.id:
                    self.guilds.update(index, guild_packet)
                    break

        # Guild Delete Handler
        async def _guild_delete(packet):
            guild_id = packet.get("id")

            if guild_id is None:
                return
            else:
                guild_id = int(guild_id)
                self.guilds.items = tuple(
                    i for i in self.guilds.items if i.id != guild_id)

        # Channel Create Handler
        async def _channel_create(channel):
            self.channels.append(channel)

        # Channel Update Handler
        async def _channel_update(channel_packet):
            for index, channel in enumerate(self.channels.items):
                if channel.id == channel_packet.id:
                    self.channels.update(index, channel_packet)
                    break

        # Channel Delete Handler
        async def _channel_delete(channel_packet):
            channel_id = hasattr(channel_packet, "id")

            if channel_id is None:
                return
            else:
                self.channels.items = tuple(
                    i for i in self.channels.items if i.id != channel_packet.id)

        # Thread Create Handler
        async def _thread_create(channel):
            self.channels.append(channel)

        # Thread Update Handler
        async def _thread_update(channel_packet):
            for index, channel in enumerate(self.channels.items):
                if channel.id == channel_packet.id:
                    self.channels.update(index, channel_packet)
                    break

        # Thread Delete Handler
        async def _thread_delete(channel_packet):
            channel_id = channel_packet.get("id")

            if channel_id is None:
                return
            else:
                channel_id = int(channel_id)
                self.channels.items = tuple(
                    i for i in self.channels.items if i.id != channel_id)

        local = locals()

        # Load Events
        self.events.extend(
            (i[1:], local[i]) for i in local if i.startswith("_")
        )

    # Cache Functions
    # ==================

    def get_guild(self, guild_id: int):
        """Get Guild from Cache by ID.

        Args:
            guild_id (int): Guild ID.

        Returns:
            Guild: Found Guild object.
            None: Guild is not Found.
        """

        result = self.guilds.find(lambda g: g.id == guild_id)

        if result != kollektor.Nothing:
            return result
        else:
            return None

    def get_channel(self, channel_id: int):
        """Get Channel from Cache by ID.

        Args:
            channel_id (int): Channel ID.

        Returns:
            Channel: Found Channel object.
            None: Channel is not Found.
        """

        result = self.channels.find(lambda c: c.id == channel_id)

        if result != kollektor.Nothing:
            return result
        else:
            return None

    def get_message(self, message_id: int):
        """Get Message from Cache by ID.

        Args:
            message_id (int): Message ID.

        Returns:
            Message: Found Message object.
            None: Message is not Found.
        """

        result = self.messages.find(lambda m: m.id == message_id)

        if result != kollektor.Nothing:
            return result
        else:
            return None

    def get_thread(self, thread_id: int, list_thread_result: dict):
        """Get Thread-Channel with Thread ID.

        Args:
            thread_id (int): Thread-Channel ID.
            list_thread_result (dict): The result from `<Channel>.list_...` functions.

        Returns:
            Channel: Found Thread-Channel object.
            None: Thread-Channel is not Found.

        Examples:
            >>> channel = client.get_channel(123)
            >>> thread_list = await channel.list_threads()
            >>> client.get_thread(456, thread_list)
            Channel()
        """

        for thread in list_thread_result["threads"]:
            if thread_id == thread.id:
                return thread

        return None

    async def bulk_delete(self, channel_id: int, messages: list):
        """Pure bulk-delete function.

        Args:
            channel_id (int): Channel ID.
            messages (list): List of message IDs.

        Returns:
            True: Messages are deleted successfully.
        """

        await self.http.request("POST", f"/channels/{channel_id}/messages/bulk-delete", json={
            "messages": messages
        })
        return True

    # Gateway Functions
    # ==================

    async def update_presence(self, packet: dict):
        """Update client-user presence.

        Args:
            packet (dict): https://discord.com/developers/docs/topics/gateway#update-presence-gateway-presence-update-structure
        """

        await self.connection.websocket.send_json({
            "op": 3,
            "d": packet
        })

    # Endpoint Functions
    # ==================

    async def fetch_channel(self, id: int):
        """Fetch a Channel by ID.

        Args:
            id (int): Channel ID.

        Returns:
            Channel: Found channel.
        """

        from .channel import Channel

        result = await self.http.request("GET", f"/channels/{id}")
        return Channel(self, result)

    async def fetch_user(self, id: int = None):
        """Fetch an User by ID.

        Args:
            id (int, optional): User ID, if not added it will fetch client user (@me).

        Returns:
            User: Found user.
        """

        from .user import User

        result = await self.http.request("GET", f"/users/{id if id is not None else '@me'}")

        return User(self, result)

    async def create_guild(self, **kwargs):
        """Create a Guild with API params.

        Args:
            **kwargs: https://discord.com/developers/docs/resources/guild#create-guild-json-params.

        Returns:
            Guild: Created guild object.
        """

        from .guild import Guild

        result = await self.http.request("POST", f"/guilds", json=kwargs)
        return Guild(self, result)

    async def fetch_guild(self, guild_id: int, with_count: bool = False):
        """Fetch a Guild by ID.

        Args:
            guild_id (int): Guild ID.
            with_count (bool, optional): if True, will return approximate member and presence counts for the guild. (default False)

        Returns:
            Guild: Found guild object.
        """

        from .guild import Guild

        result = await self.http.request("GET", f"/guilds/{guild_id}?with_count={with_count}")
        return Guild(self, result)

    async def edit(self, username: str, path: str):
        """Edit client user.

        Args:
            username (str): New username.
            path (str): Image / Gif path.

        Returns:
            User: Updated user.
        """

        from .user import User

        result = await self.http.request("PATCH", "/users/@me", json={
            "username": username,
            "avatar": image_to_data_uri(path)
        })
        return User(self, result)

    async def edit_banner_color(self, color: int):
        """Change banned color.

        Args:
            color (int): New Banner Color.

        Returns:
            User: Updated user.
        """

        from .user import User

        result = await self.http.request("PATCH", "/users/@me", json={
            "accent_color": color
        })
        return User(self, result)

    async def edit_nickname(self, guild_id: int, nick: str):
        """Edit Client User nickname from Guild.

        Args:
            guild_id (int): Guild ID.
            nick (str): New nickname for Client User.

        Returns:
            True: Nickname updated successfully.
        """

        await self.http.request("PATCH", f"/guilds/{guild_id}/members/@me/nick", json={
            "nick": nick
        })
        return True

    async def fetch_invite(self, invite_code: str, **kwargs):
        """Fetch Invite by Code.

        Args:
            invite_code (str): Invite Code.
            **kwargs: https://discord.com/developers/docs/resources/invite#get-invite-query-string-params

        Returns:
            Invite: Found invite object.
        """

        from .invite import Invite

        result = await self.http.request("GET", f"/invites/{invite_code}{dict_to_query(kwargs)}")
        return Invite(self, result)

    async def delete_invite(self, invite_code: str):
        """Delete Invite by Code.

        Args:
            invite_code (str): Invite Code.

        Returns:
            Invite: Found invite object.
        """

        from .invite import Invite

        result = await self.http.request("DELETE", f"/invites/{invite_code}")
        return Invite(self, result)

    async def fetch_webhook(self, webhook_id: int):
        """Fetch Webhook by ID.

        Returns:
            Webhook: Found Webhook object.
        """

        from .webhook import Webhook

        result = await self.http.request("GET", f"/webhooks/{webhook_id}")
        return Webhook(self, result)

    async def fetch_sticker(self, sticker_id: int):
        """Fetch Sticker by ID.

        Args:
            sticker_id (int): Sticker ID.

        Returns:
            Sticker: Found Sticker object.
        """

        from .sticker import Sticker

        result = await self.http.request("GET", f"/stickers/{sticker_id}")
        return Sticker(self, result)

    # async def create_global_slash_command(self, **kwargs):
    #     """Create a global slash command.

    #     Args:
    #         params (dict): Slash command parameters.

    #     Returns:
    #         True: Command added successfully.
    #     """

    #     result = await self.http.request("POST", f"/applications/{self.user.id}/commands", json=kwargs)
    #     return True

    async def fetch_application_commands(self):
        """Fetch global application commands.

        Returns:
            list: List of ApplicationCommand objects.
        """

        result = await self.http.request("GET", f"/applications/{self.user.id}/commands")
        return [ApplicationCommand(self, i) for i in result]

    async def fetch_application_command(self, command_id: int):
        """Fetch global application command by ID.

        Args:
            command_id (int): Command ID.

        Returns:
            ApplicationCommand: Found Command object.
        """

        result = await self.http.request("GET", f"/applications/{self.user.id}/commands/{command_id}")
        return ApplicationCommand(self, result)


@dataclass
class Interaction:
    """Interaction class.

    Args:
        client (Client): Krema client.
        data (dict): Sent packet from websocket.

    Attributes:
        client (Client): Krema client.
        Other things are same with https://discord.com/developers/docs/interactions/slash-commands#interaction-object-interaction-structure.
    """

    def __init__(self, client, data: dict) -> None:
        from .user import Member, User
        from .message import Message

        self.client = client

        self.id: int = int(data.get("id"))
        self.application_id: int = int(data.get("application_id"))
        self.type: int = data.get("type")
        self.data: Union[dict, None] = data.get("data")
        self.guild_id: Union[int, None] = int(
            data.get("guild_id")) if data.get("guild_id") is not None else None
        self.channel_id: Union[int, None] = int(
            data.get("channel_id")) if data.get("channel_id") is not None else None
        self.member: Union[Member, None] = Member(self.client, data.get(
            "member")) if data.get("member") is not None else None
        self.user: Union[User, None] = User(self.client, data.get(
            "user")) if data.get("user") is not None else None
        self.token: str = data.get("token")
        self.version: int = data.get("version")
        self.message: Union[Message, None] = Message(self.client, data.get(
            "message")) if data.get("message") is not None else None

    async def reply(self, type: int, **kwargs):
        """Reply to the interaction (must be used for finish the interaction.).

        Args:
            type (int): https://discord.com/developers/docs/interactions/slash-commands#interaction-response-object-interaction-callback-type
            **kwargs: https://discord.com/developers/docs/interactions/slash-commands#interaction-response-object-interaction-application-command-callback-data-structure

        Returns:
            True: Response sent successfully.
        """

        await self.client.http.request("POST", f"/interactions/{self.id}/{self.token}/callback", json={
            "type": type,
            "data": kwargs
        })
        return


@dataclass
class ApplicationCommand:
    """Application command class.

    Args:
        client (Client): Krema client.
        data (dict): Sent packet from websocket.

    Attributes:
        client (Client): Krema client.
        id (int): Command ID.
        application_id (int): Application ID.
        name (str): Command name.
        description (str): Command description.
        options (list, None): Command option(s).
        default_permission (bool, None): Whether the command is enabled by default when the app is added to a guild.
    """

    def __init__(self, client, data: dict) -> None:
        self.client = client

        self.id: int = int(data.get("id"))
        self.application_id: int = int(data.get("application_id"))
        self.guild_id: Union[int, None] = int(
            data.get("guild_id")) if data.get("guild_id") is not None else None
        self.name: str = data.get("name")
        self.description: str = data.get("description")
        self.options: Union[list, None] = data.get("options")
        self.default_permission: Union[bool,
                                       None] = data.get("default_permission")

    async def delete(self):
        """Delete application command.

        Returns:
            True: Command deleted successfully.
        """

        await self.client.http.request("DELETE", f"/applications/{self.application_id}/{f'guilds/{self.guild_id}/' if self.guild_id is not None else ''}commands/{self.id}")
        return True

    async def edit(self, **kwargs):
        """Edit application command.

        Args:
            **kwargs: https://discord.com/developers/docs/interactions/slash-commands#edit-guild-application-command-json-params

        Returns:
            ApplicationCommand: Updated command application object.
        """

        result = await self.client.http.request("PATCH", f"/applications/{self.application_id}/{f'guilds/{self.guild_id}/' if self.guild_id is not None else ''}commands/{self.id}", json=kwargs)
        return ApplicationCommand(self.client, result)
