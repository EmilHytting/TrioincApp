import nextcord
from nextcord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help(self, ctx):
        embed = nextcord.Embed(
            title="Trioinc - Commands",
            description="Here is a list of the available commands",
            color=nextcord.Color.blue()
        )
        embed.add_field(name="📋 General Commands", value="`-ping`, `-serverinfo`, `-userinfo`, `-translate`, `-weather`", inline=False)
        embed.add_field(name="🛠️ Administrative Commands", value="`-ban`, `-kick`, `-clear`", inline=False)
        embed.add_field(name="🔒 Fun Commands", value="`-funfact`, `-quote`", inline=False)
        embed.add_field(name="🙋‍♂️ Further help", value="`-commandhelp <commandname>`", inline=False)
        embed.set_footer(text="This message will disappear after 20 seconds. © 2024 Trioinc")
        await ctx.send(embed=embed, delete_after=20)
        await ctx.message.delete(delay=20)

    @commands.command(name='commandhelp')
    async def detailed_help(self, ctx, command_name: str = None):
        if command_name is None:
            await self.helo(ctx)
        else:
            command = self.bot.get_command(command_name)
            if command: 
                embed = nextcord.Embed(
                    title=f"{command_name.capitalize()} Command",
                    description=command.help.split("\nExample:")[0].strip() if "Example:" in command.help else command.help,
                    color=nextcord.Color.blue()
                )
                example = command.help.split("Example:")[1].strip() if "Example:" in command.help else "No example available."
                embed.add_field(name="**Example:**", value=example, inline=False)
                embed.set_footer(text="This message will disappear after 20 seconds. © 2024 Trioinc")
                await ctx.send(embed=embed, delete_after=20)
                await ctx.message.delete(delay=20)
            else:
                await ctx.send("This command doesn't exist.", delete_after=20)
                await ctx.message.delete(delay=20)

def setup(bot):
    bot.add_cog(HelpCommand(bot))
