from discord.ext import commands


class ProBuilds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Both u.gg and Pro Builds removes spaces for web links
    def ugg_format(self, champion_name):
        formatted = champion_name
        if " " in champion_name:
            formatted = champion_name.replace(" ", "")

        return formatted

    # Pro Builds for specified Champion
    @commands.command()
    async def pb(self, ctx, *, champion_name):
        formatted = self.ugg_format(champion_name)
        await ctx.send("https://probuildstats.com/champion/" + formatted)