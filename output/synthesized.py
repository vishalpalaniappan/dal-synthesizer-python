from LoggingHelper import semanticLogger
design = 'library_manager'

def createBasket():
    global worldState
    basket = []
    worldState['basket'] = basket
    return 'getChoice'

def getChoice():
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
    global worldState
    basket = worldState['basket']
    book = basket.pop(0)
    worldState['book'] = book
    return 'getFirstLetterOfBookName'

def getFirstLetterOfBookName():
    global worldState
    book = worldState['book']
    name = book['name']
    firstLetter = name[0]
    print(f'Got book named {name} and it has first letter {firstLetter}')
    worldState['firstLetter'] = firstLetter
    return 'getChoice'

def displayChoice():
    global worldState
    choice = worldState['choice']
    print(f'User Choice: {choice}')
    return 'getChoice'

def getName():
    global worldState
    name = input('\nPlease enter book name: ')
    semanticLogger.logParticipant('getName', 'name', 'string', name)
    worldState['name'] = name
    return 'createBook'

def createBook():
    global worldState
    name = worldState['name']
    book = {}
    book['name'] = name
    worldState['book'] = book
    return 'addBookToBasket'

def addBookToBasket():
    global worldState
    book = worldState['book']
    basket = worldState['basket']
    basket.insert(0, book)
    worldState['basket'] = basket
    return 'showBasket'

def showBasket():
    global worldState
    basket = worldState['basket']
    print(f'Basket Contents: {basket}')
    return 'getChoice'
if __name__ == '__main__':
    nextBehavior = 'createBasket'
    worldState = {}
    while nextBehavior:
        nextBehavior = globals()[nextBehavior]()