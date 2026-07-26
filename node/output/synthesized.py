import logging
from pathlib import Path
from clp_logging.handlers import ClpKeyValuePairStreamHandler
import os, uuid
ADLI_EXECUTION_ID = str(uuid.uuid4())
path = Path(os.path.dirname(__file__)) / f'{ADLI_EXECUTION_ID}.clp.zst'
clp_handler = ClpKeyValuePairStreamHandler(open(path, 'wb'))
logger = logging.getLogger('semanticLogger')
logger.setLevel(logging.INFO)
logger.addHandler(clp_handler)

class LoggingHelper:
    """
        This class holds all the logging functions used by the 
        instrumented code during runtime. 
    """

    def logParticipant(self, behaviorId, participantName, participantType, participantValue):
        entry = {}
        entry['type'] = 'participant'
        entry['behaviorName'] = behaviorId
        entry['participantName'] = participantName
        entry['participantType'] = participantType
        entry['participantValue'] = participantValue
        logger.info(entry)

    def logBehavior(self, behaviorId):
        entry = {}
        entry['type'] = 'behavior'
        entry['behaviorName'] = behaviorId
        logger.info(entry)
semanticLogger = LoggingHelper()
design = 'library_manager'

def createBasket():
    semanticLogger.logBehavior('createBasket')
    global worldState
    basket = []
    worldState['basket'] = basket
    return 'getChoice'

def getChoice():
    semanticLogger.logBehavior('getChoice')
    global worldState
    choice = input('\nGet user choice (a for add book, g for get book, else exit): ')
    semanticLogger.logParticipant('getChoice', 'choice', 'string', choice)
    isAdd = choice == 'a'
    isGet = choice == 'g'
    worldState['choice'] = choice
    if isAdd:
        return 'getName'
    if isGet:
        return 'getBookFromBasket'

def getBookFromBasket():
    semanticLogger.logBehavior('getBookFromBasket')
    global worldState
    basket = worldState['basket']
    book = basket.pop(0)
    worldState['book'] = book
    return 'getFirstLetterOfBookName'

def getFirstLetterOfBookName():
    semanticLogger.logBehavior('getFirstLetterOfBookName')
    global worldState
    book = worldState['book']
    name = book['name']
    firstLetter = name[0]
    print(f'Got book named {name} and it has first letter {firstLetter}')
    worldState['firstLetter'] = firstLetter
    return 'getChoice'

def displayChoice():
    semanticLogger.logBehavior('displayChoice')
    global worldState
    choice = worldState['choice']
    print(f'User Choice: {choice}')
    return 'getChoice'

def getName():
    semanticLogger.logBehavior('getName')
    global worldState
    name = input('\nPlease enter book name: ')
    semanticLogger.logParticipant('getName', 'name', 'string', name)
    worldState['name'] = name
    return 'createBook'

def createBook():
    semanticLogger.logBehavior('createBook')
    global worldState
    name = worldState['name']
    book = {}
    book['name'] = name
    worldState['book'] = book
    return 'addBookToBasket'

def addBookToBasket():
    semanticLogger.logBehavior('addBookToBasket')
    global worldState
    book = worldState['book']
    basket = worldState['basket']
    basket.insert(0, book)
    worldState['basket'] = basket
    return 'showBasket'

def showBasket():
    semanticLogger.logBehavior('showBasket')
    global worldState
    basket = worldState['basket']
    print(f'Basket Contents: {basket}')
    return 'getChoice'
if __name__ == '__main__':
    nextBehavior = 'createBasket'
    worldState = {}
    while nextBehavior:
        nextBehavior = globals()[nextBehavior]()