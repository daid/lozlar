import typing
from checkMetadata import checkMetadataTable

class ItemInfo:
    OPTIONS = []
    MULTIWORLD = False

    def __init__(self):
        self.item = None
        self._location = None
        self.room = None

    def setLocation(self, location):
        self._location = location

    def getOptions(self):
        return self.OPTIONS

    def configure(self, options):
        pass

    def read(self, rom):
        raise NotImplementedError()

    def patch(self, rom, option, *, cross_world=False):
        raise NotImplementedError()

    def __repr__(self):
        return self.__class__.__name__
    
    @property
    def nameId(self):
        return "0x%03X" % self.room if self.room != None else "None"