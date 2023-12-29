import random
import copy
import sys
import os

num_weeks = 16

class Game:
    division = { "Don": "Senior",
        "Dean": "Senior",
        "Joe": "Senior",
        "Marc": "Senior",
        "Josh": "Junior",
        "Michael": "Junior",
        "Pat": "Junior",
        "Nick": "Junior",
    }

    def __init__(self, team1, team2):
        self.Team1 = team1
        self.Team2 = team2

    def IsEqual(self, other_game):
        if ((self.Team1 == other_game.Team1 and self.Team2 == other_game.Team2) or
            (self.Team2 == other_game.Team1 and self.Team1 == other_game.Team2)):
            return True

        return False

    def IsDivisionGame(self) -> bool:
        return Game.division[self.Team1] == Game.division[self.Team2]

    def __str__(self) -> str:
        return self.Team1 + " - " + self.Team2

class Week:
    def __init__(self):
        self.games = []

    def Length(self):
        return len(self.games)

    def AddGame(self, newGame) -> bool:
        teams = set([])
        for game in self.games:
            teams.add(game.Team1)
            teams.add(game.Team2)
            if newGame.Team1 in teams or newGame.Team2 in teams:
                return False

        self.games.append(newGame)
        return True

    def IsValid(self, previous_week) -> bool:
        if self.Length() != 4:
            return False
        if previous_week is None:
            return True

        for game in self.games:
            for previous_week_game in previous_week.games:
                if game.IsEqual(previous_week_game):
                    return False
        
        return True

    def __str__(self):
        val = ""
        for game in self.games:
            val += str(game)
            val += "\r\n"

        return val

if __name__ == '__main__':
    year = None
    if len(sys.argv) == 2:
        try:
            year = sys.argv[1]
        except:
            year = None

    teams = ["Don", "Dean", "Joe", "Marc", "Josh", "Michael", "Pat", "Nick"]
    games = [
        # Cross-division, standings-based games
        Game("Joe", "Josh"),
        Game("Marc", "Pat"),
        Game("Don", "Michael"),
        Game("Dean", "Nick"),

        # Rotating, yearly intra-division matchups
        Game("Josh", "Michael"),
        Game("Pat", "Nick"),
        Game("Don", "Dean"),
        Game("Joe", "Marc")
    ]

    for i in range(0, 2):
        teams = ["Don", "Dean", "Joe", "Marc", "Josh", "Michael", "Pat", "Nick"]
        teams.reverse()
        while len(teams) > 1:
            team1 = teams.pop()

            for team in teams:
                game = Game(team1, team)
                games.append(game)

    games_backup = copy.deepcopy(games)
    random.shuffle(games)
    weeks = []
    i = 0

    # Generate a division-only week, and save it for the last week of the regular season
    last_week = Week()
    for game in games:
        if game.IsDivisionGame() and last_week.AddGame(game):
            games.remove(game)

    print (last_week)

    while len(weeks) < (num_weeks - 1):
        week = Week()

        for game in games:
            if not(week.AddGame(game)):
                continue

            if (week.Length() >= 4):
                break

        previous_week = weeks[-1] if len(weeks) > 0 else None
        if week.IsValid(previous_week):
            for game in week.games:
                games.remove(game)

            weeks.append(week)
        elif len(weeks) <= (num_weeks - 3):
            print ("Week not generating, shuffle and try again; Week number: " + str(len(weeks) + 1))
            random.shuffle(games)
        else:
            print ("Week not generated, restarting: " + str(i) + ", Week number: " + str(len(weeks) + 1))
            i += 1
            games = copy.deepcopy(games_backup)
            random.shuffle(games)
            weeks = []

    second_last_week = weeks[-1]
    if second_last_week.IsValid(last_week):
        weeks.append(last_week)
    else:
        print ("It didn't work, try again")
        exit(1)

    i = 1
    for finished_week in weeks:
        print ("Week " + str(i))
        i += 1
        print(str(finished_week))

    try:
        if year is not None:
            if not os.path.exists(year):
                os.mkdir(year)
    except:
        year = None
    
    outFile = open('schedule.txt' if year is None else year + '/schedule.txt', 'w')
    files = {
            'Don':open('Don.txt' if year is None else year + '/Don.txt', 'w'),
            'Marc':open('Marc.txt' if year is None else year + '/Marc.txt', 'w'),
            'Dean':open('Dean.txt' if year is None else year + '/Dean.txt', 'w'),
            'Joe':open('Joe.txt' if year is None else year + '/Joe.txt', 'w'),
            'Nick':open('Nick.txt' if year is None else year + '/Nick.txt', 'w'),
            'Michael':open('Michael.txt' if year is None else year + '/Michael.txt', 'w'),
            'Josh':open('Josh.txt' if year is None else year + '/Josh.txt', 'w'),
            'Pat':open('Pat.txt' if year is None else year + '/Pat.txt', 'w')
            }
    for i in range(len(weeks)):
        outFile.write("Week " + str(i+1) + ":\n")
        for game in weeks[i].games:
            outFile.write('\t' + str(game) + '\n')

            team1 = game.Team1
            team2 = game.Team2

            files[team1].write("Week " + str(i+1) + ": " + team2 + "\n")
            files[team2].write("Week " + str(i+1) + ": " + team1 + "\n")
    outFile.close()
