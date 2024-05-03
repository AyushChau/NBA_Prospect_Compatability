import nba_api.stats.endpoints as nba
import pandas as pd

# Using Team Id's as it's not affected by Team rebranding (i.e. SuperSoncis -> Thunder)
NBA_team_ids = [1610612759, 1610612765, 1610612753, 1610612754, 1610612749, 1610612750,
 1610612742, 1610612740, 1610612751, 1610612756, 1610612755, 1610612766,
 1610612738, 1610612739, 1610612748, 1610612764, 1610612746, 1610612758,
 1610612741, 1610612757, 1610612760, 1610612761, 1610612737, 1610612752,
 1610612745, 1610612744, 1610612747, 1610612743, 1610612762]

# Used to get Historical Draft data from nba_api
def GetDraftData():
    global Colleges
    drafts = nba.DraftHistory()
    draft_df = pd.DataFrame(drafts.get_data_frames()[0])
    draft_df['TEAM'] = draft_df['TEAM_CITY'] + ' ' + draft_df['TEAM_NAME']
    draft_df_frp = draft_df[(draft_df['OVERALL_PICK'] <= 30) & (draft_df['OVERALL_PICK'] > 0) & (draft_df['SEASON'] == '2023')]
    
    return draft_df_frp[['PERSON_ID','PLAYER_NAME','SEASON','OVERALL_PICK','TEAM_ID','TEAM']]


# Used to get Team stats per year (which will be useful in deciding what the team needs are)
def GetTeamStats(NBA_team_ids):
    team_stats = nba.TeamYearByYearStats(team_id= NBA_team_ids)
    teams_df = pd.DataFrame(team_stats.get_data_frames()[0])

    for id in NBA_team_ids[1:]:
        team_stats = nba.TeamYearByYearStats(team_id= id)
        team_df = pd.DataFrame(team_stats.get_data_frames()[0])
        teams_df = pd.concat([teams_df,team_df],axis=0)

    teams_df['SEASON'] = teams_df['YEAR'].map(lambda x: x.split('-')[0]) # This is used to decide the Draft Season and correlate it to the stats

    teams_df = teams_df[(teams_df['SEASON'] == '2023') | (teams_df['SEASON'] == '2022')]
    return teams_df


def GetPlayerRookieStats(picks):
    rookie_stats = nba.PlayerCareerStats(player_id=picks)
    rookie_stats_df = pd.DataFrame(rookie_stats.get_data_frames()[0])
    rookie_stats_df = rookie_stats_df[['PLAYER_ID','GP','GS','MIN','FGM','FGA','FG_PCT','FG3M','FG3A','FG3_PCT','FTM','FTA','FT_PCT','OREB','DREB','AST','STL','BLK','TOV','PTS']]
    rookie_stats_df = rookie_stats_df.head(1)

    for pick in picks[1:]:
        rookie_stats = nba.PlayerCareerStats(player_id=pick)
        stats_df = pd.DataFrame(rookie_stats.get_data_frames()[0])
        stats_df = stats_df[['PLAYER_ID','GP','GS','MIN','FGM','FGA','FG_PCT','FG3M','FG3A','FG3_PCT','FTM','FTA','FT_PCT','OREB','DREB','AST','STL','BLK','TOV','PTS']]
        stats_df = stats_df.head(1)
        # print(stats_df)
        rookie_stats_df = pd.concat([rookie_stats_df,stats_df],axis=0)

    return rookie_stats_df


def GetYearlyChange(teams_yearly_stats):
    changes = teams_yearly_stats.groupby('TEAM_ID')[['WINS','FGM','FGA','FG_PCT','FG3M','FG3A','FG3_PCT','FTM','FTA','FT_PCT','OREB','DREB','REB','AST','PTS','STL','BLK','TOV']].diff()

    changes.columns = ['Team_' + col + '_change' for col in changes.columns]
    teams_stat_changes = pd.concat([teams_yearly_stats, changes], axis=1).dropna()
    return teams_stat_changes[['TEAM_ID','SEASON','Team_WINS_change','Team_FGM_change','Team_FGA_change','Team_FG_PCT_change','Team_FG3M_change','Team_FG3A_change','Team_FG3_PCT_change','Team_FTM_change','Team_FTA_change','Team_FT_PCT_change','Team_OREB_change','Team_DREB_change','Team_REB_change','Team_AST_change','Team_PTS_change','Team_STL_change','Team_BLK_change','Team_TOV_change']]


#Draft Picts
first_round_picks = GetDraftData()
first_round_picks['PLAYER_NAME'] = first_round_picks['PLAYER_NAME'].map(lambda x: x.upper())


#Rookie season stats for draft pick

rookie_season_stats = GetPlayerRookieStats(list(first_round_picks['PERSON_ID'].unique()))

frp_season_stats = first_round_picks.merge(rookie_season_stats, left_on='PERSON_ID', right_on='PLAYER_ID').drop('PLAYER_ID',axis=1)



#Team Stats changes after draft pick
teams_yearly_stats = GetTeamStats(NBA_team_ids)


teams_stat_changes = GetYearlyChange(teams_yearly_stats)

draft_pick_impact = frp_season_stats.merge(teams_stat_changes,on=['SEASON','TEAM_ID'])

print(draft_pick_impact)








