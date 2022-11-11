import discord
from discord.ext import commands
import random
import datetime
import passives
import in_game_scraper

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("Bot is working!")


# Shortens weblinks from eBay and Amazon before deleting the long link
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
    if " " in summoner_name:
        formatted = summoner_name.replace(" ", "%20")
        await ctx.send("https://www.op.gg/summoners/euw/" + formatted)
    else:
        await ctx.send("https://www.op.gg/summoners/euw/" + summoner_name)


# Link to live game for summoner name entered after command
@bot.command()
async def ig2(ctx, *, summoner_name):
    formatted = summoner_name
    if " " in summoner_name:
        formatted = summoner_name.replace(" ", "%20")

    embed = discord.Embed(
        title = "Live Game Match-Up",
        description = f"From {summoner_name}'s op.gg \n https://www.op.gg/summoners/euw/{formatted}/ingame",
        colour = 0xbc8125
    )

    blue_side, red_side = in_game_scraper.return_lists()

    blue_champs = blue_ranks = blue_wr = ""
    red_champs = red_ranks = red_wr = ""

    for items in blue_side:
        blue_champs += items[0] + '\n'
        blue_ranks += items[1] + '\n'
        blue_wr += items[2] + '\n'

    for items in red_side:
        red_champs += items[0] + '\n'
        red_ranks += items[1] + '\n'
        red_wr += items[2] + '\n'

    embed.add_field(name = "Blue Team", value = blue_champs, inline = True)
    embed.add_field(name = "Rank", value = blue_ranks, inline = True)
    embed.add_field(name = "Win Rate", value = blue_wr, inline = True)

    embed.add_field(name = "Red Team", value = red_champs, inline = True)
    embed.add_field(name = "Rank", value = red_ranks, inline = True)
    embed.add_field(name = "Win Rate", value = red_wr, inline = True)

    embed.set_thumbnail(url= 'https://static.wikia.nocookie.net/leagueoflegends/images/0/02/Season_2022_-_Challenger.png')
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text= '\u200b',
                     icon_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/LoL_icon.svg/1200px-LoL_icon.svg.png')

    await ctx.send(embed = embed)


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
    if " " in champion_name:
        formatted = champion_name.replace(" ", "")
        await ctx.send("https://probuildstats.com/champion/" + formatted)
    else:
        await ctx.send("https://probuildstats.com/champion/" + champion_name)


# u.gg build guide for specified Champion
@bot.command()
async def ugg(ctx, *, champion_name):
    if " " in champion_name:
        formatted = champion_name.replace(" ", "")
        await ctx.send("https://u.gg/lol/champions/" + formatted + "/build")
    else:
        await ctx.send("https://u.gg/lol/champions/" + champion_name + "/build")


bot.run(passives.token)
