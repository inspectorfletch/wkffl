import nflgame
import sys
import time
import datetime
import pytz
from collections import OrderedDict
from openpyxl import load_workbook
from openpyxl.styles import Font, Color
from openpyxl.styles import colors

from joblib import Parallel, delayed

year = None
week = None

position_rows = {
    "QB": [1,2],
    "RB": [4,5,6],
    "WR": [8,9,10,11],
    "TE": [13],
    "K": [16],
    "DEF": [19]
}

class PlayerStats(object):
    def __init__(self, player_cell, position):
        self.player_cell = player_cell
        player_name = self.player_cell.value

        print(self)

        player_list = nflgame.find(player_name)
        if player_list is None or len(player_list) == 0:
            print("Player not found!", player_name)
            exit(1)

        self.player_name = player_name
        self.player = None

        for p in player_list:
            if p.position != '' and p.position == position:
                self.player = p
                break

        if self.player is None:
            raise Exception(player_name + " was not found!")

        self.stats = self.player.stats(year, week=week)

        self.long_pass_tds = 0
        self.long_rush_tds = 0
        self.long_rec_tds = 0
        
        self.hookup_tds = 0
        
        self.plays = self.player.plays(year, week=week)

        if self.stats.passing_tds > 0:
            for play in self.plays:
                if play.passing_tds > 0:
                    play_stats = None
                    for p in play.players:
                        if p.playerid == self.player.playerid:
                            play_stats = p
                            break
                            
                    if play_stats.passing_tds > 0 and play_stats.passing_yds >= 40:
                        self.long_pass_tds += 1
                        
        if self.stats.rushing_tds > 0:
            for play in self.plays:
                if play.rushing_tds > 0:
                    play_stats = None
                    for p in play.players:
                        if p.playerid == self.player.playerid:
                            play_stats = p
                            break
                            
                    if play_stats.rushing_tds > 0 and play_stats.rushing_yds >= 40:
                        self.long_rush_tds += 1
                        
        if self.stats.receiving_tds > 0:
            for play in self.plays:
                if play.receiving_tds > 0:
                    play_stats = None
                    for p in play.players:
                        if p.playerid == self.player.playerid:
                            play_stats = p
                            break
                            
                    if play_stats.receiving_tds > 0 and play_stats.receiving_yds >= 40:
                        self.long_rec_tds += 1

    def find_game(self, team_name):
        official_name = nflgame.standard_team(team_name)
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

    def print_to_file(self, player_scores):
        player_scores.write(self.player_name)
        player_scores.write(',')
        player_scores.write(str(self.stats.passing_cmp))
        player_scores.write(',')
        player_scores.write(str(self.stats.passing_yds))
        player_scores.write(',')
        player_scores.write(str(self.stats.passing_tds))
        player_scores.write(',')
        player_scores.write(str(self.stats.passing_ints))
        player_scores.write(',')
        player_scores.write(str(self.long_pass_tds)) #Long passing TDs
        player_scores.write(',')
        player_scores.write(str(self.hookup_tds)) #Hookup TDs
        player_scores.write(',')
        player_scores.write(str(self.stats.rushing_att))
        player_scores.write(',')
        player_scores.write(str(self.stats.rushing_yds))
        player_scores.write(',')
        player_scores.write(str(self.stats.rushing_tds + self.stats.kickret_tds + self.stats.puntret_tds))
        player_scores.write(',')
        player_scores.write(str(self.long_rush_tds)) #Long rushing TDs
        player_scores.write(',')
        player_scores.write(str(self.stats.fumbles_lost))
        player_scores.write(',')
        player_scores.write(str(self.stats.receiving_rec))
        player_scores.write(',')
        player_scores.write(str(self.stats.receiving_yds))
        player_scores.write(',')
        player_scores.write(str(self.stats.receiving_tds))
        player_scores.write(',')
        player_scores.write(str(self.long_rec_tds)) #Long receiving TDs
        player_scores.write(',')
        player_scores.write(str(self.stats.twoptm))
        player_scores.write('\n')

    def print_value_to_spreadsheet(self, player_row, row_index, value):
        if int(value) != 0:
            player_row[row_index].value = value

    def update_cell_color(self, player_row, team_name):
        player_name_cell = player_row[0]
        official_name = nflgame.standard_team(team_name)
        game = self.find_game(official_name)
        if game is None:
            player_name_cell.font = Font(color='c2c2a3')
        elif game == '' or not (game.game_over() or game.playing()):
            player_name_cell.font = Font(color=colors.RED)
        elif game.playing():
            player_name_cell.font = Font(color=colors.GREEN)
        else:
            player_name_cell.font = Font(color=colors.BLACK)

    def print_to_spreadsheet(self, player_sheet):
        player_row = player_sheet[self.player_cell.row]

        self.update_cell_color(player_row, self.player.team)

        self.print_value_to_spreadsheet(player_row, 1, self.stats.passing_cmp)
        self.print_value_to_spreadsheet(player_row, 2, self.stats.passing_yds)
        self.print_value_to_spreadsheet(player_row, 3, self.stats.passing_tds)
        self.print_value_to_spreadsheet(player_row, 4, self.stats.passing_ints)
        self.print_value_to_spreadsheet(player_row, 5, self.long_pass_tds)
        self.print_value_to_spreadsheet(player_row, 6, self.hookup_tds)
        self.print_value_to_spreadsheet(player_row, 7, self.stats.rushing_att)
        self.print_value_to_spreadsheet(player_row, 8, self.stats.rushing_yds)
        self.print_value_to_spreadsheet(player_row, 9, self.stats.rushing_tds + self.stats.kickret_tds + self.stats.puntret_tds)
        self.print_value_to_spreadsheet(player_row, 10, self.long_rush_tds)
        self.print_value_to_spreadsheet(player_row, 11, self.stats.fumbles_lost)
        self.print_value_to_spreadsheet(player_row, 12, self.stats.receiving_rec)
        self.print_value_to_spreadsheet(player_row, 13, self.stats.receiving_yds)
        self.print_value_to_spreadsheet(player_row, 14, self.stats.receiving_tds)
        self.print_value_to_spreadsheet(player_row, 15, self.long_rec_tds)
        self.print_value_to_spreadsheet(player_row, 16, self.stats.twoptm)
        
    def __str__(self):
        return str(self.player_cell.value)

