import asyncio

from .utils import all_clients
from db import crud

from telegram_utils.teleg_group import CustomTelegramChat as TelegChat

from proxy import proxy_utils


async def test():
    """Тестовоя команда"""
    print("Тестовая команда")


async def add_clients(proxy_count_in_client=3):
    """Добавляет всех клиентов в базу данных.

    args:
        proxy_count_in_client: Сколько клинтов на 1 прокси(рекомендуем-3)

    python manage.py add_clients 3
    """
    clients = await crud.add_clients()
    proxies = await crud.add_proxies(proxies=await proxy_utils.get_proxies())
    await crud.add_proxy_to_clients(clients, proxies, proxy_count_in_client)


async def edit_clients():
    """Заполняют информацию о клиенте в базе данных.

    python manage.py edit_client
    """
    for client in crud.iter_clients():
        tg_client = await client.launch_telegram_client()
        client.user_id = tg_client.user.id
        client.username = tg_client.user.username
        client.first_name = tg_client.user.first_name
        client.last_name = tg_client.user.last_name

    crud.session_commit()


async def print_clients():
    """Выводит в консоль всех клиентов в базу данных.

    python manage.py print_clients
    """
    for db_client in crud.iter_clients():
        tg_client = await db_client.launch_telegram_client()
        print(f"Клиент: "
              f"{tg_client.user.first_name} "
              f"{tg_client.user.last_name} "
              f"{tg_client.user.username}")



@all_clients
async def parse_chat(chat_username, client_users_count=30,
                     client=None, num_client=None):
    """Парсит чат и добавляет юзеров в БД привязанных к клиентам.

    args:
        chat_username: Юзернейм чата.
        client_users_count: количество пользователяей, привязанных к клиентам.

    python manage.py parse_chat "python_academy_chat" 50
    """
    tg_client = await client.launch_telegram_client()
    chat: TelegChat = await tg_client.join_chat(chat_username)
    print(f"[{tg_client.user.first_name}]"
          f"Парсим пользователей чата {chat.channel.title}..")
    dialog = await tg_client.get_chat(chat)

    members = await dialog.parse_members()
    members_slice = members[num_client*int(client_users_count):
                            int(client_users_count)*(num_client+1)]
    await crud.add_members(db_client=client,
                           chat_username=chat.channel.username,
                           chat_members=members_slice)
    print(f"[{tg_client.user.first_name}]"
          f"Выгрузка в базу данных завершилась.")


@all_clients
async def spam_send(message_text, timeout=2, client=None, num_client=None):
    """Отправляет сообщения пользователям всеми клиентами.

    args:
        message_text: Текст сообщения.

    python manage.py parse_chat "Требуемое сообщение"
    """
    print(f"[{client.first_name}]"
          f"Начинаем отправку сообщения:\n {message_text}")
    tg_client = await client.launch_telegram_client()
    for member in client.members:
        if not member.sended:
            await tg_client.send_message(user_id=member.user_id,
                                         access_hash=member.access_hash,
                                         text=message_text)
            print(f"[{client.first_name}]"
                  f"Сообщение отправилось пользователю: {member.first_name}")
            member.is_send()
            await asyncio.sleep(int(timeout))
        else:
            print(f"[{client.first_name}]"
                  f"Сообщение ему уже было отправлено: {member.first_name}")
    print("Отправка сообщений завершена.")


async def clear_db():
    clients = await crud.get_clients()

    for client in clients:
        await crud.delete_client(client)


async def member_not_send():
    pass
