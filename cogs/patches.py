from discord.ext import commands


class Patches(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def patch(self, ctx, *, game):
        """
        Patch notes for specified game
        """
        match game:
            case 'lol':
                await ctx.send('https://www.leagueoflegends.com/en-us/news/tags/patch-notes/')
            case 'tft':
                await ctx.send('https://teamfighttactics.leagueoflegends.com/en-us/news/')
            case 'valo':
                await ctx.send('https://playvalorant.com/en-us/news/game-updates/')
            case _:
                await ctx.send('Please enter a valid game after !patch. The supported games are: lol, tft, valo')


async def setup(bot):
    await bot.add_cog(Patches(bot))
