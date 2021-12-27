from .models import Member, Client, Proxy
from sqlalchemy.orm import sessionmaker

from telethon.tl.types import User

from config import engine
from config import SESSIONS_PATH

from loguru import logger

Session = sessionmaker(engine)
session = Session()


async def delete_client(client: Client):
    client = session.query(Client).get(client.id)

    session.delete(client)
    session.commit()

    logger.info(f"Delete Client<{client.id}> in db")
    return client


def session_commit():
    logger.info("Session commit")
    return session.commit()


async def add_clients():
    added_clients = []
    for session_path in SESSIONS_PATH.rglob("*.session"):
        if not session.query(Client).filter_by(
                client_session=session_path.__str__()).first():
            client = Client(
                client_session=session_path.__str__()
            )
            session.add(client)

            added_clients.append(client)

    session.commit()

    logger.info(f"Add {len(added_clients)} clients in db")
    return added_clients


def iter_clients() -> Client:
    logger.info(f"Get clients iterator")
    for client in session.query(Client):
        yield client


async def get_clients() -> list[Client]:
    logger.info("Get clients")
    return [client for client in session.query(Client)]


async def add_members(db_client: Client,
                      chat_username: str,
                      chat_members: list[User]):
    for tg_member in chat_members:
        if not session.query(Member).filter_by(user_id=tg_member.id).first():
            await add_member(tg_member, db_client, chat_username)

    session.commit()


async def add_member(tg_member: User, db_client: Client, chat_username):
    member = Member(
        user_id=tg_member.id,
        client_id=db_client.id,
        chat_username=chat_username,
        access_hash=tg_member.access_hash,
        username=tg_member.username,
        first_name=tg_member.first_name,
        last_name=tg_member.last_name,
    )
    session.add(member)

    if member not in db_client.members:
        db_client.members.append(member)

    logger.info(f"Client<{db_client.id}> add Member<{member.id}> of "
                f"Chat<{chat_username}> in db")
    return member


async def add_proxies(proxies: list[dict]):
    added_proxy = []
    for proxy_ in proxies:
        if not session.query(Proxy).filter_by(
                ip=proxy_["ip"]).first():
            db_proxy = Proxy(proxy_type=int(proxy_["proxy_type"]),
                             ip=proxy_["ip"],
                             port=int(proxy_["port"]),
                             rdns=True if proxy_["rdns"] else False,
                             login=proxy_["login"] if proxy_["login"] else None,
                             password=proxy_["password"] if proxy_["password"]
                             else None)

            # if db_proxy.try_proxy():
            session.add(db_proxy)
            added_proxy.append(db_proxy)
            # else:
            #     logger.error("Proxy error")

    session.commit()
    logger.info(f"Add {len(added_proxy)} proxies in db")
    return added_proxy


async def add_proxy_to_clients(clients: list[Client],
                               proxies: list[Proxy],
                               proxy_count_in_client: int):
    proxy_num = 1
    for client in clients:
        print(client)
        client.proxies.append(proxies[proxy_num - 1])  # индекс с 0 => 0=1-1
        if proxy_num % proxy_count_in_client == 0:
            proxy_num += 1

    session.commit()

    logger.info(f"Add {len(proxies)} proxies to {len(clients)} clients")
