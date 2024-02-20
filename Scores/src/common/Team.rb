require 'sorbet-runtime'

class Team
    extend T::Sig

    sig {params(team_name: String).void()}
    def initialize(team_name)
        @team_name = team_name
    end

    sig {returns(String)}
    def to_s
        @team_name
    end
end