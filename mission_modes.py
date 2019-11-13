from enum import Enum


class MissionMode(Enum):
    PRE_TX = 0
    COMM_TX = 1
    ANTENNA_DEPLOY = 2
    PRE_BOOM_DEPLOY = 3
    BOOM_DEPLOY = 4
    COMM_PIC = 5
    POST_BOOM_DEPLOY = 6
    SAFE = 7
