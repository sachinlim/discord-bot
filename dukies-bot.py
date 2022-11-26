import discord
from discord.ext import commands
import random
import datetime
import passives
import actives
import in_game_scraper
import ebay_scraper

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("Bot is working!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please enter the search term!')


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


# Link to live game for summoner name entered after command
@bot.command()
async def ig(ctx, *, summoner_name):
    formatted = passives.op_format(summoner_name)

    embed = discord.Embed(
        title="Live Game Match-Up",
        description=f"From {summoner_name}'s op.gg \n https://www.op.gg/summoners/euw/{formatted}/ingame",
        colour=0xbc8125,
    )

    blue_champs = blue_ranks = blue_wr = ""
    red_champs = red_ranks = red_wr = ""

    data = in_game_scraper.get_data(formatted)

    for summoner_name in data[0:5]:
        blue_champs += summoner_name[0] + '\n'
        blue_ranks += summoner_name[1] + '\n'
        blue_wr += summoner_name[2] + '\n'

    embed.add_field(name="Blue Team", value=blue_champs, inline=True)
    embed.add_field(name="Rank", value=blue_ranks, inline=True)
    embed.add_field(name="Win Rate", value=blue_wr, inline=True)

    for summoner_name in data[5:10]:
        red_champs += summoner_name[0] + '\n'
        red_ranks += summoner_name[1] + '\n'
        red_wr += summoner_name[2] + '\n'

    embed.add_field(name="Red Team", value=red_champs, inline=True)
    embed.add_field(name="Rank", value=red_ranks, inline=True)
    embed.add_field(name="Win Rate", value=red_wr, inline=True)

    embed.set_thumbnail(url='https://static.wikia.nocookie.net/leagueoflegends/images/0/02/Season_2022_-_Challenger'
                            '.png')
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text='\u200b',
                     icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/LoL_icon.svg/1200px'
                              '-LoL_icon.svg.png')

    await ctx.send(embed=embed)


@bot.command()
async def ig2(ctx, *, summoner_name):
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


# patch notes
@bot.command()
async def patch(ctx, *, game):
    match game:
        case 'lol':
            await ctx.send('https://www.leagueoflegends.com/en-us/news/tags/patch-notes/')
        case 'tft':
            await ctx.send('https://teamfighttactics.leagueoflegends.com/en-us/news/')
        case 'valo':
            await ctx.send('https://playvalorant.com/en-us/news/game-updates/')
        case _:
            await ctx.send('Please enter a valid game after !patch. The supported games are: lol, tft, valo')


# command to delete previous messages
@bot.command()
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount + 1)


@bot.command()
async def ebay(ctx, *, item):
    formatted_search_term = item
    if " " in item:
        formatted_search_term = item.replace(" ", "+")

    soup = ebay_scraper.website_data(formatted_search_term)
    my_list = ebay_scraper.get_data(soup)
    mean, median, mode = ebay_scraper.calculate_averages(my_list)

    embed = discord.Embed(
        title='eBay Sold Items Search',
        description='The values below may not reflect all of the items in the market due to the filers used in '
                    'eBay Advanced search',
        colour=0x6b9312,
    )

    embed.add_field(name="Average", value=f'£{mean:.2f}', inline=False)
    embed.add_field(name="Median", value=f'£{median:.2f}', inline=False)
    embed.add_field(name="Mode", value=f'£{mode:.2f}', inline=False)

    embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/EBay_logo.svg/2560px-EBay_logo.svg.png')
    embed.set_footer(text=f'There are a total of {len(my_list)} results')

    await ctx.send(embed=embed)


bot.run(actives.token)
