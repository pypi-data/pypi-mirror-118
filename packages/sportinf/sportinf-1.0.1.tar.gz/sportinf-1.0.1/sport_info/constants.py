"""
link_patterns is a dictionary that contains
"""
link_patterns = {
    "Information about team":
        {
            "link": "https://www.thesportsdb.com/api/v1/json/1/searchteams.php?t={parameter1}",
            "parameter1": "team_name",
            "useful parameters": ["strTeam", "strTeamShort", "strAlternate", "intFormedYear", "strSport", "strLeague",
                                  "strLeague2", "strLeague3", "strLeague4", "strLeague5", "strLeague6", "strLeague7",
                                  "strDivision", "strManager", "strStadium", "strKeywords", "strRSS", "strStadiumThumb",
                                  "strStadiumDescription", "strStadiumLocation", "intStadiumCapacity", "strWebsite",
                                  "strFacebook", "strTwitter", "strInstagram", "strDescriptionEN", "strDescriptionDE",
                                  "strDescriptionFR", "strDescriptionCN", "strDescriptionIT", "strDescriptionJP",
                                  "strDescriptionRU", "strDescriptionES", "strDescriptionPT", "strDescriptionSE",
                                  "strDescriptionNL", "strDescriptionHU", "strDescriptionNO", "strDescriptionIL",
                                  "strDescriptionPL", "strGender", "strCountry", "strTeamBadge", "strTeamJersey",
                                  "strTeamLogo", "strTeamFanart1", "strTeamFanart2", "strTeamFanart3", "strTeamFanart4",
                                  "strTeamBanner", "strYoutube"]
        },  # team name----------------------------------------
    # "strRSS", "strStadiumThumb",
    "Information about player":
        {
            "link": "https://www.thesportsdb.com/api/v1/json/1/searchplayers.php?p={parameter1}",
            "parameter1": "player_name",
            "useful parameters": ["strPlayer", "strNationality", "strTeam", "strTeam2", "strSport", "dateBorn",
                                  "strNumber", "dateSigned", "strSigning", "strWage", "strOutfitter", "strKit",
                                  "strAgent", "strBirthLocation", "strDescriptionEN", "strDescriptionDE",
                                  "strDescriptionFR", "strDescriptionCN", "strDescriptionIT", "strDescriptionJP",
                                  "strDescriptionRU", "strDescriptionES", "strDescriptionPT", "strDescriptionSE",
                                  "strDescriptionNL", "strDescriptionHU", "strDescriptionNO", "strDescriptionIL",
                                  "strDescriptionPL", "strGender", "strSide", "strPosition", "strCollege",
                                  "strFacebook", "strWebsite", "strTwitter", "strInstagram", "strYoutube", "strHeight",
                                  "strWeight", "strThumb", "strCutout", "strRender", "strBanner", "strFanart1",
                                  "strFanart2", "strFanart3", "strFanart4"]
        },  # player name----------------------------------------------------------
    "Information about event":
        {
            "link": "https://www.thesportsdb.com/api/v1/json/1/searchevents.php?e={parameter1}",
            "parameter1": "event_name",
            "useful parameters": ["dateEvent", "strEvent", "strEventAlternate", "strFilename", "strSport", "strLeague",
                                  "strSeason", "strDescriptionEN", "strHomeTeam", "strAwayTeam", "intHomeScore",
                                  "intRound", "intAwayScore", "intSpectators", "strOfficial", "strHomeGoalDetails",
                                  "strHomeRedCards", "strHomeYellowCards", "strHomeLineupGoalkeeper",
                                  "strHomeLineupDefense", "strHomeLineupMidfield", "strHomeLineupForward",
                                  "strHomeLineupSubstitutes", "strHomeFormation", "strAwayRedCards",
                                  "strAwayYellowCards", "strAwayGoalDetails", "strAwayLineupGoalkeeper",
                                  "strAwayLineupDefense", "strAwayLineupMidfield", "strAwayLineupForward",
                                  "strAwayLineupSubstitutes", "strAwayFormation", "intHomeShots", "intAwayShots",
                                  "strTimestamp", "dateEventLocal", "strTime", "strTimeLocal",
                                  "strTVStation", "strResult", "strVenue", "strCountry", "strCity", "strPoster",
                                  "strSquare", "strFanart", "strThumb", "strBanner", "strMap", "strTweet1", "strTweet2",
                                  "strTweet3", "strVideo", "strStatus", "strPostponed"]
        },  # event name
    "List all sports":
        {
            "link": "https://www.thesportsdb.com/api/v1/json/1/all_sports.php",
            "useful parameters": ["strSport", "strFormat", "strSportThumb", "strSportThumbGreen", "strSportDescription"]
        },
    "List all leagues":
        {
            "link": "https://www.thesportsdb.com/api/v1/json/1/all_leagues.php",
            "useful parameters": ["strLeague", "strSport", "strLeagueAlternate"]
        },
    "List all countries":
        {
            "link": "https://www.thesportsdb.com/api/v1/json/1/all_countries.php",
            "useful parameters": ["name_en"]
        },
    # "List all Leagues in a country": "",
    "List all Seasons in a League":
        {
            "link": "https://www.thesportsdb.com/api/v1/json/1/search_all_seasons.php?id={parameter1}",
            "parameter1": "league_name",
            "useful parameters": ["strSeason"]
        },  # league ID
    "List all Teams in a League":
        {
            "link": "https://www.thesportsdb.com/api/v1/json/1/search_all_teams.php?l={parameter1}",
            "parameter1": "league_name",
            "useful parameters": ["strTeam", "strTeamShort", "strAlternate", "intFormedYear", "strSport", "strLeague",
                                  "strLeague2", "strLeague3", "strLeague4", "strLeague5", "strLeague6", "strLeague7",
                                  "strDivision", "strManager", "strStadium", "strKeywords", "strRSS", "strStadiumThumb",
                                  "strStadiumDescription", "strStadiumLocation", "intStadiumCapacity", "strWebsite",
                                  "strFacebook", "strTwitter", "strInstagram", "strDescriptionEN", "strDescriptionDE",
                                  "strDescriptionFR", "strDescriptionCN", "strDescriptionIT", "strDescriptionJP",
                                  "strDescriptionRU", "strDescriptionES", "strDescriptionPT", "strDescriptionSE",
                                  "strDescriptionNL", "strDescriptionHU", "strDescriptionNO", "strDescriptionIL",
                                  "strDescriptionPL", "strGender", "strCountry", "strTeamBadge", "strTeamJersey",
                                  "strTeamLogo", "strTeamFanart1", "strTeamFanart2", "strTeamFanart3", "strTeamFanart4",
                                  "strTeamBanner", "strYoutube"]
        },  # league name, use for loop-------------------------------------
    "League Details":
        {
            "link": "https://www.thesportsdb.com/api/v1/json/1/lookupleague.php?id={parameter1}",
            "parameter1": "league_name",
            "useful parameters": ["strLeague", "strSport", "strLeagueAlternate", "strDivision", "strCurrentSeason",
                                  "intFormedYear", "dateFirstEvent", "strGender", "strCountry", "strWebsite",
                                  "strFacebook", "strTwitter", "strYoutube", "strRSS", "strDescriptionEN",
                                  "strDescriptionDE", "strDescriptionFR", "strDescriptionIT", "strDescriptionCN",
                                  "strDescriptionJP", "strDescriptionRU", "strDescriptionES", "strDescriptionPT",
                                  "strDescriptionSE", "strDescriptionNL", "strDescriptionHU", "strDescriptionNO",
                                  "strDescriptionPL", "strDescriptionIL", "strTvRights", "strFanart1", "strFanart2",
                                  "strFanart3", "strFanart4", "strBanner", "strBadge", "strLogo", "strPoster",
                                  "strTrophy", "strNaming"]
        },  # league ID
    "Player Honours":
        {
            "link": "https://www.thesportsdb.com/api/v1/json/1/lookuphonors.php?id={parameter1}",
            "parameter1": "player_name",
            "useful parameters": ["strHonour", "strPlayer", "strSport", "strTeam", "strSeason"]
        },  # player ID
    "Player Former Teams":
        {
            "link": "https://www.thesportsdb.com/api/v1/json/1/lookupformerteams.php?id={parameter1}",
            "parameter1": "player_name",
            "useful parameters": ["strFormerTeam", "strSport", "strPlayer", "strMoveType", "strTeamBadge", "strJoined",
                                  "strDeparted"]
        },  # player ID
    "Player Contracts":
        {
            "link": "https://www.thesportsdb.com/api/v1/json/1/lookupcontracts.php?id={parameter1}",
            "parameter1": "player_name",
            "useful parameters": ["strSport", "strPlayer", "strTeam", "strTeamBadge", "strYearStart", "strYearEnd",
                                  "strWage"]
        },  # player ID-----------------------------------------------------------------
    "Lookup Table by League and Season":
        {
            "link": "https://www.thesportsdb.com/api/v1/json/1/lookuptable.php?l={parameter1}&s={parameter2}",
            "parameter1": "league_name",
            "parameter2": "season",
            "useful parameters": ["intRank", "strTeam", "strTeamBadge", "strLeague", "strSeason", "strForm",
                                  "strDescription", "intPlayed", "intWin", "intLoss", "intDraw", "intGoalsFor",
                                  "intGoalsAgainst", "intGoalDifference", "intPoints", "dateUpdated"]
        },  # league ID and season----------------------------------------------
    "Lookup Equipment by Team":
        {
            "link": "https://www.thesportsdb.com/api/v1/json/1/lookupequipment.php?id={parameter1}",
            "parameter1": "team_name",
            "useful parameters": ["date", "strSeason", "strEquipment", "strType", "strUsername"]
        },  # team ID------------------------------------------
    "Last 15 Events by League":
        {
            "link": "https://www.thesportsdb.com/api/v1/json/1/eventspastleague.php?id={parameter1}",
            "parameter1": "league_name",
            "useful parameters": ["strEvent", "strEventAlternate", "strFilename", "strSport", "idLeague", "strLeague",
                                  "strSeason", "strDescriptionEN", "strHomeTeam", "strAwayTeam", "intHomeScore",
                                  "intRound", "intAwayScore", "intSpectators", "strOfficial", "strHomeGoalDetails",
                                  "strHomeRedCards", "strHomeYellowCards", "strHomeLineupGoalkeeper",
                                  "strHomeLineupDefense", "strHomeLineupMidfield", "strHomeLineupForward",
                                  "strHomeLineupSubstitutes", "strHomeFormation", "strAwayRedCards",
                                  "strAwayYellowCards", "strAwayGoalDetails", "strAwayLineupGoalkeeper",
                                  "strAwayLineupDefense", "strAwayLineupMidfield", "strAwayLineupForward",
                                  "strAwayLineupSubstitutes", "strAwayFormation", "intHomeShots", "intAwayShots",
                                  "strTimestamp", "dateEvent", "dateEventLocal", "strTime", "strTimeLocal",
                                  "strTVStation", "strResult", "strVenue", "strCountry", "strCity", "strPoster",
                                  "strSquare", "strFanart", "strThumb", "strBanner", "strMap", "strTweet1", "strTweet2",
                                  "strTweet3", "strVideo", "strStatus", "strPostponed"]
        }  # league ID-------------------------------------------------------------
}
"""

"""
options_need_id = ["List all Seasons in a League", "League Details", "Player Honours", "Player Former Teams",
                   "Player Contracts", "Lookup Table by League and Season", "Lookup Equipment by Team",
                   "Last 15 Events by League"]
