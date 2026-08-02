import uuid
from LoggingHelper import semanticLogger

class WorldState:
    '''
        This class will contain the world state of the design. It will
        assign a UID to each participant that is added and then it will
        return the value when requested or the UID + value.
    '''

    def __init__(self):
        self.worldState = {}

    def add(self, name, value):
        self.worldState[name] = {
            "value": value
        }

        if "uid" in value:
            self.worldState[name]["uid"] = value["uid"]
        else:
            self.worldState[name]["uid"] = str(uuid.uuid4())

        return self.worldState[name]

    def remove(self, name):
        del self.worldState[name]

    def get(self, name):
        return self.worldState[name]

    def getValue(self, name):
        return self.worldState[name]["value"]

    def getUid(self, name):
        return self.worldState[name]["uid"]

    def update(self, name, value):
        self.worldState[name]["value"] = value

    def log(self, name):
        semanticLogger.logParticipant(None, name, None, self.worldState[name])


worldStateManager = WorldState()