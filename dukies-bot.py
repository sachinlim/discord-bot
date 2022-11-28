import discord
from discord.ext import commands
import os
import asyncio
import actives

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def load():
    for files in os.listdir('./cogs'):
        if files.endswith('.py'):
            await bot.load_extension(f'cogs.{files[:-3]}')


@bot.event
async def on_ready():
    print("Bot is online!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please enter the search term!')


async def main():
    await load()
    await bot.start(actives.token)

asyncio.run(main())
