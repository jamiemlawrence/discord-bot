import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

# load and extract bot token and channel id from env file
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

bot = commands.Bot(command_prefix = '!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Hello! Im the best bot')
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello! Best bot is ready")

bot.run(BOT_TOKEN)
