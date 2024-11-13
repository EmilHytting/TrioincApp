import nextcord
import json
import os
import pyodbc
from nextcord.ext import commands
from cogs.LevelSystem import setup  # Importer setup-funktionen

# Load Bot Configuration
with open("Config/Config.json", "r") as config_file:
    config = json.load(config_file)

# Opret forbindelse til SQL Server
db = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=' + config['SQLSERVER_HOST'] + ';'
    'DATABASE=' + config['SQLSERVER_DATABASE'] + ';'
    'UID=' + config['SQLSERVER_USER'] + ';'
    'PWD=' + config['SQLSERVER_PASSWORD']
)
cursor = db.cursor()

# Bot Token
TOKEN = config['TOKEN']

# Setup Intents and Bot Prefix
intents = nextcord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="-", intents=intents)

# Gem db og cursor som attributter på botten
bot.db = db
bot.cursor = cursor

# Commands Handler
for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and filename != "Utils.py":  # Undgå Utils.py
        try:
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'Successfully loaded command: {filename[:-3]}')
        except Exception as e:
            print(f'Failed to load the command {filename[:-3]}: {e}')

# OnReady Event: Confirms bot is online and displays bot info
@bot.event
async def on_ready():
    print(f'Bot is online and logged in as {bot.user}')

# Run the Bot with the Token
bot.run(TOKEN)
