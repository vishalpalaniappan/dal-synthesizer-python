import uuid
from LoggingHelper import semanticLogger

class WorldState:
    '''
        This class will contain the world state of the design. It will
        assign a UID to each participant that is added and then it will
        return the value when requested or the UID + value.

        It wll also act as the boudary through which all world state
        transformations happen. This will then allow you to log all the
        information needed to understand how the design modifies the world
        state and the invariants that were violated.
    '''

    def __init__(self, mode):
        self.worldState = {}
        self.mode = mode

    def add(self, name, value):
        if "uid" in value:
            self.worldState[name] = {
                "value": value["value"],
                "uid": value["uid"]
            }
        else:
            self.worldState[name] = {
                "value": value,
                "uid": str(uuid.uuid4())
            }

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
        self.log(name)

    def log(self, name):
        semanticLogger.logParticipant(None, name, None, self.worldState[name])