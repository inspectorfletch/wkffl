import nflapi
from nflapi import NFL
from nflstatswrapper.nflstatswrapper import nflstatswrapper

class objectview(object):
    def __init__(self, d):
        self.__dict__ = d

class nflapiplayer():
    def __init__(self, player_dict, scoring_plays):
        self.playerid = player_dict["node"]["player"]['person']['id']
        self.player_name = player_dict["node"]["player"]['person']['displayName']
        #print(self.player_name)
        self.player_team = player_dict["node"]["player"]['currentTeam']['abbreviation']
        self.player_position = player_dict["node"]["player"]['position']

        self._stats = nflapiplayerstats(player_dict["node"]["gameStats"])
        self._plays = self.__get_plays(scoring_plays)

    def stats(self, year, week):
        return self._stats

    def plays(self, year, week):
        return self._plays

    def __get_plays(self, scoring_plays):
        player_scoring_plays = []

        if self.playerid in scoring_plays:
            for scoring_play in scoring_plays[self.playerid]:
                player_scoring_plays.append(nflapiplayerplay(scoring_play))

        return player_scoring_plays

class nflapiplayerplay():
    def __init__(self, scoring_play):
        self.players = []
        self.passing_tds = 0
        self.passing_yds = 0
        self.rushing_tds = 0
        self.rushing_yds = 0
        self.receiving_tds = 0
        self.receiving_yds = 0

        for playStat in scoring_play['playStats']:
            if 'gsisPlayer' in playStat and playStat['gsisPlayer'] is not None and 'person' in playStat['gsisPlayer'] and playStat['gsisPlayer']['person'] is not None and 'id' in playStat['gsisPlayer']['person']:
                if 'statId' in playStat:
                    playerplay = nflapiplayerplay.nflapiplayerplayplayer(playStat)
                    self.players.append(playerplay)

        for p in self.players:
            self.passing_tds += p.passing_tds
            self.passing_yds = p.passing_yds
            self.rushing_tds = p.rushing_tds
            self.rushing_yds = p.rushing_yds
            self.receiving_tds = p.receiving_tds
            self.receiving_yds = p.receiving_yds

    class stattype():
        def __init__(self):
            pass

        passing_td = [16, 18]
        rushing_td = [11, 13]
        receiving_td = [22, 24]

    class nflapiplayerplayplayer():
        def __init__(self, playStat):
            self.playerid = None
            self.passing_tds = 0
            self.passing_yds = 0
            self.rushing_tds = 0
            self.rushing_yds = 0
            self.receiving_tds = 0
            self.receiving_yds = 0

            if 'gsisPlayer' in playStat and playStat['gsisPlayer'] is not None and 'person' in playStat['gsisPlayer'] and playStat['gsisPlayer']['person'] is not None and 'id' in playStat['gsisPlayer']['person']:
                self.playerid = playStat['gsisPlayer']['person']['id']

            if 'statId' in playStat:
                statId = playStat['statId']
                if statId in nflapiplayerplay.stattype.passing_td:
                    self.passing_tds = 1
                    self.passing_yds = playStat['yards']

                if statId in nflapiplayerplay.stattype.rushing_td:
                    self.rushing_tds = 1
                    self.rushing_yds = playStat['yards']

                if statId in nflapiplayerplay.stattype.receiving_td:
                    self.receiving_tds = 1
                    self.receiving_yds = playStat['yards']

class nflapiplayerstats():
    def get_value(self, stats_dict, name):
        if (stats_dict[name] is None):
            return 0

        return stats_dict[name]

    def __init__(self, stats_dict):
        self.passing_cmp = self.get_value(stats_dict, "passingCompletions")
        self.passing_yds = self.get_value(stats_dict, "passingYards")
        self.passing_tds = self.get_value(stats_dict, "passingTouchdowns")
        self.passing_ints = self.get_value(stats_dict, "passingInterceptions")

        self.rushing_att = self.get_value(stats_dict, "rushingAttempts")
        self.rushing_yds = self.get_value(stats_dict, "rushingYards")
        self.rushing_tds = self.get_value(stats_dict, "rushingTouchdowns")

        self.fumbles_lost = self.get_value(stats_dict, "fumblesLost")

        self.receiving_rec = self.get_value(stats_dict, "receivingReceptions")
        self.receiving_yds = self.get_value(stats_dict, "receivingYards")
        self.receiving_tds = self.get_value(stats_dict, "receivingTouchdowns")

        self.kickret_tds = self.get_value(stats_dict, "touchdownsDefense") + self.get_value(stats_dict, 'kickReturnsTouchdowns') + self.get_value(stats_dict, 'puntReturnsTouchdowns')

class nflapistatswrapper(nflstatswrapper):
    def __init__(self, at):
        super().__init__()
        self.nfl = NFL(ua='wkffl')#, auth=at)

        (year, week) = self.current_year_and_week()
        print (year, week)
        games_obj = self.nfl.game.week_games(week)
        print(games_obj)
        self.games_dict = {}
        self.games_list = []

        self.scoringPlaysByPlayer = {}
        for game_obj in games_obj:
            team1 = game_obj['home_team']['abbreviation']
            team2 = game_obj['away_team']['abbreviation']

            print("Loading: " + team1 + " vs " + team2)

            gameId = game_obj['id']
            game = self.nfl.game.by_id(gameId)

            gameDetailId = game.game_detail_id
            if (gameDetailId is not None):
                gameDetails = self.nfl.game_detail.by_id(gameDetailId)

                scoringPlays = [scoringPlay for scoringPlay in gameDetails.plays if scoringPlay.scoring_play]
                for scoringPlay in scoringPlays:
                    for playStat in scoringPlay['play_stats']:
                        if 'gsisPlayer' in playStat and playStat['gsisPlayer'] is not None and 'person' in playStat['gsisPlayer'] and playStat['gsisPlayer']['person'] is not None and 'id' in playStat['gsisPlayer']['person']:
                            scoringPlayPlayerId = playStat['gsisPlayer']['person']['id']
                            if not scoringPlayPlayerId in self.scoringPlaysByPlayer:
                                self.scoringPlaysByPlayer[scoringPlayPlayerId] = []

                            self.scoringPlaysByPlayer[scoringPlayPlayerId].append(scoringPlay)

            self.games_list.append(game_obj)
            self.games_dict[team1] = game_obj
            self.games_dict[team2] = game_obj

        print(self.games_list)
        self.player_dict = {}
        for game in self.games_list:
            playerGameStats = self.nfl.endpoint.session.playerGameStats(game['id'])

            for player_obj in playerGameStats['data']['viewer']['playerGameStats']['edges']:
                player = nflapiplayer(player_obj, self.scoringPlaysByPlayer)
                self.player_dict[player.player_name] = player

        print(self.player_dict)

    def find_player(self, name, position):
        return self.player_dict[name]

    def find_game(self, team_name, year, week):
        pass

    def current_year_and_week(self):
        weekInfo = self.nfl.schedule.current_week()
        #weekInfo = self.api_session.currentWeek()
        return (2020, 15)
        #return (weekInfo.season_value, weekInfo.week_value)

    def get_standard_team_name(self, team_name):
        pass

    def get_team_plays(self, game):
        pass
