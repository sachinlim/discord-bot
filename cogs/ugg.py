from discord.ext import commands


class Ugg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def ugg_format(self, champion_name):
        # Both u.gg and Pro Builds removes spaces for web links
        formatted = champion_name
        if ' ' in champion_name:
            formatted = champion_name.replace(' ', '')

        return formatted

    @commands.command()
    async def ug(self, ctx, *, champion_name):
        # Provides a link to u.gg build guide for specified Champion
        formatted = self.ugg_format(champion_name)
        await ctx.send(f'https://u.gg/lol/champions/{formatted}/build')

    @commands.command()
    async def pb(self, ctx, *, champion_name):
        # Provides a link to ProBuilds for specified Champion
        formatted = self.ugg_format(champion_name)
        await ctx.send(f'https://probuildstats.com/champion/{formatted}')


async def setup(bot):
    await bot.add_cog(Ugg(bot))
