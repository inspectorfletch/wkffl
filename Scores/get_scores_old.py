import nflgame
import sys

year = 2016
week = 3

class PlayerStats(object):
	def __init__(self, player_name):
		player_list = nflgame.find(player_name)
		if player_list is None or len(player_list) == 0:
			print "Player not found!", player_name
			exit(1)
			
		self.player_name = player_name
		self.player = player_list[0]
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

class KickerStats(PlayerStats):
	def __init__(self, player_name):
		super(self.__class__, self).__init__(player_name)
		
		self.fg30 = 0
		self.fg40 = 0
		self.fg50 = 0
		self.fg60 = 0
		if self.stats.kicking_fgm > 0:
			for play in self.plays:
				for p in play.players:
					if p.kicking_fgm > 0 and  p.playerid == self.player.playerid:
						if p.kicking_fgm_yds > 60:
							self.fg60 += 1
						elif p.kicking_fgm_yds > 50:
							self.fg50 += 1
						elif p.kicking_fgm_yds > 40:
							self.fg40 += 1
						else:
							self.fg30 += 1
						break

	def print_to_file(self, player_scores):
		super(self.__class__, self).print_to_file(player_scores)
		
		player_scores.write(",XP,0-39 FG,40-49 FG,50-59 FG,60+ FG\n")
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
		
class DefenseStats(PlayerStats):
	def __init__(self, player_name):
	
		self.print_name = player_name
		self.official_name = nflgame.standard_team(player_name)
		
		self.sacks = 0
		self.int = 0
		self.fumbles_rec = 0
		self.safeties = 0
		self.dst_tds = 0
		self.two_pts = 0
		self.pts_allowed = 0
		
		games = None
		
		try:
			games = nflgame.games(year, week=week, away=self.official_name)
			self.pts_allowed = games[0].pts_home
		except:
			games = nflgame.games(year, week=week, home=self.official_name)
			self.pts_allowed = games[0].pts_away
		
		for drive in game.drives:
			if drive.team != self.official_name and drive.result == u'Safety':
				self.safeties += 1
		
		plays = nflgame.combine_game_stats(games)
		for play in plays:
			if play.team == self.official_name:
				self.sacks += play.defense_sk
				self.int += play.defense_int
				self.fumbles_rec += play.fumbles_rcv
				self.dst_tds += play.kickret_tds + play.puntret_tds + 
		
	def print_to_file(self, player_scores):
		pass
		
class Team:
	def __init__(self, players, player_scores):
		self.player_names = players[:10]
		
		player_index = OrderedDict()
		
		for player_name in self.player_names:
			player = PlayerStats(player_name)
			player_index[player.player.playerid] = player
			
		kicker = KickerStats(players[10])
		player_index[kicker.player.playerid] = kicker
		
		defense = DefenseStats(players[11])
		player_index[0] = defense
			
		for playerid, player in player_index.iteritems():
			if not isinstance(player, DefenseStats) and player.stats.receiving_tds > 0:
				for play in player.plays:
					if play.receiving_tds > 0:
						play_stats = None
						for p in play.players:
							if p.passing_tds > 0 and p.playerid != playerid and p.playerid in player_index.keys():
								player.hookup_tds += 1
								player_index[p.playerid].hookup_tds += 1
								break

		for player in player_index.values():
			player.print_to_file(player_scores)
		
if __name__ == '__main__':
	
	players = ["Russell Wilson","Brock Osweiler","David Johnson","Theo Riddick","Charles Sims","DeAndre Hopkins","Golden Tate","Doug Baldwin","Dez Bryant","Travis Kelce","Wil Lutz","SD"]
	#players = ["Derek Carr","Andy Dalton","Jerick McKinnon","Jay Ajayi","Giovani Bernard","A.J. Green","T.Y. Hilton","Amari Cooper","Travis Benjamin","Gary Barnidge"]
	
	#players = ["Andrew Luck","Kirk Cousins","Todd Gurley","Dwayne Washington","Justin Forsett","Antonio Brown","Markus Wheaton","DeSean Jackson","Anquan Boldin","Jordan Reed"]
	#players = ["Eli Manning","Drew Brees","Ezekiel Elliott","DeAngelo Williams","LeGarrette Blount","Odell Beckham","Kelvin Benjamin","Tajae Sharpe","Willie Snead","Rob Gronkowski"]
	
	player_scores = open('player_scores.csv', 'w')
	player_scores.write(',Comp,Pass Yd,Pass TD,INT,ovr 40,hook TD,Carries,Rush Yd,Rush TD,ovr 40,fum lost,Receptions,Rec Yd,Rec TD,ovr 40,2 pt,Points\n')
	
	team = Team(players, player_scores)
		