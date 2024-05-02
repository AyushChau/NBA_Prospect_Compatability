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
    
    return teams_df


college_stats = pd.read_csv('CollegeBasketballPlayers2022.csv')
college_stats = pd.concat([college_stats,pd.read_csv('CollegeBasketballPlayers2009-2021.csv')],axis=0)

college_stats['player_name'] = college_stats['player_name'].map(lambda x: x.upper())
college_stats.rename(columns={"Unnamed: 64":"Position"},inplace=True)
first_round_picks = GetDraftData()
#teams_yearly_stats = GetTeamStats(NBA_team_ids)

#test = first_round_picks.merge(college_stats, left_on='PLAYER_NAME', right_on='player_name')

mean_college_stats = college_stats.groupby('player_name')[['usg','Ortg','adrtg','pts','dreb','oreb','dreb','treb','ast','stl','blk','ast/tov']].mean().reset_index()
mean_college_stats = mean_college_stats.merge(college_stats[['player_name','Position']],on='player_name').drop_duplicates(['player_name'])

#teams_draft_pick_stats = teams_draft_pick.merge(college_stats,on=['TEAM_ID','SEASON']).drop(columns=['TEAM_CITY','TEAM_NAME'])









