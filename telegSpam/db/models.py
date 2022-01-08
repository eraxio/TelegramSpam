from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

import socks
import requests

import telegSpam.config

from telegSpam.telegram_utils.teleg_client import launch_telegram_client
from telegSpam.telegram_utils.teleg_client import CustomTelegramClient

from loguru import logger

Session = sessionmaker(config.engine)
session = Session()

Base = declarative_base()

proxies = Table('proxies', Base.metadata,
                Column('proxy_id', Integer, ForeignKey('proxy.id',
                                                       ondelete="CASCADE")),
                Column('client_id', Integer, ForeignKey('client.id',
                                                        ondelete="CASCADE"))
                )


class Client(Base):
    __tablename__ = "client"
    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, nullable=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

    proxies = relationship('Proxy', secondary=proxies,
                           backref="proxies", uselist=False)

    client_session = Column(String(3000))
    api_id = Column(String(100), nullable=True)
    api_hash = Column(String(100), nullable=True)

    members = relationship("Member", backref="members")

    def __init__(self, client_session,
                 api_id=12345, api_hash='0123456789abcdef0123456789abcdef',
                 user_id=None, username=None, first_name=None, last_name=None):
        self.client_session = client_session
        self.api_id = api_id
        self.api_hash = api_hash
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

    async def launch_telegram_client(self) -> CustomTelegramClient:
        client = await launch_telegram_client(client_path=self.client_session,
                                              api_id=self.api_id,
                                              api_hash=self.api_hash,
                                              proxy=self.proxies)
        if not client:
            logger.error(f"Telegram client is None")
        else:
            logger.info(f"Telegram Client "
                        f"launch in db Client<{self.id}>")
            return client

    def __repr__(self):
        return f"Client<session={self.client_session}>"


class Proxy(Base):
    __tablename__ = "proxy"
    id = Column(Integer, primary_key=True, autoincrement=True)

    proxy_type = Column(Integer)
    ip = Column(String)
    port = Column(String)
    rdns = Column(Boolean)
    login = Column(String)
    password = Column(String)

    def __init__(self, proxy_type: int, ip: str, port: str, rdns: bool = True,
                 login: str = None, password: str = None):
        if proxy_type == 1:
            self.proxy_type = socks.SOCKS4
        elif proxy_type == 2:
            self.proxy_type = socks.SOCKS5
        elif proxy_type == 3:
            self.proxy_type = socks.HTTP

        self.ip = ip
        self.port = port
        self.rdns = rdns
        self.login = login
        self.password = password

    def __repr__(self):
        return f"Proxy<ip={self.ip}, " \
               f"port={self.port}, " \
               f"login={self.login}, " \
               f"password={self.password}>"

    def get_proxy(self):
        logger.info(f"Get Proxy<{self.ip}> for Telegram Client")
        return (self.proxy_type,
                self.ip,
                int(self.port),
                True,
                self.login,
                self.password)

    def try_proxy(self):
        proxies = {
            "http": f"http://{self.login}:{self.password}@"
                    f"{self.ip}:{self.port}",
        }
        r = requests.get("http://example.com/", proxies=proxies)
        if r.status_code == 200:
            logger.info(f"Proxy<{self.id}> is success and work")
            return True
        else:
            logger.warning(f"Proxy<{self.id}> is not success and don`t work")
            return False


class Member(Base):
    __tablename__ = "member"
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("client.id", ondelete="CASCADE"))
    chat_username = Column(String)
    user_id = Column(Integer)
    access_hash = Column(Integer)
    username = Column(String(32), nullable=True)
    first_name = Column(String(1000))
    last_name = Column(String(1000), nullable=True)
    sended = Column(Boolean)

    def __init__(self, client_id, chat_username, user_id, access_hash, username,
                 first_name, last_name, sended=False):
        self.client_id = client_id
        self.chat_username = chat_username
        self.user_id = user_id
        self.access_hash = access_hash
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.sended = sended

    def __repr__(self):
        return f"<Member id={self.user_id}, " \
               f"chat_username={self.chat_username}" \
               f"access_hash={self.access_hash}, " \
               f"username={self.username}, " \
               f"first_name={self.first_name}, " \
               f"last_name={self.last_name}>"

    def is_send(self):
        member = session.query(Member).get(self.id)
        member.sended = True
        session.commit()

        logger.info(f"Member<{self.id}> was written")

    def is_not_send(self):
        member = session.query(Member).get(self.id)
        member.sended = False
        session.commit()

        logger.info(f"Member<{self.id}> was not written")


if __name__ == "__main__":
    from sqlalchemy import create_engine

    logger.info("Create tables in data base.")

    engine = create_engine('sqlite:///sqlite3.db')
    Base.metadata.create_all(engine)
