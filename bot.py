import disnake
from disnake.ext import commands, tasks
TOKEN = 'TOKEN'

bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=discord.Intents.all())
