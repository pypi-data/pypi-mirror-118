import bs4
import urllib3
from .scraping.common import *
from .scraping.fifa_index import *
from .objects.fifa_data import *

def all_fifa_player_ids():

    all_players = []
    all_versions = get_all_fifa_versions()
    for year, versions in all_versions.items():
        if year == "FIFA 22":
            continue
        version_players = get_version_players(versions[0]["link"])
        for player in version_players:
            player_row = FifaPlayerRow(player, year, versions[0]["date"])
            all_players.append((player_row.name, player_row.player_id))
    return all_players
