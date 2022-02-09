import discord
from discord.ext import commands
import os.path
from anime import Anime
from music import Music

#discordToken.txt is the the token used to authenticate with Discord.
SECRET_TOKEN = open(os.path.join("data", "discordToken.txt")).read()
client = commands.Bot(command_prefix="/")

@client.event
async def on_ready():
    print("Currently logged in as: {} | {}".format(client.user.name, client.user.id))

    client.add_cog(Anime(client))
    client.add_cog(Music(client))

client.run(SECRET_TOKEN)