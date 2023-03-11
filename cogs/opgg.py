import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime


class Opgg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def op_format(self, summoner_name):
        """
        op.gg replaces blank spaces with "%20"

        :param summoner_name: name of a player being passed onto the bot by the user
        :return: formatted name with "%20" being used to replace spaces
        """
        formatted = summoner_name
        if " " in summoner_name:
            formatted = summoner_name.replace(' ', '%20')

        return formatted

    def get_data(self, summoner_name):
        """
        Scraping data from op.gg live game viewer
        The player must be in a spectate-able game to be able to view this information
        The name of the champion the players are playing is obtained, rather than providing the player's username

        :param summoner_name: name of a player being passed onto the bot by the user
        :return: a list containing the champion's name, current rank and win rate for all 10 players
        """
        url = f'https://www.op.gg/summoners/euw/{summoner_name}/ingame'

        path = 'chromedriver'
        driver = webdriver.Chrome(path)
        driver.get(url)

        summoners = []
        ranks = []
        win_rates = []

        summoner_name = driver.find_elements(By.XPATH, '//td[1]/a/div/img')
        for summoner in summoner_name:
            champ = summoner.get_attribute('alt')
            summoners.append(champ)

        current_rank = driver.find_elements(By.CLASS_NAME, 'current-rank')
        for rank in current_rank:
            formatted = rank.text.replace('(', ' (')
            ranks.append(formatted)

        winratio = driver.find_elements(By.XPATH, '//td[7]')
        for ratios in winratio:
            win_rates.append(ratios.text)

        final_list = list(zip(summoners, ranks, win_rates))

        driver.quit()
        return final_list

    @commands.command()
    async def op(self, ctx, *, summoner_name):
        """
        op.gg profile for summoner name entered after command

        :param ctx: value being passed on by the user
        :param summoner_name: name of the player to search for
        :return: URL link to user profile on op.gg with the player's name
        """
        formatted = self.op_format(summoner_name)
        await ctx.send(f'https://www.op.gg/summoners/euw/{formatted}')

    @commands.command()
    async def ig(self, ctx, *, summoner_name):
        """
        Link to op.gg live game webpage for specified summoner name

        :param ctx: value being passed on by the user
        :param summoner_name: name of the player to search for
        :return: URL link to an active game that can provide a detailed view about the current matchups
        """
        if " " in summoner_name:
            formatted = self.op_format(summoner_name)
            await ctx.send(f'https://www.op.gg/summoners/euw/{formatted}/ingame')
        else:
            await ctx.send(f'https://www.op.gg/summoners/euw/{summoner_name}/ingame')

    @commands.command()
    async def ig2(self, ctx, *, summoner_name):
        """
        Scraping live game information from the website available on op.gg
        Sends out an embedded message to show match-up without having to go to the link provided in ig()

        :param ctx: value being passed on by the user
        :param summoner_name: name of the player to search for
        :return: embedded message with 3 fields that display relevant information about the game the player is in
        """
        formatted = self.op_format(summoner_name)

        embed = discord.Embed(
            title="Live Game Match-Up",
            description=f"From {summoner_name}'s op.gg \n https://www.op.gg/summoners/euw/{formatted}/ingame",
            colour=0xbc8125,
        )

        blue_champs = blue_ranks = blue_wr = ""
        red_champs = red_ranks = red_wr = ""

        data = self.get_data(formatted)

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


async def setup(bot):
    await bot.add_cog(Opgg(bot))
