from WorldState import WorldState
from registered import *
from LoggingHelper import semanticLogger

def test():
    worldStateManager.setBehavior('test')
    global worldState
if __name__ == '__main__':
    worldStateManager = WorldState('verbose')
    nextBehavior = 'test'
    worldState = {}
    while nextBehavior:
        try:
            nextBehavior = globals()[nextBehavior]()
        except Exception as e:
            worldStateManager.setFailure()
            raise e