from nextcord.ext import commands
from cogs.Utils import update_user_level  

class ListenCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.cursor = bot.cursor

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content.startswith(self.bot.command_prefix):
            return

        user_id = message.author.id
        update_user_level(self.cursor, self.db, user_id)

        await self.bot.process_commands(message)

def setup(bot):
    bot.add_cog(ListenCommands(bot))
