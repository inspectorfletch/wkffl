from HTMLParser import HTMLParser, HTMLParseError
import urllib, sys

import numbers

def get_distance(score):
	length = ''
	for letter in score:
		try:
			length += str(int(letter))
		except ValueError: pass
	return length

def parse_score(score):
	#print "Score type: " + score[2]
	#print "Detail: " + score[4]
	
	scoreType = score[2]
	scoreDetail = score[4]
	
	if scoreType == 'FG':
		fg = FieldGoal()
		detail = scoreDetail.split(' ')
		
		fg.length = detail[len(detail) - 2]
		fg.who = detail[0:len(detail)-2]
		fg.team = score[0]

		print fg
	
	elif scoreType == 'TD':
		if 'Pass' in scoreDetail:
			td = TouchdownPass()
			
			td.length = get_distance(scoreDetail)
			
			detail = scoreDetail.split(' ')
			for numberIndex in range(0, len(detail)):
				if detail[numberIndex] == td.length: break

			for i in range(0, numberIndex):
				td.receiver += detail[i] + ' '
			td.receiver.strip()
			
			qbStart = scoreDetail.find('From')
			qbEnd = scoreDetail.find('(')
			
			td.passer = scoreDetail[qbStart:qbEnd].strip()
			td.team = score[0]
			
			print td
		
		elif 'Run' in scoreDetail:
			td = Touchdown()
			td.type = 'run'
			td.length = get_distance(scoreDetail)
			
			numberIndex = scoreDetail.find(td.length)
			td.who = scoreDetail[0:numberIndex].strip()
			td.team = score[0]
			
			print td
			
		elif 'Return' in scoreDetail:
			td = ReturnTouchdown()
			td.team = score[0]
			
			td.length = get_distance(scoreDetail)
			index = scoreDetail.find(td.length)
			
			td.player = scoreDetail[0:index].strip()
			
			detail = scoreDetail.split(' ')
			for i in range(0, len(detail)):
				if detail[i] == td.length:
					td.type = detail[i+2]
					break
			
			print td
		
		patStart = scoreDetail.find('(')
		patEnd = scoreDetail.find(')')
		pat = scoreDetail[patStart+1:patEnd]
		patDetail = pat.split(' ')
		if patDetail[len(patDetail)-1] == "Kick":
			xp = ExtraPoint()
			xp.team = score[0]
			xp.kicker = pat[0:pat.find('Kick')].strip()
			
			print xp
		print pat
	
	elif scoreType == 'SF':
		sf = Safety()
		sf.team = score[0]
		
		print sf

class Score:
	def __init__(self):
		self.team = ''

class Touchdown(Score):
	def __init__(self):
		self.type = ''
		self.who = ''
		self.length = ''
	
	def __str__(self):
		return "(" + str(self.team) + ") " + str(self.length) + ' yard ' + self.type + ' by ' + self.who

class TouchdownPass(Touchdown):
	def __init__(self):
		self.passer = ''
		self.receiver = ''
		self.length = ''
	
	def __str__(self):
		return "(" + str(self.team) + ") " + str(self.length) + ' yard touchdown pass from ' + self.passer + ' to ' + self.receiver

class ReturnTouchdown(Touchdown):
	def __init__(self):
		self.team = ''
		self.player = ''
		self.type = ''
	
	def __str__(self):
		return "(" + str(self.team) + ") " + self.player + " " + self.length + " yd " + self.type + " return "

class PAT(Score): pass
class ExtraPoint(PAT):
	def __init__(self):
		self.kicker = ''
	
	def __str__(self):
		return "(" + self.team + ") " + self.kicker + " extra point"

#class TwoPointConversion(PAT):
	#def __init__(self):
		#self.player
		
class FieldGoal(Score):
	def __init__(self):
		self.length = None
		self.who = None
		
	def __str__(self):
		description = "(" + str(self.team) + ") "
		for name in self.who:
			description += name
			description += ' '
		description += self.length + " yard field goal"
		return description

class Safety(Score):
	def __init__(self):
		Score.__init__(self)
	
	def __str__(self):
		return "(" + self.team + ") Safety"

class TouchdownParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.check_header = False
		self.header = ''
		self.inScoringSummary = False
		
		self.getScore = False
		
		self.team = None
		self.score = ''
		
		self.details = []
	
	def handle_starttag(self, tag, attrs):
		if tag == 'h4':
			self.check_header = True
			#print attrs
		
		if tag == 'tbody' and self.inScoringSummary:
			self.getScore = True
		
		if self.getScore and tag == 'img':
			teamPath = attrs[0][1]
			teamPath = teamPath.split('/')
			team = teamPath[len(teamPath)-1]
			team = team.split('.')[0]
			self.team = team
			self.details.append(team)
			
	def handle_endtag(self, tag):
		if tag == 'h4':
			#print self.header
			if self.header == 'Scoring Summary':
				self.inScoringSummary = True
			self.header = ''
			self.check_header = False
		
		if tag == 'tbody': self.getScore = False
		
		if tag == 'table': self.inScoringSummary = False
		
		if tag == 'td' and self.getScore:
			self.details.append(self.score)
			self.score = ''
		
		if tag == 'tr' and self.getScore:
			parse_score(self.details)
			self.details = []
	
	def handle_data(self, data):
		if self.check_header:
			self.header += data
			
		elif self.getScore:
			self.score += data

if __name__ == '__main__':
	tp = TouchdownParser()
	page = urllib.urlopen('http://scores.espn.go.com/nfl/boxscore?gameId=321111033')
	
	#options = dict(output_xhtml=1, add_xml_decl=1, indent=1, tidy_mark=0)
	#page_string = ''
	#for p in page.readlines():
	#	page_string += p
	#tidy_page = str(tidy.parseString(page_string, **options))
	#for i in range(0, min(len(tidy_page), len(page_string))):
		#print page_string[i]
		#print tidy_page[i]
	#print str(page_string).split('\n')
	#print page_string.split('\n')
	#sys.exit(0)
	
	inScriptBlock = False
	for line in page.readlines():
		try:
			tp.feed(line)
		except HTMLParseError as errorSucks:
			print errorSucks