class KickerStats(PlayerStats):
    def __init__(self, player_cell, position):
        super(self.__class__, self).__init__(player_cell, position)
        
        self.fg30 = 0
        self.fg40 = 0
        self.fg50 = 0
        self.fg60 = 0
        if self.stats.kicking_fgm > 0:
            for play in self.plays:
                for p in play.players:
                    if p.kicking_fgm > 0 and  p.playerid == self.player.playerid:
                        if p.kicking_fgm_yds >= 60:
                            self.fg60 += 1
                        elif p.kicking_fgm_yds >= 50:
                            self.fg50 += 1
                        elif p.kicking_fgm_yds >= 40:
                            self.fg40 += 1
                        else:
                            self.fg30 += 1
                        break

    def print_to_file(self, player_scores):
        #super(self.__class__, self).print_to_file(player_scores)
        
        player_scores.write(",XP,0-39 FG,40-49 FG,50-59 FG,60+ FG\n")
        player_scores.write(self.player_name)
        player_scores.write(",")
        player_scores.write(str(self.stats.kicking_xpmade))
        player_scores.write(",")
        player_scores.write(str(self.fg30))
        player_scores.write(",")
        player_scores.write(str(self.fg40))
        player_scores.write(",")
        player_scores.write(str(self.fg50))
        player_scores.write(",")
        player_scores.write(str(self.fg60))
        player_scores.write('\n')
        
    def print_to_spreadsheet(self, player_sheet):
        player_row = player_sheet[self.player_cell.row]
        
        self.update_cell_color(player_row, self.player.team)
        
        self.print_value_to_spreadsheet(player_row, 1, self.stats.kicking_xpmade)
        self.print_value_to_spreadsheet(player_row, 2, self.fg30)
        self.print_value_to_spreadsheet(player_row, 3, self.fg40)
        self.print_value_to_spreadsheet(player_row, 4, self.fg50)
        self.print_value_to_spreadsheet(player_row, 5, self.fg60)
        
