from discord.ext import commands


class op(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # op.gg replaces blank spaces with "%20"
    def op_format(self, summoner_name):
        formatted = summoner_name
        if " " in summoner_name:
            formatted = summoner_name.replace(' ', '%20')

        return formatted

    # op.gg profile for summoner name entered after command
    @commands.command()
    async def op(self, ctx, *, summoner_name):
        formatted = self.op_format(summoner_name)
        await ctx.send(f'https://www.op.gg/summoners/euw/{formatted}')

    @commands.command()
    async def ig3(self, ctx, *, summoner_name):
        if " " in summoner_name:
            formatted = self.op_format(summoner_name)
            await ctx.send(f'https://www.op.gg/summoners/euw/{formatted}/ingame')
        else:
            await ctx.send(f'https://www.op.gg/summoners/euw/{summoner_name}/ingame')


async def setup(bot):
    await bot.add_cog(op(bot))
