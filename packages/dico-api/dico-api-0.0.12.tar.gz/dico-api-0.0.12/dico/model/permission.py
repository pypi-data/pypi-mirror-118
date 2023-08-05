import typing

from .snowflake import Snowflake
from ..base.model import DiscordObjectBase, FlagBase


class PermissionFlags(FlagBase):
    CREATE_INSTANT_INVITE = 0x0000000001
    KICK_MEMBERS = 0x0000000002
    BAN_MEMBERS = 0x0000000004
    ADMINISTRATOR = 0x0000000008
    MANAGE_CHANNELS = 0x0000000010
    MANAGE_GUILD = 0x0000000020
    ADD_REACTIONS = 0x0000000040
    VIEW_AUDIT_LOG = 0x0000000080
    PRIORITY_SPEAKER = 0x0000000100
    STREAM = 0x0000000200
    VIEW_CHANNEL = 0x0000000400
    SEND_MESSAGES = 0x0000000800
    SEND_TTS_MESSAGES = 0x0000001000
    MANAGE_MESSAGES = 0x0000002000
    EMBED_LINKS = 0x0000004000
    ATTACH_FILES = 0x0000008000
    READ_MESSAGE_HISTORY = 0x0000010000
    MENTION_EVERYONE = 0x0000020000
    USE_EXTERNAL_EMOJIS = 0x0000040000
    VIEW_GUILD_INSIGHTS = 0x0000080000
    CONNECT = 0x0000100000
    SPEAK = 0x0000200000
    MUTE_MEMBERS = 0x0000400000
    DEAFEN_MEMBERS = 0x0000800000
    MOVE_MEMBERS = 0x0001000000
    USE_VAD = 0x0002000000
    CHANGE_NICKNAME = 0x0004000000
    MANAGE_NICKNAMES = 0x0008000000
    MANAGE_ROLES = 0x0010000000
    MANAGE_WEBHOOKS = 0x0020000000
    MANAGE_EMOJIS = 0x0040000000
    USE_SLASH_COMMANDS = 0x0080000000
    REQUEST_TO_SPEAK = 0x0100000000
    MANAGE_THREADS = 0x0400000000
    USE_PUBLIC_THREADS = 0x0800000000
    USE_PRIVATE_THREADS = 0x1000000000
    USE_EXTERNAL_STICKERS = 0x2000000000


class Role(DiscordObjectBase):
    TYPING = typing.Union[int, str, Snowflake, "Role"]

    def __init__(self, client, resp, *, guild_id=None):
        super().__init__(client, resp)
        self.guild_id = Snowflake.optional(guild_id)  # This isn't actually in payload, but role is always created at the guild, so why not?
        self._cache_type = "role"
        self.name = resp["name"]
        self.color = resp["color"]
        self.hoist = resp["hoist"]
        self.position = resp["position"]
        self.permissions = PermissionFlags.from_value(int(resp["permissions"]))
        self.managed = resp["managed"]
        self.mentionable = resp["mentionable"]
        self.tags = RoleTags.optional(resp.get("tags"))

    @property
    def guild(self):
        if self.client.has_cache:
            return self.client.get(self.guild_id, "guild")

    def to_position_param(self, position: int = None):
        body = {"id": str(self.id)}
        if position is not None:
            body["position"] = position
        return body


class RoleTags:
    def __init__(self, resp):
        self.bot_id = Snowflake.optional(resp.get("bot_id"))
        self.integration_id = Snowflake.optional(resp.get("integration_id"))
        self.premium_subscriber = resp.get("premium_subscriber")

    @classmethod
    def optional(cls, resp):
        if resp:
            return cls(resp)
