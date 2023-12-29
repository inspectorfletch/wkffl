from nflstatswrapper.nflgamestatswrapper.nflgamestatswrapper import nflgamestatswrapper
from nflstatswrapper.nflapistatswrapper.nflapistatswrapper import nflapistatswrapper

class nflstatswrapperfactory():
    nflgame = "nflgame"
    nflapi = "nflapi"

    @classmethod
    def create(cls, name, at):
        if (name is not None):
            if name == nflstatswrapperfactory.nflgame:
                return nflgamestatswrapper()
            elif name == nflstatswrapperfactory.nflapi:
                return nflapistatswrapper(at)

        raise Exception("Unknown arg: " + name)
