import nba_api.stats.endpoints as nba
import pandas as pd

# Using Team Id's as it's not affected by Team rebranding (i.e. SuperSoncis -> Thunder)
NBA_team_ids = [1610612759, 1610612765, 1610612753, 1610612754, 1610612749, 1610612750,
 1610612742, 1610612740, 1610612751, 1610612756, 1610612755, 1610612766,
 1610612738, 1610612739, 1610612748, 1610612764, 1610612746, 1610612758,
 1610612741, 1610612757, 1610612760, 1610612761, 1610612737, 1610612752,
 1610612745, 1610612744, 1610612747, 1610612743, 1610612762]
Colleges = None

# Used to get Historical Draft data from nba_api
def GetDraftData():
    global Colleges
    drafts = nba.DraftHistory()
    draft_df = pd.DataFrame(drafts.get_data_frames()[0])
    draft_df['TEAM'] = draft_df['TEAM_CITY'] + ' ' + draft_df['TEAM_NAME']
    draft_df_frp = draft_df[(draft_df['OVERALL_PICK'] <= 30) & (draft_df['OVERALL_PICK'] > 0)]
    return draft_df_frp[['PERSON_ID','PLAYER_NAME','SEASON','OVERALL_PICK','TEAM_ID','TEAM']]



# Used to get Team stats per year (which will be useful in deciding what the team needs are)
def GetTeamStats(NBA_team_ids):
    team_stats = nba.TeamYearByYearStats(team_id= NBA_team_ids)
    teams_df = pd.DataFrame(team_stats.get_data_frames()[0])

    for id in NBA_team_ids[1:]:
        team_stats = nba.TeamYearByYearStats(team_id= id)
        team_df = pd.DataFrame(team_stats.get_data_frames()[0])
        teams_df = pd.concat([teams_df,team_df],axis=0)

    teams_df['SEASON'] = teams_df['YEAR'].map(lambda x: x.split('-')[0][:2] + x.split('-')[1]) # This is used to decide the Draft Season and correlate it to the stats
    teams_df['DRAFTED_SEASON'] = teams_df['YEAR'].map(lambda x: str(int(x.split('-')[0][:2] + x.split('-')[1]) - 1))
    return teams_df


#Player college stats
# college_stats = pd.read_csv('CollegeBasketballPlayers2022.csv')
# college_stats = pd.concat([college_stats,pd.read_csv('CollegeBasketballPlayers2009-2021.csv')],axis=0)
# college_stats['player_name'] = college_stats['player_name'].map(lambda x: x.upper())
# college_stats.rename(columns={"Unnamed: 64":"Position"},inplace=True)
# mean_college_stats = college_stats.groupby('player_name')[['usg','Ortg','adrtg','pts','dreb','oreb','dreb','treb','ast','stl','blk','ast/tov']].mean().reset_index()
# mean_college_stats = mean_college_stats.merge(college_stats[['player_name','Position']],on='player_name').drop_duplicates(['player_name'])


#Draft Picts
first_round_picks = GetDraftData()
first_round_picks['PLAYER_NAME'] = first_round_picks['PLAYER_NAME'].map(lambda x: x.upper())


#Team Stats in previous year
#teams_yearly_stats = GetTeamStats(NBA_team_ids)
#print(teams_yearly_stats[teams_yearly_stats['DRAFTED_SEASON'] == '2023'])
#teams_yearly_stats = teams_yearly_stats[['TEAM_ID','SEASON','DRAFTED_SEASON','WINS','LOSSES','WIN_PCT','FGM','FGA','FG_PCT','FG3M','FG3A','FG3_PCT','FT_PCT','OREB','DREB','REB','AST','PF','STL','TOV','BLK','PTS','PTS_RANK']]

test = nba.PlayerCareerStats(player_id=77869)
test_db = pd.DataFrame(test.get_data_frames()[0])

print(test_db.columns)
#frp_college_stats = first_round_picks.merge(mean_college_stats, left_on='PLAYER_NAME', right_on='player_name')


#teams_draft_pick_stats = first_round_picks.merge(teams_yearly_stats,on=['SEASON','TEAM_ID'])


#print(frp_college_stats[['PLAYER_NAME','pts']])

#print(teams_draft_pick_stats[teams_draft_pick_stats['STL'] > 0])








