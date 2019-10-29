from abc import ABCMeta, abstractmethod
import nflgame

class PlayerSourceFactory():
    @classmethod
    def create(cls):
        return NflGamePlayerSource()

class PlayerSource:
    __metaclass__ = ABCMeta

    @abstractmethod
    def find(self, name, position): pass

class NflGamePlayerSource(PlayerSource):
    def find(self, name, position):
        player = None

        player_list = nflgame.find(name)
        if player_list is not None and len(player_list) > 0:
            for p in player_list:
                if p.position != '' and p.position == position:
                    player = p
                    break

        if player is None:
            raise Exception(name + " (" + position + ")" + " was not found!")

        return player