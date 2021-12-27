from loguru import logger
from telethon import TelegramClient


class CustomTelegramChat:
    def __init__(self, client: TelegramClient, channel):
        self.client = client
        self.channel = channel

    async def parse_members(self):
        participants = await self.client.get_participants(
            self.channel,
            aggressive=True
        )
        user = await self.client.get_me()
        logger.info(f"Client<{user.id}> get {len(participants)} "
                    f"participants in Chat<{self.channel.title}>")
        return participants
