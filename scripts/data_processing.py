def calculate_possession():
    possesion_dict = {}
    for i, row in minutes_played_df.iterrows():
        player_id, team_id, match_id = row["playerId"], row["teamId"], row["matchId"]

        if not str(player_id) in possesion_dict.keys():
            possesion_dict[str(player_id)] = {"team_passes" : 0, "all_passes" : 0}
        
        min_in = row["player_in_min"] * 60
        min_out = row["player_out_min"] * 60

        match_df = df.loc[df["matchId"] == match_id].copy()
        match_df.loc[match_df["matchPeriod"] == "2H", 'eventSec'] = match_df.loc[match_df["matchPeriod"] == "2H", 'eventSec'] + match_df.loc[match_df["matchPeriod"] == "1H"]["eventSec"].iloc[-1]
        
        player_in_match_df = match_df.loc[match_df["eventSec"] > min_in].loc[match_df["eventSec"] <= min_out]

        all_passes = player_in_match_df.loc[player_in_match_df["eventName"].isin(["Pass", "Duel"])]

        if len(all_passes) > 0:
            no_contact = all_passes.loc[all_passes["subEventName"].isin(["Air duel", "Ground defending duel","Ground loose ball duel"])].loc[all_passes.apply(lambda x:{'id':701} in x.tags, axis = 1)]
            all_passes = all_passes.drop(no_contact.index)

        team_passes = all_passes.loc[all_passes["teamId"] == team_id]
        possesion_dict[str(player_id)]["team_passes"] += len(team_passes)
        possesion_dict[str(player_id)]["all_passes"] += len(all_passes)

    return possesion_dict