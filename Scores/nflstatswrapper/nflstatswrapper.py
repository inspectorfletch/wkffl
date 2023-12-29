from abc import ABCMeta, abstractmethod

class nflstatswrapper:
    __metaclass__ = ABCMeta

    @abstractmethod
    def find_player(self, name, position): pass

    @abstractmethod
    def find_game(self, team_name, year, week): pass

    @abstractmethod
    def current_year_and_week(self): pass

    @abstractmethod
    def get_standard_team_name(self, team_name): pass

    @abstractmethod
    def get_team_plays(self, game): pass
