from . import manage_commands
from .command import Command


async def get_command(command_name, *args):
    commands = {
        "test": Command(function=manage_commands.test,
                        args=args),
        "add_clients": Command(function=manage_commands.add_clients,
                               args=args),
        "edit_clients": Command(function=manage_commands.edit_clients,
                                args=args),
        "print_clients": Command(function=manage_commands.print_clients,
                                 args=args),
        "parse_chat": Command(function=manage_commands.parse_chat,
                              args=args),
        "spam_send": Command(function=manage_commands.spam_send,
                             args=args),
        "clear_db": Command(function=manage_commands.clear_db,
                            args=args),
        "member_not_send": Command(function=manage_commands.member_not_send,
                                   args=args),
    }

    return commands[command_name]


async def execute_from_command_line(argv):
    command_name = argv[1]
    args = argv[2:]
    command = await get_command(command_name, *args)

    await command.run_for_command_line()
