import discord
from discord.ext import commands
from glob import glob
import os.path
import random

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.path = ["data", "audio"]
        self.player = None

    @commands.command(name="connect")
    async def connect(self, context):
        if context.message.author.voice is None: #check if the invoker is in a channel
            await context.send("Error: User is not in a valid channel.")
            return
        if context.message.author.voice.channel.permissions_for(context.message.author.guild.get_member(self.client.user.id)).view_channel == False: #check if I have permission to join
            await context.send("Error: User is in a private channel.")
            return
        if context.voice_client is not None: # check if the bot is already connected elsewhere
            await context.voice_client.move_to(context.author.voice.channel)
        else:
            await context.author.voice.channel.connect()

    #TODO: Add idle disconnect timer.
    @commands.command(name="disconnect")
    async def disconnect(self, context):
        if context.voice_client is not None and context.voice_client.is_playing():
            discord.PCMVolumeTransformer.cleanup(self.player)
        await context.voice_client.disconnect()

    #TODO: Re-loop the music when it is done playing.
    @commands.command(name="play")
    async def play(self, context):
        if context.voice_client is None:
            await context.send("Error: Bot is not in a valid voice channel.")
            return

        files = glob(os.path.join(*self.path, "*.mp3"))
        self.player = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(random.choice(files)))
        try:
            context.voice_client.play(self.player)
        except discord.errors.ClientException as e:
            await context.send("Error: {}".format(e))

    @commands.command(name="stop")
    async def stop(self, context):
        if context.voice_client is not None and context.voice_client.is_playing():
            context.voice_client.stop()

    @commands.command(name="pause")
    async def pause(self, context):
        if context.voice_client is not None and context.voice_client.is_playing():
            context.voice_client.pause()

    @commands.command(name="resume")
    async def resume(self, context):
        if context.voice_client is not None and context.voice_client.is_playing() == False:
            context.voice_client.resume()