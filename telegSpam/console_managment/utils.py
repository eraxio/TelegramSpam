import asyncio
from functools import wraps
from db import crud


def all_clients(wrap_func):
    @wraps(wrap_func)
    async def wrapper(*args, **kwargs):
        func_tasks = []
        for num_client, client in enumerate(crud.iter_clients()):
            func_tasks.append(wrap_func(*args,
                                        client=client,
                                        num_client=num_client,
                                        **kwargs))

        await asyncio.wait(
            [asyncio.ensure_future(func) for func in func_tasks]
        )

    return wrapper
