import discord
from discord.ext import commands
import config

client = commands.Bot(command_prefix=config.PREFIX)


@client.command()
async def hello(ctx):
    await ctx.send("cytryna")

client.run(config.TOKEN)
