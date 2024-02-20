require 'sorbet-runtime'
require 'sports_data_api'
require 'rest_client'

require_relative 'common/Player'
require_relative 'common/Team'

extend T::Sig

sig {returns(T::Array[Player])}
def generate_rosters()
    SportsDataApi.set_access_level(:nfl, 'trial')
    SportsDataApi.set_key(:nfl, 'tfjckqdd567tmqvk3yhhqsqv')

    players = []

    teams = SportsDataApi::Nfl.teams
    teams.each do |team|
        sleep(1)
        team_roster = SportsDataApi::Nfl.team_roster(team.id)

        team_roster.players.each do |player|
            players.push(Player.new(player[:name], Team.new(team.alias), player[:position]))
        end

        break
    end

    players
end

sig {params(players: T::Array[Player]).void()}
def write_rosters_to_file(players)
    Dir.mkdir "rosters" unless File.directory?("rosters")

    rosters_file = File.new(".\\rosters\\rosters1.txt", "w")

    players.each do |player|
        puts "#{player.name}|#{player.position}|#{player.team}"
        rosters_file.write("#{player.name}|#{player.position}|#{player.team}")
        rosters_file.write("\n")
    end

    rosters_file.close()
end

RestClient.proxy = "http://127.0.0.1:8888/"
players = generate_rosters
write_rosters_to_file(players)
