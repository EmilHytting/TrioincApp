import nextcord
import random
import os
import requests
from nextcord.ext import commands
from cogs.Utils import load_json_file

class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        current_dir = os.path.dirname(os.path.abspath(__file__))
        text_file_path = os.path.join(current_dir, "assets", "Text.json")
        data = load_json_file(text_file_path)  # Load data from the new Text.json
        self.fun_facts = data.get("funfacts", [])
        self.quotes = data.get("quotes", [])

    @commands.command(name='ping', help="Displays the bot's latency in milliseconds.\nExample: -ping")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        embed = nextcord.Embed(
            title="Ping",
            description=f"Trioinc's latency: **{latency}** ms",
            color=nextcord.Color.blue()
        )
        embed.set_footer(text="This message will disappear after 10 seconds. © 2024 Trioinc")
        await ctx.send(embed=embed, delete_after=10)
        await ctx.message.delete(delay=10)

    @commands.command(name='serverinfo', help="Shows information about the server.\nExample: -serverinfo")
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = nextcord.Embed(
            title=f"Guild information for {guild.name}",
            description=f"Here is the guild information for **{guild.name}**",
            color=nextcord.Color.blue(),
        )
        embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="🆔 Server ID", value=guild.id, inline=True)
        embed.add_field(name="🌍 Region", value=guild.region, inline=True)
        embed.add_field(name="👥 Members", value=guild.member_count, inline=True)
        embed.add_field(name="📅 Created", value=guild.created_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="🔒 Owner", value=guild.owner, inline=True)
        embed.add_field(name="📝 Rolecount", value=len(guild.roles), inline=True)
        embed.set_footer(text="This message will disappear after 10 seconds. © 2024 Trioinc")
        await ctx.send(embed=embed, delete_after=10)
        await ctx.message.delete(delay=10)

    @commands.command(name='userinfo', help="Shows information about a user.\nExample: -userinfo @username")
    async def userinfo(self, ctx, member: nextcord.Member = None):
        if not member: 
            member = ctx.author
        embed = nextcord.Embed(
            title=f"User Information for {member.display_name}",
            description=f"Here is the information for {member.mention}:",
            color=nextcord.Color.blue()
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="🆔 User ID", value=member.id, inline=True)
        embed.add_field(name="👤 Username", value=member.name, inline=True)
        embed.add_field(name="📅 Account Created", value=member.created_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="📅 Joined Server", value=member.joined_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="🕒 Status", value=str(member.status).capitalize(), inline=True)
        embed.add_field(name="🎮 Game", value=member.activity.name if member.activity else "None", inline=True)
        embed.add_field(name="🔒 Roles", value=", ".join([role.name for role in member.roles[1:]]), inline=False)
        embed.set_footer(text="This message will disappear after 10 seconds. © 2024 Trioinc")
        await ctx.send(embed=embed, delete_after=10)
        await ctx.message.delete(delay=10)

    @commands.command(name='translate', help="Translates a given text to the specified language.\nExample: -translate en 'Hello, how are you?'")
    async def translate(self, ctx, lang: str, *, text: str):
        try:
            translated = self.translator.translate(text, dest=lang)
            embed = nextcord.Embed(
                title=f"Oversættelse til {lang.upper()}",
                description=f"**Original text:**\n{text}\n\n**Translated:**\n{translated.text}",
                color=nextcord.Color.blue()
            )
            embed.set_footer(text="This message will disappear after 10 seconds. © 2024 Trioinc")
            await ctx.send(embed=embed, delete_after=10)
            await ctx.message.delete(delay=10)
        except Exception as e:
            error_message = f"Error: {str(e)}"
            await ctx.send(f"Something went wrong. Try again later. Error: {error_message}", delete_after=10)
            await ctx.message.delete(delay=10)
            print(f"Error i oversættelse: {error_message}") 

    @commands.command(name='funfact', help="Sends a random fun fact. Optionally specify a category.\nExample: -funfact science, -funfact animals, -funfact history")
    async def funfact(self, ctx, category: str = None):
        if category:
            category = category.lower()
            if category in self.fun_facts:
                fact = random.choice(self.fun_facts[category]) 
            else:
                await ctx.send(f"Sorry, no fun facts available for the category '{category}'. Please try another category.", delete_after=10)
                await ctx.message.delete(delay=10)
                return
        else:
            fact = random.choice(self.fun_facts)

        category_display = category.capitalize() if category else "Random"

        embed = nextcord.Embed(
            title=f"Fun Fact of the Day! 🌟",
            description=f"**Category:** {category_display}\n\n{fact}",
            color=nextcord.Color.blurple()
        )
        embed.set_footer(text="This message will disappear after 10 seconds. © 2024 Trioinc")
        
        await ctx.send(embed=embed, delete_after=10)
        await ctx.message.delete(delay=10)



    @commands.command(name='weather', help="Shows the current weather for a city.\nExample: -weather Copenhagen")
    async def weather(self, ctx, *, city: str):
        geocode_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.bot.api_key}"
        geocode_response = requests.get(geocode_url)
        geocode_data = geocode_response.json()

        if geocode_response.status_code != 200:
            await ctx.send(f"Could not find weather for {city}. Please try again.", delete_after=10)
            await ctx.message.delete(delay=10)
            return

        lat = geocode_data['coord']['lat']
        lon = geocode_data['coord']['lon']
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.bot.api_key}&units=metric"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        if weather_response.status_code == 200:
            temperature = weather_data['main']['temp']
            description = weather_data['weather'][0]['description']
            city_name = weather_data['name']
            humidity = weather_data['main']['humidity']
            wind_speed = weather_data['wind']['speed']
            
            snow = weather_data.get('snow', None)
            snow_description = f"**Snow:** {snow.get('1h', 0)} mm" if snow else None

            if 'rain' in description:
                weather_icon = "🌧️"
            elif 'clear' in description:
                weather_icon = "☀️"
            elif 'cloud' in description:
                weather_icon = "☁️"
            elif 'snow' in description:
                weather_icon = "❄️"
            else:
                weather_icon = "🌤️"

            description = description.capitalize()

            embed = nextcord.Embed(
                title=f"Weather in {city_name}   {weather_icon}",
                description=f"**Temperature:** {temperature}°C 🌡️\n"
                            f"**Condition:** {description} 🌤️\n"
                            f"**Humidity:** {humidity}% 💧\n"
                            f"**Wind Speed:** {wind_speed} m/s 🌬️\n"
                            f"{snow_description if snow_description else ''}",
                color=nextcord.Color.blue()
            )
            embed.set_footer(text="This message will disappear after 10 seconds. © 2024 Trioinc")
            await ctx.send(embed=embed, delete_after=10)
            await ctx.message.delete(delay=10)
        else:
            await ctx.send("Couldn't retrieve weather data. Please try again later.", delete_after=10)
            await ctx.message.delete(delay=10)

    @commands.command(name='quote', help="Sends an inspirational quote. Optionally specify a category.\nExample: -quote motivation, -quote life, -quote success, -quote love")
    async def quote(self, ctx, category: str = None):
        if category:
            category = category.lower()
            if category in self.quotes:
                quote = random.choice(self.quotes[category])
            else:
                await ctx.send(f"Sorry, no quotes available for the category '{category}'.", delete_after=10)
                await ctx.message.delete(delay=10)
                return
        else:
            all_quotes = [quote for category_quotes in self.quotes.values() for quote in category_quotes]
            quote = random.choice(all_quotes)

        embed = nextcord.Embed(
            title="Quote of the Day",
            description=quote,
            color=nextcord.Color.blue()
        )
        embed.set_footer(text="This message will disappear after 10 seconds. © 2024 Trioinc")
        await ctx.send(embed=embed, delete_after=10)
        await ctx.message.delete(delay=10)

def setup(bot):
    bot.add_cog(BasicCommands(bot))

