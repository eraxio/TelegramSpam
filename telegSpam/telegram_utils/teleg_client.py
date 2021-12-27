import asyncio

from telethon import TelegramClient

from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import InputPeerUser, User

from telethon.errors.rpcerrorlist import PeerIdInvalidError
from telethon.errors.rpcerrorlist import PeerFloodError

from .teleg_group import CustomTelegramChat as TelegChat

from loguru import logger


class CustomTelegramClient:
    def __init__(self, client, user: User, proxy=None, client_path=None):
        self.client = client
        self.user = user
        self.client_path = client_path
        self.proxy = proxy

    async def join_chat(self, username) -> TelegChat:
        update = await self.client(JoinChannelRequest(
            channel=username
        ))
        channel = update.chats[0]

        logger.info(f"Client<{self.user.id}> join chat {username}")
        return TelegChat(client=self.client, channel=channel)

    async def get_chats(self):
        logger.info(f"Client<{self.user.id}> get his dialogs")
        return await self.client.get_dialogs()

    async def get_chat(self, channel: TelegChat):
        chats = await self.get_chats()
        for chat in chats:
            if chat.title == channel.channel.title:
                logger.info(f"Client<{self.user.id}> get chat "
                            f"{channel.channel.title}")
                return TelegChat(channel=chat, client=self.client)

        logger.error(f"Client<{self.user.id}> not found chat")

    async def __repeat_until_send(self, peerUser, text):
        while True:
            await asyncio.sleep(30)
            await self.client.send_message(peerUser, text)

            logger.info(f"Client<{self.user.id}> repeat send message "
                        f"Member<{peerUser.user_id}>")

    async def send_message(self, user_id: int, access_hash: int, text: str):
        user = InputPeerUser(user_id, int(access_hash))
        try:
            await self.client.send_message(user, text)

            logger.info(f"Client<{self.user.id}> send message "
                        f"Member<{user_id}>")
        except PeerIdInvalidError:
            logger.error(f"PeerIdInvalidError Member<{user_id}>")
        except PeerFloodError:
            logger.error(f"PeerFloodError Member<{user_id}>")
            await self.__repeat_until_send(user, text)


async def launch_telegram_client(
        client_path,
        proxy,
        api_id=12345,
        api_hash='0123456789abcdef0123456789abcdef') -> CustomTelegramClient:
    if proxy.try_proxy():
        tg_client = TelegramClient(session=client_path.__str__(),
                                   api_id=api_id,
                                   api_hash=api_hash,
                                   proxy=proxy.get_proxy())

        await tg_client.connect()

        custom_telegram_clients = CustomTelegramClient(
            client=tg_client,
            user=await tg_client.get_me(),
            client_path=client_path,
            proxy=proxy
        )

        logger.info(f"Return CustomTelegramClient<"
                    f"{custom_telegram_clients.user.first_name}>")
        return custom_telegram_clients
    else:
        logger.error(f"CustomTelegramClient is not launch, "
                     f"because proxy don`t work")
