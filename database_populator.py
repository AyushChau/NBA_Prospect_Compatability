import nba_api.stats.endpoints as nba
import pandas as pd


NBA_team_ids = [1610612759, 1610612765, 1610612753, 1610612754, 1610612749, 1610612750,
 1610612742, 1610612740, 1610612751, 1610612756, 1610612755, 1610612766,
 1610612738, 1610612739, 1610612748, 1610612764, 1610612746, 1610612758,
 1610612741, 1610612757, 1610612760, 1610612761, 1610612737, 1610612752,
 1610612745, 1610612744, 1610612747, 1610612743, 1610612762]

drafts = nba.DraftHistory()
team_stats = nba.TeamYearByYearStats(team_id= NBA_team_ids)

draft_df = pd.DataFrame(drafts.get_data_frames()[0])
teams_df = pd.DataFrame(team_stats.get_data_frames()[0])

for ids in NBA_team_ids[1:]:
    team_stats = nba.TeamYearByYearStats(team_id= ids)
    teams_df = pd.DataFrame(team_stats.get_data_frames()[0])
    print(ids,teams_df)


draft_df['TEAM'] = draft_df['TEAM_CITY'] + ' ' + draft_df['TEAM_NAME']

first_round_only = draft_df[draft_df['ROUND_PICK'] == 1]


first_round_only = first_round_only[['PERSON_ID','PLAYER_NAME','SEASON','OVERALL_PICK','TEAM_ID','TEAM']]

# print(teams_df)










