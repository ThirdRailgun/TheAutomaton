from anime import Anime
from discord.ext import commands
from time import sleep
import unittest

#TODO: Something must have changed with test_skip_1-3 because they now are failing.
#the sleep commands are in place because I don't want to call on the API in quick successions.
class TestCommandAnime(unittest.TestCase):
    mock_client = Anime(client = commands.Bot(command_prefix="/"))

    def test_name(self):
        assert self.mock_client.anime_logic("Steins;Gate").get("title_english") == "Steins;Gate"
        sleep(2)

    def test_skip_1(self):
        assert self.mock_client.anime_logic("Steins;Gate", "-s", "1").get("title_english") == "Steins;Gate 0"
        sleep(2)

    def test_skip_2(self):
        assert self.mock_client.anime_logic("Steins;Gate", "--skip", "1").get("title_english") == "Steins;Gate 0"
        sleep(2)
    
    def test_skip_3(self):
        assert self.mock_client.anime_logic("Steins;Gate", "-s", "2").get("title_english") == "Steins;Gate: Egoistic Poriomania"
        sleep(2)

    def test_skip_4(self):
        assert self.mock_client.anime_logic("Steins;Gate", "-s").get("title_english") == "Steins;Gate"
        sleep(2)

    def test_error(self):
        assert isinstance(self.mock_client.anime_logic(""), Exception) == True

if __name__ == '__main__':
    unittest.main()