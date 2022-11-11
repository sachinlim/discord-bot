import discord
from discord.ext import commands
import random
import datetime
import passives
import actives
import in_game_scraper

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("Bot is working!")


# Shortens website links from eBay and Amazon before deleting the long link
@bot.listen("on_message")
async def on_message(message):
    # Shortens eBay links
    if message.content.startswith('https://www.ebay.co.uk/itm/'):
        if "?" in message.content:
            new_link = message.content.split("?")[0]

            await message.channel.send(new_link)
            await message.delete()

    # Shortens Amazon links
    if message.content.startswith('https://www.amazon.co.uk/'):
        if "/dp/" in message.content:
            new_link = message.content.split("/")
            dp_pos = new_link.index("dp")
            id_pos = dp_pos + 1

            await message.channel.send("https://amazon.co.uk/" + new_link[dp_pos] + "/" + new_link[id_pos])
            await message.delete()

        if "/gp/" in message.content:
            new_link = message.content.split("/")
            gp_pos = new_link.index("gp")
            product_pos = gp_pos + 1
            id_pos = gp_pos + 2

            await message.channel.send("https://amazon.co.uk/" + new_link[gp_pos] + "/" + new_link[product_pos]
                                       + "/" + new_link[id_pos])
            await message.delete()


@bot.command()
async def lolrole(ctx):
    roles = ["Top", "Jungle", "Mid", "ADC", "Support"]
    await ctx.send(random.choice(roles))


# op.gg profile for summoner name entered after command
@bot.command()
async def op(ctx, *, summoner_name):
    formatted = passives.op_format(summoner_name)
    await ctx.send("https://www.op.gg/summoners/euw/" + formatted)


@bot.command()
async def ig(ctx, *, summoner_name):
    if " " in summoner_name:
        formatted = summoner_name.replace(" ", "%20")
        await ctx.send("https://www.op.gg/summoners/euw/" + formatted + "/ingame")
    else:
        await ctx.send("https://www.op.gg/summoners/euw/" + summoner_name + "/ingame")


# Pro Builds for specified Champion
@bot.command()
async def pb(ctx, *, champion_name):
    formatted = passives.ugg_format(champion_name)
    await ctx.send("https://probuildstats.com/champion/" + formatted)


# u.gg build guide for specified Champion
@bot.command()
async def ug(ctx, *, champion_name):
    formatted = passives.ugg_format(champion_name)
    await ctx.send("https://u.gg/lol/champions/" + formatted + "/build")


bot.run(actives.token)
