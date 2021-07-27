import discord, config
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

    @commands.command(name="set-language", aliases=["setlanguage", "language", "lang", "set-lang"])
    @commands.has_permissions(manage_guild=True)
    async def set_language(self, ctx, language_name):
        "Change the bot language"

        language = await self.bot.db.get_language(ctx.guild.id)

        if language_name.lower() not in [l.lower() for l in config.av_languages]:
            emb = discord.Embed(description=language["invalidLanguage"].replace("{' '.join(config.av_languages)}", str(', '.join(config.av_languages))), colour=discord.Colour.red())
            return await ctx.reply(embed=emb, mention_author=False)

        await self.bot.db.update_language(ctx.guild.id, language_name)
        language = await self.bot.db.get_language(ctx.guild.id)
        await ctx.reply(language["languageUpdate"].replace("{language_name}", language_name), mention_author=False)

def setup(bot):
    bot.add_cog(Misc(bot))
