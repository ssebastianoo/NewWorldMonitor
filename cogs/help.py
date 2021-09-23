import discord, config
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden = True)
    async def help(self, ctx, *, command=None):
        "Get some help"

        prefix = ctx.prefix
        emb = discord.Embed(colour=discord.Colour.blurple())
        emb.set_author(name=self.bot.user.name, icon_url=str(self.bot.user.display_avatar.replace(static_format = "png")))
        emb.set_footer(text=ctx.author, icon_url=str(ctx.author.display_avatar.replace(static_format = "png")))
        error = discord.Embed(description = f"""```sh
Command \"{command}\" not found
```""", colour = discord.Colour.red())

        if command:
            command = self.bot.get_command(command)

            if not command or command.name == "jishaku":
                return await ctx.send(embed=error)

            res =  f"```{command.help}```"

            if command.parent:
                name = command.parent.name + " " + command.name
                res += f"\n**Parent**\n> `{command.parent}`"

            else:
                name = command.name

            if command.signature:
                usage = f"{name} {command.signature}"
            else:
                usage = name

            res += f"**\nUsage**\n> `{usage}`"

            if command.aliases:
                al = [f"`{a}`" for a in command.aliases]
                res += f"\n**Aliases**\n> {' '.join(al)}"

            try:
                sub = [f"`{a}`" for a in command.commands]
                res += f"\n**Subcommands**\n> {' '.join(sub)}"
            except:
                pass

            emb.description = res
            return await ctx.send(embed = emb)

        res = ""
        for cog_ in sorted(self.bot.cogs, key=lambda x : len(self.bot.get_cog(x).get_commands())):
            res_ = ">>> "
            if str(cog_) != "Jishaku":
                cog = self.bot.get_cog(cog_)
                cog_cmds = cog.get_commands()
                act_cmds = [a for a in cog_cmds if not a.hidden]
                if len(act_cmds) >= 1:
                    for b in cog_cmds:
                        if not b.hidden:
                            res_ += f"`{prefix}{b.name}` "
                            try:
                                for c in b.commands:
                                    if not c.hidden:
                                        res_ += f"`{prefix}{c.parent} {c.name}` "
                            except:
                                pass

                    res += f"{res_}\n"
                    emb.add_field(name=str(cog_), value=res_)

        emb.set_footer(text=f"Need more help? Use \"{prefix}help <command>\".", icon_url = str(ctx.author.display_avatar.replace(static_format = "png")))
        await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(Help(bot))
