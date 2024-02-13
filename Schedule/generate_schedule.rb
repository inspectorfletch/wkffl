require 'io/console'

$teams = ["Don", "Dean", "Joe", "Marc", "Josh", "Michael", "Pat", "Nick"]

class Game
    @@divisions = {
        "Don" => "Senior",
        "Dean" => "Senior",
        "Joe" => "Senior",
        "Marc" => "Senior",
        "Josh" => "Junior",
        "Michael" => "Junior",
        "Pat" => "Junior",
        "Nick" => "Junior",
    }

    def initialize(team1, team2)
        @team1 = team1;
        @team2 = team2;
    end

    def team1()
        @team1
    end

    def team2()
        @team2
    end

    def str()
        @team1 + "-" + @team2
    end

    def is_division_game()
        @@divisions[@team1] == @@divisions[@team2]
    end
end

class Week
    def initialize()
        @games = []
    end

    def length()
        @games.length
    end

    def str()
        val = ""
        @games.each do |game|
            val += game.str
            val += "\n"
        end

        val
    end

    def games()
        @games
    end

    def add_game(game)
        valid = true
        if @games.length == 4
            raise "Too many games"
        end

        if valid
            @games.each do |existing_game|
                if (existing_game.team1 == game.team1 ||
                    existing_game.team2 == game.team1 ||
                    existing_game.team1 == game.team2 ||
                    existing_game.team2 == game.team2)
                    valid = false
                end
            end
        end

        if valid
            @games.push(game)
        end

        valid
    end
end

class Season
    def initialize()
        @weeks = []
    end

    def weeks()
        @weeks
    end

    def is_valid(week, last_week)
        valid = true
        week.games.each do |current_week_game|
            last_week.games.each do |last_week_game|
                if (current_week_game.team1 == last_week_game.team1 &&
                    current_week_game.team2 == last_week_game.team2)
                    valid = false
                end
            end
        end

        valid
    end

    def add_week(week)
        valid = true
        if @weeks.length != 0
            last_week = @weeks.last
            valid = is_valid(week, last_week)
        end

        if valid && @weeks.length > 1
            last_week = @weeks[-2]
            valid = is_valid(week, last_week)
        end

        if valid
            @weeks.push(week)
        end

        valid
    end

    def length()
        @weeks.length
    end
end

def make_week(games, division_game_required)
    week = Week.new
    i = 0
    games.each do |game|
        if (!division_game_required || game.is_division_game)
            week.add_game(game)
        end

        if week.length == 4
            break
        end
    end

    if week.length != 4
        week = nil
    end

    week
end

$max_weeks = 0
def generate_schedule()
    games = [
        # Start with games that are required based on previous season standings
        Game.new("Marc", "Josh"),
        Game.new("Dean", "Pat"),
        Game.new("Joe", "Michael"),
        Game.new("Don", "Nick"),

        # Also add rotating intra-division 16th games
        Game.new("Josh", "Pat"),
        Game.new("Michael", "Nick"),
        Game.new("Don", "Joe"),
        Game.new("Dean", "Marc"),
    ]

    i = 0
    while i < $teams.length - 1
        2.times do |x|
            j = i + 1
            while j < $teams.length
                games.push(Game.new($teams[i], $teams[j]))
                j += 1
            end
        end
        i+=1
    end

    games = games.shuffle()
    weeks = Season.new

    # Set aside an all-divisional week for Week 16
    final_week = make_week(games, true)
    final_week.games.each do |game|
        games.delete(game)
    end

    retries = 0
    while games.length > 0
        week = make_week(games, false)
        if week != nil && weeks.add_week(week)
            week.games.each do |game|
                games.delete(game)
            end
        elsif retries < 10
            games = games.shuffle()
            retries += 1
            puts "Retry: " + String(retries)
        else
            break
        end
    end

    if games.length > 0 || !weeks.add_week(final_week)
        $max_weeks = weeks.length > $max_weeks ? weeks.length : $max_weeks
        weeks = nil
    end

    weeks
end

def run_schedule_generation()
    weeks = nil
    tries = 0
    while weeks == nil
        weeks = generate_schedule
        if weeks == nil
            puts "Retry " + String(tries) + ", current max: " + String($max_weeks)
            tries += 1
        end
    end

    weeks.weeks.each_with_index do |week, week_num|
        puts "Week " + String(week_num + 1)
        puts week.str
        puts "\n"
    end

    weeks
end

def write_schedule_to_file()
    Dir.mkdir "schedules" unless File.directory?("schedules")

    schedule_file = File.new(".\\schedules\\schedule.txt", "w")
    team_files = {}
    $teams.each do |team|
        team_file = File.new(".\\schedules\\#{team}.txt", "w")
        team_files[team] = team_file
    end

    weeks = run_schedule_generation()

    weeks.weeks.each_with_index do |week, week_num|
        schedule_file.write("Week #{String(week_num + 1)}")
        schedule_file.write("\n")
        schedule_file.write(week.str)
        schedule_file.write("\n")

        week.games.each do |game|
            team_file = team_files[game.team1]
            team_file.write("Week #{week_num + 1}: #{game.team2}")
            team_file.write("\n")

            team_file = team_files[game.team2]
            team_file.write("Week #{week_num + 1}: #{game.team1}")
            team_file.write("\n")
        end
    end

    schedule_file.close()
    team_files.each do |team, team_file|
        team_file.close()
    end
end

write_schedule_to_file