import sys

import asyncio

from console_managment.base import execute_from_command_line

if __name__ == "__main__":
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(execute_from_command_line(sys.argv))

# Ruler 80
