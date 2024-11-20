from nextcord.ext import commands
import nextcord
import json
import os
import pyodbc

# LevelSystem Cog
class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cursor = bot.cursor

    @commands.command(name='level')
    async def level(self, ctx):
        user_id = ctx.author.id
        self.cursor.execute("SELECT message_count, level FROM users WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()

        if result:
            message_count, level = result
            embed = nextcord.Embed(
                title=f"Level Information for {ctx.author.display_name}",
                description="Here is your information:",
                color=nextcord.Color.green()
            )
            embed.add_field(name="Messages", value=f"{message_count}", inline=True)
            embed.add_field(name="Level", value=f"{level}", inline=True)
            embed.set_footer(text="© 2024 Trioinc")
        else:
            embed = nextcord.Embed(
                title="Level Information",
                description="You are not registred in the database. Please contact out support.",
                color=nextcord.Color.red()
            )
            embed.set_footer(text="© 2024 Trioinc")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(LevelSystem(bot))