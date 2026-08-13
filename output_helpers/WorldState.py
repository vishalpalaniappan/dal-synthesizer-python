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
        self.behavior = None
        self.mode = mode

    def setBehavior(self, behaviorName):
        self.behavior = behaviorName
        if self.mode == "verbose":
            semanticLogger.logBehavior(behaviorName)

    def setInvariantViolation(self, invariantName, invartiantParticipant, protectedBehavior):
        semanticLogger.logInvariant(self.behavior, invariantName, invartiantParticipant, protectedBehavior )

    def setFailure(self):
        semanticLogger.logFailure(self.behavior)

    def create(self, name, value, type, role, inputFlag):
        try:
            self.worldState[name] = {
                "value": value["value"],
                "uid": value["uid"]
            }
        except:
            self.worldState[name] = {
                "value": value,
                "uid": str(uuid.uuid4())
            }

        if inputFlag:
            semanticLogger.logParticipantV2("addInput", name, self.worldState[name]["value"])
        elif self.mode == "verbose":
            semanticLogger.logParticipantV2("create", name, self.worldState[name]["value"])

        return self.worldState[name]


    def add(self, name, value, type, role, inputFlag):
        try:
            self.worldState[name] = {
                "value": value["value"],
                "uid": value["uid"]
            }
        except:
            self.worldState[name] = {
                "value": value,
                "uid": str(uuid.uuid4())
            }

        if inputFlag:
            semanticLogger.logParticipantV2("addInput", name, self.worldState[name]["value"])
        elif self.mode == "verbose":
            semanticLogger.logParticipantV2("add", name, self.worldState[name]["value"])

        return self.worldState[name]

    def remove(self, name):
        if self.mode == "verbose":
            semanticLogger.logParticipantV2("remove", name, None)
        del self.worldState[name]

    def get(self, name, type, role):
        if self.mode == "verbose":
            semanticLogger.logParticipantV2("get", name, None)
        return self.worldState[name]

    def getValue(self, name, type, role):
        if self.mode == "verbose":
            semanticLogger.logParticipantV2("getValue", name, None)
        return self.worldState[name]["value"]

    def getUid(self, name):
        return self.worldState[name]["uid"]

    def hasParticipant(self, name):
        if name in self.worldState:
            return True
        else:
            return False

    def hasParticipants(self, names):
        for name in names:
            if name not in self.worldState:
                return False
        return True

    def update(self, name, value, type, role):
        self.worldState[name]["value"] = value
        if self.mode == "verbose":
            semanticLogger.logParticipantV2("update", name, self.worldState[name]["value"])