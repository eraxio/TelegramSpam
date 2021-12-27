from colorama import init
from colorama import Fore


class Command:
    def __init__(self, function, args, help=None):
        self.function = function
        self.help = help if help else self.function.__doc__
        self.args = args

    async def run_for_command_line(self):
        init()
        if "--help" in self.args:
            print(Fore.GREEN, self.help)
        else:
            return await self.run()

    async def run(self):
        return await self.function(*self.args)
