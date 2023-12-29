from nflstatswrapper.nflstatswrapper import nflstatswrapper
import nflgame

class objectview(object):
    def __init__(self, d):
        self.__dict__ = d

class nflgamestatswrapper(nflstatswrapper):
    def find_player(self, name, position):
        player = None

        player_list = nflgame.find(name)
        if player_list is not None and len(player_list) > 0:
            for p in player_list:
                if p.position != '' and p.position == position:
                    player = p
                    break

        if player is None:
            p = {}
            p['gsis_id'] = 0
            return nflgame.player.Player(p)
            #raise Exception(name + " (" + position + ")" + " was not found!")

        return player

    def find_game(self, team_name, year, week):
        official_name = self.get_standard_team_name(team_name)
        game = None

        try:
            games = nflgame.games(year, week=week, away=official_name)
            if (len(games) > 0):
                game = games[0]
            else:
                game = ''
        except:
            pass
        
        try:
            games = nflgame.games(year, week=week, home=official_name)
            if (len(games) > 0):
                game = games[0]
            else:
                game = ''
        except:
            pass
                
        return game

    def get_game_plays(self, game): 
        return nflgame.combine_game_stats([ game ])

    def get_standard_team_name(self, team_name):
        return nflgame.standard_team(team_name)

    def current_year_and_week(self):
        return (2020, 15)#nflgame.live.current_year_and_week()