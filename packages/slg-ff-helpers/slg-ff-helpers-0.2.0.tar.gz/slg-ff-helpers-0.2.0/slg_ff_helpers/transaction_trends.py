import re
from bs4 import BeautifulSoup
from slg_utilities import Scraper, FileOperations
import subprocess


def get_transaction_trends_html(league_id=139692):
    s = Scraper()
    return s.get_html(f'https://football.fantasysports.yahoo.com/f1/buzzindex')

def parse_row(row):
    # only for use with transaction trend table
    columns = row.select('td')
    player = columns[0].text.replace('New Player Note', '').replace('Player Note', '').replace('No new player Notes', '').replace('\n', '').split('-')[0].strip()
    position = columns[0].text.replace('New Player Note', '').replace('Player Note', '').replace('No new player Notes', '').replace('\n', '').split('-')[1].strip().split(' ')[0]
    return {
        'Player': player,
        'Position': position,
        'Drops': int(columns[1].text),
        'Adds': int(columns[2].text),
        'Trades': int(columns[3].text),
        'Total': int(columns[4].text),
    }

def testing():
    html = get_transaction_trends_html()
    soup = BeautifulSoup(html, features="html.parser")
    rows = soup.select('tr')[1:]
    for row in rows:
        row_data = parse_row(row)
        print(row_data['Position'])
    return rows


def requirements_met(requirement_dict, *input_variables) -> bool:
    # could be refactored to just be a list, but having it in json format where you can specify the description as the key and the lambda as the value makes sense
    # requirement_dict should be of the form {label: lambda (<pertinent_variable>): <requirement statement>
    for requirement_lambda in requirement_dict.values():
        if not requirement_lambda(*input_variables): # if false then stop
            return False
    return True


def main(
    add_threshold=100,
    ignore_positions='',
):
    fo = FileOperations(start_home=True)
    add_threshold = int(add_threshold)
    ignore_positions = [item.strip().lower() for item in ignore_positions.split(',')]

    REQUIREMENTS = {
        'Player adds exceed threshold': lambda row_data: int(row_data['Adds']) > add_threshold,
        'Player not in ignore position': lambda row_data: row_data['Position'].lower() not in ignore_positions
    }

    html = get_transaction_trends_html()
    soup = BeautifulSoup(html, features="html.parser")
    rows = soup.select('tr')[1:]

    for row in rows:
        row_data = parse_row(row)
        if requirements_met(REQUIREMENTS, row_data):
            result = fo.update_json_if_time_elapsed('ff-player-adds.json', row_data['Player'])
            if result:
                # send text message
                subprocess.run(f"slg-send-text-message -m \"{row_data['Player']}\"", shell=True)

if __name__ == "__main__":
    main()
