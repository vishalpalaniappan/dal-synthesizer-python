import logging
from pathlib import Path
from clp_logging.handlers import ClpKeyValuePairStreamHandler

import os, uuid

ADLI_EXECUTION_ID = str(uuid.uuid4())

path = Path(os.path.dirname(__file__)) / f"{ADLI_EXECUTION_ID}.clp.zst"
clp_handler = ClpKeyValuePairStreamHandler(open(path, "wb"))
logger = logging.getLogger("semanticLogger")
logger.setLevel(logging.INFO)
logger.addHandler(clp_handler)

class LoggingHelper:
    '''
        This class holds all the logging functions used by the 
        instrumented code during runtime. 
    '''
    def logParticipant(self, behaviorId, participantName, participantType, participantValue):
        entry = {}
        entry["type"] = "participant"
        entry["behaviorName"] = behaviorId
        entry["participantName"] = participantName
        entry["participantType"] = participantType
        entry["participantValue"] = participantValue
        logger.info(entry)

    def logBehavior(self, behaviorId):
        entry = {}
        entry["type"] = "behavior"
        entry["behaviorName"] = behaviorId
        logger.info(entry)

semanticLogger = LoggingHelper()