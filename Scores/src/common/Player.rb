require 'sorbet-runtime'
require_relative 'Team'

class Player
    extend T::Sig

    sig {params(name: String, team: Team, position: String).void()}
    def initialize(name, team, position)
        @name = name
        @team = team
        @position = position
    end

    sig {returns(String)}
    def name
        @name
    end

    sig {returns(Team)}
    def team
        @team
    end

    sig {returns(String)}
    def position
        @position
    end

    sig {returns(String)}
    def to_s
        "#{@name} (#{@team})"
    end
end