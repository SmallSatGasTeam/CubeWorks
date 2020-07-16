from enum import Enum


class MissionMode(Enum):
    BOOT = 0
    ANTENNA_DEPLOY = 1
    PRE_BOOM_DEPLOY = 2
    BOOM_DEPLOY = 3
    POST_BOOM_DEPLOY = 4
    COMM_TX = 5
    SAFE = 6
