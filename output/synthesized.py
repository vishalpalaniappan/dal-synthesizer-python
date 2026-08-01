from registered import *
from LoggingHelper import semanticLogger
design = 'simple_invariant_test'

def addNewLineToDisplay():
    semanticLogger.logBehavior('addNewLineToDisplay')
    global worldState
    print(f'')
    return 'getName'

def getName():
    semanticLogger.logBehavior('getName')
    global worldState
    name = input('Provide Name: ')
    if True:
        semanticLogger.logInvariant('getName', 'name_length', 'name')
        if inv_isValid:
            semanticLogger.logInvariantViolation('getName', 'name_length')
    worldState['name'] = name
    return 'getFirstLetterOfName'

def getFirstLetterOfName():
    semanticLogger.logBehavior('getFirstLetterOfName')
    global worldState
    name = worldState['name']
    firstLetter = name[0]
    print(f'First Letter: {firstLetter}')
    worldState['firstLetter'] = firstLetter
    return 'addNewLineToDisplay'
if __name__ == '__main__':
    nextBehavior = 'addNewLineToDisplay'
    worldState = {}
    while nextBehavior:
        nextBehavior = globals()[nextBehavior]()