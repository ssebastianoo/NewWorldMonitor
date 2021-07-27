import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            emb = discord.Embed(description=f"I don't have enough permissions to run this command.", colour=discord.Colour.red())
            return await ctx.reply(embed=emb, mention_author=False, delete_after=5)

        if isinstance(error, commands.CommandNotFound):
            if ctx.guild:
                if ctx.author.guild_permissions.manage_guild:
                    if isinstance(error, commands.CommandNotFound):
                        emb = discord.Embed(description=f"Command not found", colour=discord.Colour.red())
                        return await ctx.reply(embed=emb, mention_author=False, delete_after=5)
            return

        emb = discord.Embed(description=error, colour=discord.Colour.red())
        await ctx.reply(embed=emb, mention_author=False)

def setup(bot):
    bot.add_cog(Events(bot))
