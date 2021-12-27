import pandas
from pathlib import Path

import config


async def iter_proxies(proxies_file: Path = config.PROXIES_CSV_FILE):
    pd_proxies = pandas.read_csv(proxies_file)

    for num in range(len(pd_proxies)):
        yield pd_proxies.iloc()[num]


async def get_proxies(proxies_file: Path = config.PROXIES_CSV_FILE):
    return [proxy async for proxy in iter_proxies(proxies_file)]
