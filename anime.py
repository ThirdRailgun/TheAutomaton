from jikanpy import Jikan
from jikanpy.exceptions import APIException
import discord
from discord.ext import commands
import argparse
import json

class Anime(commands.Cog):
    def __init__(self, client):
        self.jikan = Jikan()
        self.client = client
        self.parsedCommand = []

    #this was written this way so that it could be called by a testing script.
    #also it uses argparse which is pretty cool I guess. but what user would be calling this directly?
    def anime_logic(self, *args):
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("-s", "--skip", default=0, action="store", type=int, nargs="?")
        self.parsedCommand = parser.parse_known_args(args)

        try:
            if self.parsedCommand[0].skip == None:
                self.parsedCommand[0].skip = 0
            searchResults = self.jikan.search("anime", self.parsedCommand[1][0])["results"]
            animeID = searchResults[self.parsedCommand[0].skip]["mal_id"]
            anime = self.jikan.anime(animeID)
        except (IndexError, APIException) as e:
            return e

        return anime

    #creation of embed object and the posting of it to discord.
    @commands.command(name="anime")
    async def anime_skeleton(self, context, *args):
        anime = self.anime_logic(*args)
        if isinstance(anime, Exception):
            await context.send("Python Exception: {}".format(str(anime).title()))
            return
        embed=discord.Embed(title=anime.get("title_english"), url=anime.get("url"), description=(anime.get("synopsis")[:500] + "[...]") if len(anime.get("synopsis")) > 500 else anime.get("synopsis"))
        embed.set_author(name="MyAnimeList", url="https://myanimelist.net/", icon_url="https://image.myanimelist.net/ui/OK6W_koKDTOqqqLDbIoPAiC8a86sHufn_jOI-JGtoCQ")
        embed.set_thumbnail(url=anime.get("image_url"))
        await context.send(embed=embed)