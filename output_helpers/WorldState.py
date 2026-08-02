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

    def add(self, name, value, input):
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

        if self.mode == "verbose" or input:
            semanticLogger.logParticipantV2("add", name, self.worldState[name]["value"])

        return self.worldState[name]

    def remove(self, name):
        del self.worldState[name]
        if self.mode == "verbose":
            semanticLogger.logParticipantV2("remove", name, self.worldState[name]["value"])

    def get(self, name):
        if self.mode == "verbose":
            semanticLogger.logParticipantV2("get", name, self.worldState[name]["value"])
        return self.worldState[name]

    def getValue(self, name):
        if self.mode == "verbose":
            semanticLogger.logParticipantV2("getValue", name, self.worldState[name]["value"])
        return self.worldState[name]["value"]

    def getUid(self, name):
        return self.worldState[name]["uid"]

    def update(self, name, value):
        if self.mode == "verbose":
            semanticLogger.logParticipantV2("update", name, self.worldState[name]["value"])
        self.worldState[name]["value"] = value

    def log(self, name):
        semanticLogger.logParticipant(None, name, None, self.worldState[name])