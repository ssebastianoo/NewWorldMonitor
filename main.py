import discord, config, os, aiohttp, aiosqlite, utils
from discord.ext import commands

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"

bot = commands.Bot(command_prefix=config.bot.prefix, intents=discord.Intents(guilds=True, messages=True), slash_commands=True)
bot.load_extension("jishaku")
bot.remove_command("help")

@bot.event
async def on_ready():
    conn = await aiosqlite.connect("db.db")
    bot.db = utils.DataBase(conn)
    await bot.db.check()
    bot.session = aiohttp.ClientSession()
    bot.monitor = utils.Monitor(bot.session)
    print("ready as", bot.user)

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(config.bot.token)
