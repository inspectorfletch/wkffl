import nflgame
from PlayerSource import PlayerSourceFactory, PlayerSource, NflGamePlayerSource

from openpyxl.styles import Font, Color
from openpyxl.styles import colors

class PlayerStats(object):
    def __init__(self, player_cell, position, year, week):
        print (player_cell.value)

        self.player_cell = player_cell
        self.player_name = self.player_cell.value

        playerSource = PlayerSourceFactory.create()
        self.player = playerSource.find(self.player_name, position)

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

    def find_game(self, team_name, year, week):
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

    def update_cell_color(self, player_row, team_name, year, week):
        player_name_cell = player_row[0]
        official_name = nflgame.standard_team(team_name)
        game = self.find_game(official_name, year, week)
        if game is None:
            player_name_cell.font = Font(color='c2c2a3')
        elif game == '' or not (game.game_over() or game.playing()):
            player_name_cell.font = Font(color=colors.RED)
        elif game.playing():
            player_name_cell.font = Font(color=colors.GREEN)
        else:
            player_name_cell.font = Font(color=colors.BLACK)

    def print_to_spreadsheet(self, player_sheet, year, week):
        player_row = player_sheet[self.player_cell.row]

        self.update_cell_color(player_row, self.player.team, year, week)

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