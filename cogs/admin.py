from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clear(self, ctx, amount=1):
        # command to delete previous messages
        await ctx.channel.purge(limit=amount + 1)


async def setup(bot):
    await bot.add_cog(Admin(bot))
