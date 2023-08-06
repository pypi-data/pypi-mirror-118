import unittest
from results import *
from sportinf.parse_information import SportInfo


class OptionsTests(unittest.TestCase):
    def test_info_team(self):
        self.maxDiff = None
        test_case = SportInfo(option="Information about team", team_name="Arsenal")
        self.assertEqual(test_case.sport_info(), result_info_team)

    def test_info_player(self):
        self.maxDiff = None
        test_case = SportInfo(option="Information about player", player_name="Lionel Messi")
        self.assertEqual(test_case.sport_info(), result_info_player)

    def test_info_event(self):
        self.maxDiff = None
        test_case = SportInfo(option="Information about event", event_name="Arsenal vs Chelsea")
        self.assertEqual(test_case.sport_info(), result_info_event)

    def test_all_sports(self):
        self.maxDiff = None
        test_case = SportInfo(option="List all sports")
        self.assertEqual(test_case.sport_info(), result_all_sports)

    def test_all_leagues(self):
        self.maxDiff = None
        test_case = SportInfo(option="List all leagues")
        self.assertEqual(test_case.sport_info(), result_all_leagues)

    def test_all_countries(self):
        self.maxDiff = None
        test_case = SportInfo(option="List all countries")
        self.assertEqual(test_case.sport_info(), result_all_countries)

    def test_all_seasons(self):
        self.maxDiff = None
        test_case = SportInfo(option="List all Seasons in a League", league_name="English Premier League")
        self.assertEqual(test_case.sport_info(), result_all_seasons)

    def test_all_teams(self):
        self.maxDiff = None
        test_case = SportInfo(option="List all Teams in a League", league_name="English Premier League")
        self.assertEqual(test_case.sport_info(), result_all_teams)

    def test_league_details(self):
        self.maxDiff = None
        test_case = SportInfo(option="League Details", league_name="English Premier League")
        self.assertEqual(test_case.sport_info(), result_league_details)

    def test_honours(self):
        self.maxDiff = None
        test_case = SportInfo(option="Player Honours", player_name="Lionel Messi")
        self.assertEqual(test_case.sport_info(), result_honours)

    def test_former_teams(self):
        self.maxDiff = None
        test_case = SportInfo(option="Player Former Teams", player_name="Lionel Messi")
        self.assertEqual(test_case.sport_info(), result_former_teams)

    def test_contracts(self):
        self.maxDiff = None
        test_case = SportInfo(option="Player Contracts", player_name="Lionel Messi")
        self.assertEqual(test_case.sport_info(), result_contracts)

    def test_table(self):
        self.maxDiff = None
        test_case = SportInfo(option="Lookup Table by League and Season", league_name="English Premier League", season="2020-2021")
        self.assertEqual(test_case.sport_info(), result_table)

    def test_equipment(self):
        self.maxDiff = None
        test_case = SportInfo(option="Lookup Equipment by Team", team_name="Arsenal")
        self.assertEqual(test_case.sport_info(), result_equipment)

    def test_15_events(self):
        self.maxDiff = None
        test_case = SportInfo(option="Last 15 Events by League", league_name="English Premier League")
        self.assertEqual(test_case.sport_info(), result_15_events)


if __name__ == '__main__':
    unittest.main()
