import pandas as pd
import requests

def roster(league_info):

    start_team_id = league_info['roster_start']
    end_team_id = league_info['roster_end']

    roster_info = {}
    for team_id in range(start_team_id, end_team_id+1):
        url = 'https://lscluster.hockeytech.com/feed/?feed=modulekit&view=roster&key={key}&fmt=json&client_code={league}&lang=en&season_id={season}&team_id={team_id}&fmt=json'.format(
            team_id = team_id, key = league_info['key'], season = league_info['season'], league = league_info['league'])
        print(team_id)
        response = requests.get(url)
        
        fjson = response.json()
        player_data = fjson['SiteKit']['Roster']

        if len(player_data) > 0:
            for player in range(0, len(player_data)-1):
                roster_info[player_data[player]['player_id']] = {
                'first_name':player_data[player]['first_name'],
                'last_name':player_data[player]['last_name'],
                'birthdate':player_data[player]['birthdate'],
                'birthdate_year':player_data[player]['birthdate_year']}

    roster_df = pd.DataFrame(roster_info).T.reset_index().rename(columns={'index' : 'player_id'})

    roster_df['birthdate'] = pd.to_datetime(roster_df['birthdate'])
    roster_df['birthdate_year'] = '20' + roster_df['birthdate_year'].str[1:]
    roster_df['player_id'] = roster_df['player_id'].astype(str)

    return roster_df