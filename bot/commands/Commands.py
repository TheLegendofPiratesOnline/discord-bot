from discord.ext import commands
import builtins

class Commands:
    def __init__(self):
        # This is really disgusting but works.
        # TODO: Rewrite.

        @self.bot.command()
        async def test(*args):
            """
            command: ping
            description: simple test command.
            """

            await self.bot.say("alive")
