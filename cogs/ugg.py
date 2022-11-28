from discord.ext import commands


class Ugg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Both u.gg and Pro Builds removes spaces for web links
    def ugg_format(self, champion_name):
        formatted = champion_name
        if " " in champion_name:
            formatted = champion_name.replace(" ", "")

        return formatted

    # Provides a link to u.gg build guide for specified Champion
    @commands.command()
    async def ug(self, ctx, *, champion_name):
        formatted = self.ugg_format(champion_name)
        await ctx.send("https://u.gg/lol/champions/" + formatted + "/build")

    # Provides a link to ProBuilds for specified Champion
    @commands.command()
    async def pb(self, ctx, *, champion_name):
        formatted = self.ugg_format(champion_name)
        await ctx.send("https://probuildstats.com/champion/" + formatted)


async def setup(bot):
    await bot.add_cog(Ugg(bot))
