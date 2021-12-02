import discord
import random
from discord.ext import commands
import youtube_dl



class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You are not in a voice channel!")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            await ctx.send("Joined voice channel!")
        else:
            await ctx.voice_client.move_to(voice_channel)
            await ctx.send("Voice channel changed!")

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from voice channel!")

    @commands.command()
    async def play(self, ctx, url):
        '''ctx.voice_client.stop()'''
        await ctx.send("Playing:" + url)
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}
        YDL_OPTIONS = {'format': "bestaudio"}
        vc = ctx.voice_client
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            vc.play(source)

    @commands.command()
    async def pause(self, ctx):
        await ctx.send("Paused")
        await ctx.voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        await ctx.send("Resumed")
        await ctx.voice_client.resume()

    @commands.command()
    async def coinflip(self, ctx):
        flip = random.randint(0, 1)
        if flip == 0:
            await ctx.send("Heads")
        else:
            await ctx.send("Tails")



def setup(client):
    client.add_cog(music(client))
