import uuid

class WorldState:
    '''
        This class will contain the world state of the design. It will
        assign a UID to each participant that is added and then it will
        return the value when requested or the UID + value.
    '''

    def __init__(self):
        self.worldState = {}

    def add(self, name, value):
        if name in self.worldState:
            self.worldState[name]["value"] = value
        else:
            self.worldState[name] = {
                "value": value,
                "uid": str(uuid.uuid4())
            }

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


worldState = WorldState()


if __name__ == "__main__":
    worldState.add("bucket", [])
    print(worldState.get("bucket"))
    print(worldState.getUid("bucket"))
    print(worldState.getValue("bucket"))


    '''
        worldState(<cmd>, <arg>)

        worldState("add", "bucket", [])

        worldState("getUid", "bucket")
    '''
