import discord
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        "Invite the bot to your server"

        language = await self.bot.db.get_language(ctx.guild.id)

        invite = discord.utils.oauth_url(self.bot.user.id, permissions=discord.Permissions(permissions=18432), scopes=('bot','applications.commands'))
        emb = discord.Embed(description=f"[{language['invite']}]({invite})", colour=discord.Colour.blurple())
        await ctx.reply(embed=emb, mention_author=False)

def setup(bot):
    bot.add_cog(Misc(bot))
