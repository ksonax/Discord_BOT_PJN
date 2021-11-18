import discord
import config

client = discord.Client()


@client.event
async def on_message(message):
    if str(message.channel) == config.IMAGE_CHANNEL and message.content != "":
        await message.channel.purge(limit=1)

client.run('config.TOKEN')
