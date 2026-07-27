from registered import *
from LoggingHelper import semanticLogger
design = 'reverse_name_persist'

def b_createDatabaseConnection():
    semanticLogger.logBehavior('b_createDatabaseConnection')
    global worldState
    connection = connectToDatabase()
    worldState['connection'] = connection
    return 'b_createCursor'

def b_createCursor():
    semanticLogger.logBehavior('b_createCursor')
    global worldState
    connection = worldState['connection']
    cursor = createCursor(connection)
    worldState['cursor'] = cursor
    return 'b_createTable'

def b_createTable():
    semanticLogger.logBehavior('b_createTable')
    global worldState
    cursor = worldState['cursor']
    createTable(cursor)
    return 'b_commitConnection'

def b_commitConnection():
    semanticLogger.logBehavior('b_commitConnection')
    global worldState
    connection = worldState['connection']
    commitConnection(connection)
    return 'b_receiveName'

def b_receiveName():
    semanticLogger.logBehavior('b_receiveName')
    global worldState
    name = receiveName()
    worldState['name'] = name
    return 'b_reverse'

def b_reverse():
    semanticLogger.logBehavior('b_reverse')
    global worldState
    name = worldState['name']
    reversedName = reverse(name)
    worldState['reversedName'] = reversedName
    return 'b_writeToDatabase'

def b_writeToDatabase():
    semanticLogger.logBehavior('b_writeToDatabase')
    global worldState
    cursor = worldState['cursor']
    reversedName = worldState['reversedName']
    writeToDatabase(cursor, reversedName)
    return 'b_commitConnection'
if __name__ == '__main__':
    nextBehavior = 'b_createDatabaseConnection'
    worldState = {}
    while nextBehavior:
        nextBehavior = globals()[nextBehavior]()