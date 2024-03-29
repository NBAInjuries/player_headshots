import os
import time
import errno
from shutil import copyfileobj

from requests import get
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.static.teams import get_teams

CURRENT_SEASON = '2023-24'


def create_path(path: str):
    if os.path.exists(path):
        return

    try:
        os.makedirs(path, exist_ok=True)  # Python>3.2
    except TypeError:
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise


def main():
    """
    Based on https://stackoverflow.com/a/13137873/16179502
    """
    teams = get_teams()

    for team_idx, team in enumerate(teams):
        print(f"[ {team_idx + 1} / {len(teams)} ] Looking at roster of '{team['full_name']}'")

        team_id = team['id']
        team_roster = commonteamroster.CommonTeamRoster(team_id=team_id).get_data_frames()[0]

        for player_idx, player_row in team_roster.iterrows():
            print(f"\t[ {player_idx + 1} / {len(team_roster)} ] Getting headshot for '{player_row['PLAYER']}'")

            player_id = player_row['PLAYER_ID']
            headshot_link = f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png"

            raw_file = get(headshot_link, stream=True)
            destination_path = f"{os.path.dirname(__file__)}/images/{CURRENT_SEASON}/{player_id}-{team_id}.png"
            create_path(f"{os.path.dirname(__file__)}/images/{CURRENT_SEASON}")

            if raw_file.status_code == 200:
                print("\t\tHeadshot found")

                with open(destination_path, 'wb') as destination_file:
                    raw_file.raw.decode_content = True
                    copyfileobj(raw_file.raw, destination_file)
            else:
                print("\t\tNo headshot found")

            time.sleep(1.5)


if __name__ == '__main__':
    main()

