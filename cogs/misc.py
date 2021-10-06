import discord, config
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        "Invite the bot to your server"

        language = await self.bot.db.get_language(ctx.guild)

        invite = discord.utils.oauth_url(self.bot.user.id, permissions=discord.Permissions(permissions=18432), scopes=('bot','applications.commands'))
        emb = discord.Embed(description=f"[{language['invite']}]({invite})", colour=discord.Colour.blurple())
        await ctx.send(embed=emb)

    @commands.command(name="set-language", aliases=["setlanguage", "language", "lang", "set-lang"])
    @commands.has_permissions(manage_guild=True)
    async def set_language(self, ctx, language):
        "Change the bot language"

        language_name = language

        language = await self.bot.db.get_language(ctx.guild)

        if language_name.lower() not in [l.lower() for l in config.av_languages]:
            emb = discord.Embed(description=language["invalidLanguage"].replace("{' '.join(config.av_languages)}", str(', '.join(config.av_languages))), colour=discord.Colour.red())
            return await ctx.send(embed=emb)

        await self.bot.db.update_language(ctx.guild.id, language_name)
        language = await self.bot.db.get_language(ctx.guild)
        await ctx.send(language["languageUpdate"].replace("{language_name}", language_name))

def setup(bot):
    bot.add_cog(Misc(bot))
