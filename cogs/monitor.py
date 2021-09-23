import discord, utils, config, datetime
from discord.ext import commands, tasks
from termcolor import colored

class Monitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_servers.start()
        self.converter = commands.TextChannelConverter()

    @tasks.loop(seconds=10)
    async def check_servers(self):
        now = datetime.datetime.utcnow().strftime("[%Y/%m/%d %X UTC]")
        try:
            print(f"{now} fetching servers...")
            servers = await self.bot.monitor.get_servers_status()
            print( colored(f"{now} found {len(servers)} servers", 'green') )
            print(f"{now} searching for changes")
            changed = False
            for server in servers:
                new_status = servers[server]
                old_status = await self.bot.db.get_status(server)
                if not old_status:
                    print( colored(f"{now} {server} doesn't have a status, fixing...", 'yellow'))
                    await self.bot.db.update_server(server, new_status)
                    print( colored(f"created status for {server} ({new_status})\n", 'green'))
                else:
                    if new_status != old_status:
                        print( colored(f"{now} found a change for server {server} (old: {old_status} new: {new_status})", 'yellow'))
                        colour = config.bot.colour[new_status]
                        status = config.bot.full_status[new_status]
                        emb = discord.Embed(title=f"<:NW_Official_logo:668448311216308236> {server}", description=f"**{status}** {config.emojis.status[new_status]}", colour=colour)

                        msgs = await self.bot.db.get_messages(server)
                        if msgs:
                            print(f"{now} getting all messages to edit")
                            for data in msgs:
                                channel = self.bot.get_channel(data['channel'])
                                try:
                                    message = await channel.fetch_message(data['message'])
                                    if channel:
                                        await message.edit(content=None, embed=emb)
                                except:
                                    pass
                            print(f"{now} finished editing")
                        else:
                            print(f"{now} server doesn't have any log")

                        await self.bot.db.update_server(server, new_status)
                        print( colored(f"{now} updated status for server {server} to {new_status}\n", 'green'))
                        changed = True
            if not changed:
                print( colored(f'{now} nothing to change', 'yellow') )
            print("\n")
        except Exception as e:
            print( colored(f'{now} {e}', 'red') )

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def check(self, ctx, *, server=None):

        "Check server statuses"
        
        server_name = server
        print(server_name)

        emb = discord.Embed(description=config.emojis.loading, colour=discord.Colour.green())
        msg = await ctx.reply(embed=emb, mention_author=False)

        language = await self.bot.db.get_language(ctx.guild)
        if not server_name:

            servers = await self.bot.monitor.get_servers_status()
            emb = discord.Embed(title=language["checkTitle"], colour=discord.Colour.green(), timestamp=ctx.message.created_at)

            res = "```\n"
            count = 0
            slots = 0
            for server in servers:
                count += 1
                name = f"{server}{' ' * (12 - (len(server) if len(server) >= 0 else 0))}"
                res += f"{name} {config.emojis.status[servers[server]]}\n"

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

        emb = discord.Embed(description = f"**{server['name']}** {config.emojis.status[server['status']]}", colour=discord.Colour.green() if server['status'] == "up" else discord.Colour.red())
        await msg.edit(embed=emb)

    @commands.command(name="set-logs", aliases=["logs", "set-log", "setlog", "setlogs"], usage="<server> [channel]")
    @commands.has_permissions(manage_guild=True)
    async def set_logs(self, ctx, server, channel: discord.TextChannel=None):
        "Set the channel where server logs will be sent"

        channel = channel or ctx.channel

        emb = discord.Embed(description=config.emojis.loading, colour=discord.Colour.green())
        msg = await ctx.reply(embed=emb, mention_author=False)

        channel = channel or ctx.channel
        language = await self.bot.db.get_language(ctx.guild)

        try:
            server = await self.bot.monitor.get_server_status(server)
        except KeyError:
            emb = discord.Embed(description=language["serverNotFound"], colour=discord.Colour.red())
            return await msg.edit(embed=emb)

        colour = config.bot.colour[server['status']]
        status = config.bot.full_status[server['status']]
        emb = discord.Embed(title=f"<:NW_Official_logo:668448311216308236> {server['name']}", description=f"**{status}** {config.emojis.status[server['status']]}", colour=colour)
        msg_ = await channel.send(embed=emb)

        await self.bot.db.update_message(server['name'], msg_.id, channel.id, ctx.guild.id)
        await msg.edit(content=language["updateServer"].replace("{server['name']}", server['name']).replace("{channel.mention}", channel.mention), embed=None)

    @commands.command(name="remove-logs", aliases=["removelogs", "removelog", "remove-log"])
    @commands.has_permissions(manage_guild=True)
    async def remove_logs(self, ctx, *, server):
        "Remove logs"

        emb = discord.Embed(description=config.emojis.loading, colour=discord.Colour.green())
        msg = await ctx.reply(embed=emb, mention_author=False)

        language = await self.bot.db.get_language(ctx.guild)

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

        language = await self.bot.db.get_language(ctx.guild)

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