class DefenseStats(PlayerStats):
    def __init__(self, player_cell):
        print(player_cell.value)
    
        self.player_cell = player_cell
        self.print_name = player_cell.value
        self.official_name = nflgame.standard_team(self.print_name)
        
        self.sacks = 0
        self.int = 0
        self.fumbles_rec = 0
        self.safeties = 0
        self.dst_tds = 0
        self.two_pts = 0
        self.pts_allowed = -1

        self.game = self.find_game(self.official_name)

        if self.game is None or self.game == '' or not (self.game.playing() or self.game.game_over()):
            print('No game in progress for ' + self.print_name)
            return
        else:
            if self.game.home == self.official_name:
                self.pts_allowed = self.game.score_away
            elif self.game.away == self.official_name:
                self.pts_allowed = self.game.score_home
            else:
                raise "Team not found in game!"

        for drive in self.game.drives:
            if drive.team != self.official_name and 'Safety' in drive.result:
                self.safeties += 1
                
            for play in drive.plays:
                for event in play.events:
                    if event["team"] == self.official_name and "defense_tds" in event:
                        self.dst_tds += event["defense_tds"]
                        
                    if event["team"] == self.official_name and "defense_frec" in event:
                        self.fumbles_rec += event["defense_frec"]
        
        plays = nflgame.combine_game_stats([ self.game ])
        for play in plays:
            if play.team == self.official_name:                
                self.sacks += play.defense_sk
                self.int += play.defense_int
                
                self.dst_tds += play.kickret_tds
                self.dst_tds += play.puntret_tds

    def print_to_file(self, player_scores):
        player_scores.write(",Sacks,INT,FR,SFT,TD,Shutout,0-6,7-13.,14-19,20-29,30-39,40-49,50+\n")
        player_scores.write(self.print_name)
        player_scores.write(",")
        player_scores.write(str(self.sacks))
        player_scores.write(",")
        player_scores.write(str(self.int))
        player_scores.write(",")
        player_scores.write(str(self.fumbles_rec))
        player_scores.write(",")
        player_scores.write(str(self.safeties))
        player_scores.write(",")
        player_scores.write(str(self.dst_tds))
        player_scores.write(",")
        
        if (self.pts_allowed == 0):
            player_scores.write(str("1"))
        player_scores.write(str(","))
        
        if (self.pts_allowed > 0 and self.pts_allowed <= 6):
            player_scores.write(str("1"))
        player_scores.write(str(","))
        
        if (self.pts_allowed > 6 and self.pts_allowed <= 13):
            player_scores.write(str("1"))
        player_scores.write(str(","))
    
        if (self.pts_allowed > 13 and self.pts_allowed <= 19):
            player_scores.write(str("1"))
        player_scores.write(str(","))
            
        if (self.pts_allowed > 19 and self.pts_allowed <= 29):
            player_scores.write(str("1"))
        player_scores.write(str(","))
        
        if (self.pts_allowed > 29 and self.pts_allowed <= 39):
            player_scores.write(str("1"))
        player_scores.write(str(","))
        
        if (self.pts_allowed > 39 and self.pts_allowed <= 49):
            player_scores.write(str("1"))
        player_scores.write(str(","))
        
        if (self.pts_allowed >= 50):
            player_score.write("1")
        
        player_scores.write('\n')
        
    def print_to_spreadsheet(self, player_sheet):
        player_row = player_sheet[self.player_cell.row]

        self.update_cell_color(player_row, self.print_name)

        self.print_value_to_spreadsheet(player_row, 1, self.sacks)
        self.print_value_to_spreadsheet(player_row, 2, self.int)
        self.print_value_to_spreadsheet(player_row, 3, self.fumbles_rec)
        self.print_value_to_spreadsheet(player_row, 4, self.safeties)
        self.print_value_to_spreadsheet(player_row, 5, self.dst_tds)
        
        if self.game is not None and self.game != '' and (self.game.playing() or self.game.game_over()):
            if (self.pts_allowed == 0):
                self.print_value_to_spreadsheet(player_row, 6, 1)
            elif (self.pts_allowed > 0 and self.pts_allowed <= 6):
                self.print_value_to_spreadsheet(player_row, 7, 1)
            elif (self.pts_allowed > 6 and self.pts_allowed <= 13):
                self.print_value_to_spreadsheet(player_row, 8, 1)
            elif (self.pts_allowed > 13 and self.pts_allowed <= 19):
                self.print_value_to_spreadsheet(player_row, 9, 1)
            elif (self.pts_allowed > 19 and self.pts_allowed <= 29):
                self.print_value_to_spreadsheet(player_row, 10, 1)
            elif (self.pts_allowed > 29 and self.pts_allowed <= 39):
                self.print_value_to_spreadsheet(player_row, 11, 1)
            elif (self.pts_allowed > 39 and self.pts_allowed <= 49):
                self.print_value_to_spreadsheet(player_row, 12, 1)
            elif (self.pts_allowed >= 50):
                self.print_value_to_spreadsheet(player_row, 13, 1)

