import discord, utils, config
from discord.ext import commands, tasks

class Monitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_servers.start()

    @tasks.loop(seconds=60)
    async def check_servers(self):
        try:
            servers = await self.bot.monitor.get_servers_status()
            for server in servers:
                new_status = servers[server]
                old_status = await self.bot.db.get_status(server)
                if not old_status:
                    await self.bot.db.update_server(server, new_status)
                else:
                    if new_status != old_status:
                        emojis = {'up': config.emojis.success, 'down': config.emojis.fail}
                        colour = discord.Colour.green() if new_status == "up" else discord.Colour.red()
                        status = 'Offline' if new_status == 'down' else 'Online'
                        emb = discord.Embed(title=f"<:NW_Official_logo:668448311216308236> {server}", description=f"**{status}** {emojis[new_status]}", colour=colour)

                        msgs = await self.bot.db.get_messages(server)

                        for data in msgs:
                            channel = self.bot.get_channel(data['channel'])
                            try:
                                message = await channel.fetch_message(data['message'])
                                if channel:
                                    await message.edit(content=None, embed=emb)
                            except:
                                pass

                        await self.bot.db.update_server(server, new_status)
        except Exception as e:
            print(e)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def check(self, ctx, server_name=None):

        emb = discord.Embed(description=config.emojis.loading, colour=discord.Colour.green())
        msg = await ctx.reply(embed=emb, mention_author=False)

        language = await self.bot.db.get_language(ctx.guild.id)
        if not server_name:

            servers = await self.bot.monitor.get_servers_status()
            emb = discord.Embed(title=language["checkTitle"], colour=discord.Colour.green(), timestamp=ctx.message.created_at)

            res = "```\n"
            count = 0
            slots = 0
            for server in servers:
                count += 1
                name = f"{server}{' ' * (12 - (len(server) if len(server) >= 0 else 0))}"
                if servers[server] == "up":
                    res += f"{name} {config.emojis.success}\n"
                elif servers[server] == "down":
                    res += f"{name} {config.emojis.fail}\n"

                if count >= 5:
                    res += "\n```"
                    slots += 1
                    emb.add_field(name=language["slot"].replace("{slots}", str(slots)), value=res)

                    count = 0
                    res = "```\n"

            return await msg.edit(embed=emb)

        try:
            server = await self.bot.monitor.get_server_status(server_name)
        except KeyError:
            emb = discord.Embed(description=language["serverNotFound"], colour=discord.Colour.red())
            return await msg.edit(embed=emb)

        emojis = {'up': config.emojis.success, 'down': config.emojis.fail}
        emb = discord.Embed(description = f"**{server['name']}** {emojis[server['status']]}", colour=discord.Colour.green())
        await msg.edit(embed=emb)

    @commands.command(name="set-logs", aliases=["logs", "set-log", "setlog", "setlogs"])
    @commands.has_permissions(manage_guild=True)
    async def set_logs(self, ctx, server, channel: discord.TextChannel=None):
        "Set the channel where server logs will be sent"

        emb = discord.Embed(description=config.emojis.loading, colour=discord.Colour.green())
        msg = await ctx.reply(embed=emb, mention_author=False)

        channel = channel or ctx.channel
        language = await self.bot.db.get_language(ctx.guild.id)

        try:
            server = await self.bot.monitor.get_server_status(server)
        except KeyError:
            emb = discord.Embed(description=language["serverNotFound"], colour=discord.Colour.red())
            return await msg.edit(embed=emb)

        emojis = {'up': config.emojis.success, 'down': config.emojis.fail}
        colour = discord.Colour.green() if server['status'] == "up" else discord.Colour.red()
        status = 'Offline' if server['status'] == 'down' else 'Online'
        emb = discord.Embed(title=f"<:NW_Official_logo:668448311216308236> {server['name']}", description=f"**{status}** {emojis[server['status']]}", colour=colour)
        msg_ = await channel.send(embed=emb)

        await self.bot.db.update_message(server['name'], msg_.id, channel.id, ctx.guild.id)
        await msg.edit(content=language["updateServer"].replace("{server['name']}", server['name']).replace("{channel.mention}", channel.mention), embed=None)

    @commands.command(name="remove-logs", aliases=["removelogs", "removelog", "remove-log"])
    @commands.has_permissions(manage_guild=True)
    async def remove_logs(self, ctx, server):
        "Remove logs"

        emb = discord.Embed(description=config.emojis.loading, colour=discord.Colour.green())
        msg = await ctx.reply(embed=emb, mention_author=False)

        language = await self.bot.db.get_language(ctx.guild.id)

        if server.lower() == "all":
            servers = await self.bot.monitor.get_servers_status()
            for s in servers:
                await self.bot.db.remove_log(s, ctx.guild.id)
            return await msg.edit(content=language['removeAllLogs'], embed=None)

        try:
            server = await self.bot.monitor.get_server_status(server)
        except KeyError:
            emb = discord.Embed(description=language['serverNotFound'], colour=discord.Colour.red())
            return await msg.edit(embed=emb)

        await self.bot.db.remove_log(server['name'].lower(), ctx.guild.id)
        await msg.edit(content=language['removeLogs'].replace("{server['name']}", server['name']), embed=None)

    @commands.command(name="check-logs", aliases=["checklogs", "check-log", "checklog"])
    @commands.has_permissions(manage_guild=True)
    async def check_logs(self, ctx):
        "Check logs settings"

        emb = discord.Embed(description=config.emojis.loading, colour=discord.Colour.green())
        msg = await ctx.reply(embed=emb, mention_author=False)

        language = await self.bot.db.get_language(ctx.guild.id)

        logs = await self.bot.db.get_logs(ctx.guild.id)
        if not logs:
            return await msg.edit(content=language["logsEmpty"], embed=None)

        emb = discord.Embed(title=f"{ctx.guild.name} Logs", description="", colour=discord.Colour.green())
        for log in logs:
            channel = self.bot.get_channel(log)
            if channel:
                emb.description += f"• {channel.mention}\n> {' '.join([f'`{server}`' for server in logs[log]])}\n\n"
        await msg.edit(embed=emb)

def setup(bot):
    bot.add_cog(Monitor(bot))
