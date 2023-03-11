from discord.ext import commands


class Ugg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def ugg_format(self, champion_name):
        """
        Both u.gg and Pro Builds removes spaces for web links

        :param champion_name: name of the champion that was passed on by the user
        :return: formatted name with no spaces
        """
        formatted = champion_name
        if ' ' in champion_name:
            formatted = champion_name.replace(' ', '')

        return formatted

    @commands.command()
    async def ug(self, ctx, *, champion_name):
        """
        Provides a link to u.gg build guide for specified Champion

        :param ctx: message that the bot obtains from the user
        :param champion_name: name of the champion being passed on after the command is entered
        :return: URL link to the champion's build recommendations on u.gg
        """
        formatted = self.ugg_format(champion_name)
        await ctx.send(f'https://u.gg/lol/champions/{formatted}/build')

    @commands.command()
    async def pb(self, ctx, *, champion_name):
        """
        Provides a link to ProBuilds for specified Champion

        :param ctx: message that the bot obtains from the user
        :param champion_name: name of the champion being passed on after the command is entered
        :return: URL link to the champion's builds that pro players are, displayed on ProBuilds' website
        """
        formatted = self.ugg_format(champion_name)
        await ctx.send(f'https://probuildstats.com/champion/{formatted}')


async def setup(bot):
    await bot.add_cog(Ugg(bot))
