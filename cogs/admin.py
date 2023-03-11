from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clear(self, ctx, amount=1):
        """
        Command to delete previous messages
        +1 is done so that the command call is also deleted
        """
        await ctx.channel.purge(limit=amount + 1)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        Error handler when the user does not pass along a search term with the command

        :param ctx: the message sent by the user
        :param error: error name
        :return: message to inform user to enter a search term
        """
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please enter the search term!')


async def setup(bot):
    await bot.add_cog(Admin(bot))