class Team:
    def __init__(self, team_name, player_columns):
        self.team_name = team_name
        self.player_columns = []
        self.player_index = OrderedDict()
        
        for player_cell, position in player_columns:
            self.player_columns.append(player_cell)

            if position == "DEF":
                defense = DefenseStats(player_cell)
                self.player_index[0] = defense
            elif position == "K":
                kicker = KickerStats(player_cell, position)
                self.player_index[kicker.player.playerid] = kicker
            else:
                player = PlayerStats(player_cell, position)
                self.player_index[player.player.playerid] = player

        for playerid, player in self.player_index.items():
            if not isinstance(player, DefenseStats) and player.stats.receiving_tds > 0:
                for play in player.plays:
                    if play.receiving_tds > 0:
                        play_stats = None
                        for p in play.players:
                            if p.passing_tds > 0 and p.playerid != playerid and p.playerid in self.player_index.keys():
                                player.hookup_tds += 1
                                self.player_index[p.playerid].hookup_tds += 1
                                break

    def print_players(self, player_scores):
        for index, player in enumerate(self.player_index.values()):
            player.print_to_file(player_scores)
            
            if index == 1 or index == 4 or index == 8 or index == 9 or index == 10:
                player_scores.write("\n")
                
    def print_to_spreadsheet(self, roster_book):
        team_sheet = roster_book[self.team_name]
        
        for row_num, player_cell in enumerate(self.player_columns):
            if row_num != 14 and row_num != 17:
                player_row = team_sheet[player_cell.row]
                for col in range(1, 17):
                    player_row[col].value = None
        
        for player in self.player_index.values():
            player.print_to_spreadsheet(team_sheet)

def calculate_scores(team_name, team_col):
    print("****" + team_name + "****")

    players = []
    for position in position_rows:
        for row_num in position_rows[position]:
            if team_col[row_num].value is not None:
                players.append((team_col[row_num], position))

    team = Team(team_name, players)
    return team

if __name__ == '__main__':
    
    team_names = set(['Don', 'Dean', 'Joe', 'Marc', 'Josh', 'Michael', 'Pat', 'Nick'])
    filename = 'Rosters.xlsx'
    #team_names = set(['Joe'])
    #if len(sys.argv) > 1:
    #    if sys.argv[1] == '-co':
    #        team_names = set(['Marc', 'Josh'])
    #        filename = 'Rosters_autoScored.xlsx'

    if (len(sys.argv) == 3):
        year = int(sys.argv[1])
        week = int(sys.argv[2])
    else:
        (year, week) = nflgame.live.current_year_and_week()

    print("Scores for {0} Week {1}".format(str(year), str(week)))

    roster_book = load_workbook('C:\\Users\\joshw\\OneDrive\\WKFFL\\\\' + filename)
    roster_sheet = roster_book['Cap']
    sheet_ranges = {
        'Don': roster_sheet['B'],
        'Dean': roster_sheet['D'],
        'Joe': roster_sheet['F'],
        'Marc': roster_sheet['H'],
        'Josh': roster_sheet['J'],
        'Michael': roster_sheet['L'],
        'Pat': roster_sheet['N'],
        'Nick': roster_sheet['P'],
    }
    
    teams = Parallel(n_jobs=2, backend="threading")(delayed(calculate_scores)(team_name, team_col) for team_name, team_col in sheet_ranges.items() if team_name in team_names)
    #teams = [calculate_scores(team_name, team_col) for team_name, team_col in sheet_ranges.items() if team_name in team_names]

    for team in teams:
        team.print_to_spreadsheet(roster_book)

    now_time = datetime.datetime.now()
    eastern = pytz.timezone('US/Eastern')
    time_format_string = 'Last updated: %I:%M %p %a %b %d %Y EST'
    #if len(team_names) == 2:
    #    time_value += ' (Championship Only)'
    
    roster_book['Cap']['A29'].value = pytz.utc.localize(now_time).astimezone(eastern).strftime(time_format_string)
    roster_book.save('C:\\Users\\joshw\\OneDrive\\WKFFL\\Rosters_autoScored.xlsx')

