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
                description="Her er dine oplysninger:",
                color=nextcord.Color.green()
            )
            embed.add_field(name="Beskeder", value=f"{message_count}", inline=True)
            embed.add_field(name="Niveau", value=f"{level}", inline=True)
            embed.set_footer(text="Trioinc Bot")
        else:
            embed = nextcord.Embed(
                title="Level Information",
                description="Du er endnu ikke registreret i databasen.",
                color=nextcord.Color.red()
            )
            embed.set_footer(text="Trioinc Bot")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(LevelSystem(bot))