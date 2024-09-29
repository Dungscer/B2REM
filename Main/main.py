import discord
from discord.ext import commands
import logbook
from logbook import FileHandler
from dotenv import load_dotenv
import os
import requests
import time
import asyncio

# Handle environment values
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
LOG_LEVEL = os.getenv("LOG_LEVEL")
ADMIN_USER_ID = os.getenv("ADMIN_USER_ID")
DJANGO_API = os.getenv("DJANGO_API")

# Set the logger for Debuging
FileHandler('Beser.log').push_application()
logger = logbook.Logger('DiscordBot')

intents = discord.Intents(messages=True, guilds=True)
bot = commands.Bot(command_prefix='!', intents=intents)


async def check_status():
    try:
        last_checked = None
        while True:
            response = requests.get(DJANGO_API)
            messages = response.json()
            for message in messages:
                await send_message_to_admin(message)
            last_checked = time.time()
            time.sleep(10) 
    except Exception:
        logger.info("Task error")
    
        

# BOT START
@bot.event
async def on_ready():
    await send_message_to_admin("Besser is started.")
    asyncio.create_task(check_status())
    #bot.loop.create_task(check_status())


async def send_message_to_admin(message):
    logger.info(message)
    user = await bot.fetch_user(ADMIN_USER_ID)
    await user.send("Beser is started boss!")



bot.run(token=TOKEN)