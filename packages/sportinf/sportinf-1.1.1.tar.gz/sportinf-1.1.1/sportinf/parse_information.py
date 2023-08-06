from constants import *
import requests
import json


class SportInfo:
    def __init__(self, **data):
        self.__data = data
        self.raw_info = self.__get_info()

    def __get_id(self):
        if self.__data["option"] in ["List all Seasons in a League", "League Details", "Lookup Table by League and Season", "Last 15 Events by League"]:
            r = requests.get("https://www.thesportsdb.com/api/v1/json/1/all_leagues.php")
            text = r.text
            leagues = json.loads(text)
            for league in leagues["leagues"]:
                if league["strLeague"] == self.__data["league_name"] or league["strLeagueAlternate"] == self.__data["league_name"]:
                    ID = league["idLeague"]
        elif self.__data["option"] in ["Player Honours", "Player Former Teams", "Player Contracts"]:  # player ID
            r = requests.get("https://www.thesportsdb.com/api/v1/json/1/searchplayers.php?p={}".format(self.__data["player_name"]))
            text = r.text
            player = json.loads(text)
            ID = player["player"][0]["idPlayer"]
        elif self.__data["option"] == "Lookup Equipment by Team":  # team ID # CHANGE HERE
            r = requests.get("https://www.thesportsdb.com/api/v1/json/1/searchteams.php?t={}".format(self.__data["team_name"]))
            text = r.text
            team = json.loads(text)
            ID = team["teams"][0]["idTeam"]
        elif self.__data["option"] == "Event Results":  # event ID =
            r = requests.get("https://www.thesportsdb.com/api/v1/json/1/searchevents.php?e={}".format(self.__data["event_name"]))
            text = r.text
            event = json.loads(text)
            ID = event["event"][0]["idEvent"]
        return ID

    def __replace_str_or_int(self, string):
        if "str" in string:
            edited_string = string.replace("str", "")
            return edited_string
        elif "int" in string:
            edited_string = string.replace("int", "")
            return edited_string
        else:
            return string

    def __get_info(self):
        link = link_patterns[self.__data["option"]]["link"]
        opt = self.__data["option"]
        if self.__data["option"] in options_need_id:
            need_id = self.__get_id()
            if self.__data["option"] == "Lookup Table by League and Season":
                name_of_second_parameter = link_patterns[opt]["parameter2"]
                param2 = self.__data[name_of_second_parameter]
                try:
                    r = requests.get(link.format(parameter1=need_id, parameter2=param2))
                except requests.ConnectionError:
                    raise Exception("Check your Internet connection")
            else:
                try:
                    r = requests.get(link.format(parameter1=need_id))
                except requests.ConnectionError:
                    raise Exception("Check your Internet connection")

        elif self.__data["option"] in ["List all sports", "List all leagues", "List all countries"]:
            try:
                r = requests.get(link)
            except requests.ConnectionError:
                raise Exception("Check your Internet connection")
        else:
            name_of_parameter = link_patterns[opt]["parameter1"]
            param1 = self.__data[name_of_parameter]
            try:
                r = requests.get(link.format(parameter1=param1))
            except requests.ConnectionError:
                raise Exception("Check your Internet connection")
        text = r.text
        info = json.loads(text)
        return info

    def __check_none_or_empty_value(self, value):
        if value is not None and value != "":
            return True
        else:
            return False

    def sport_info(self):
        useful_information = {}
        for general_value in self.raw_info.values():
            if general_value is None or general_value == "":
                raise Exception("Can`t find any information.\nPlease check your parameters")
            else:
                if len(general_value) >= 2:
                    for every_dictionary in general_value:
                        if self.__data["option"] == "Player Contracts":
                            contract_start = link_patterns[self.__data["option"]]["useful parameters"][4]
                            contract_end = link_patterns[self.__data["option"]]["useful parameters"][5]
                            unique_parameter = every_dictionary[contract_start] + " - " + every_dictionary[contract_end]
                        else:
                            name_of_unique_parameter = link_patterns[self.__data["option"]]["useful parameters"][0]
                            unique_parameter = every_dictionary[name_of_unique_parameter]
                        useful_information[unique_parameter] = {}
                        for key, value in every_dictionary.items():
                            if key in link_patterns[self.__data["option"]]["useful parameters"] and self.__check_none_or_empty_value(value):
                                useful_information[unique_parameter][self.__replace_str_or_int(key)] = value
                else:
                    for key, value in general_value[0].items():
                        if key in link_patterns[self.__data["option"]]["useful parameters"] and self.__check_none_or_empty_value(value):
                            useful_information[self.__replace_str_or_int(key)] = value
        return useful_information
