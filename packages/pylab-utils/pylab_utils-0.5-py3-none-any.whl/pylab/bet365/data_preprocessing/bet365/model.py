from enum import Enum
from dataclasses import dataclass


class BetStyle(Enum):
    LIVE = 'LIVE'
    PRE_MATCH = 'PRE MATCH'


class BetType(Enum):
    ASIAN_HANDICAP = 'ASIAN HANDICAP'
    ASIAN_CORNER_HANDICAP = 'ASIAN CORNER HANDICAP'
    FINAL_RESULT = 'FINAL RESULT'
    TOTAL_CORNER = 'TOTAL CORNER'
    TOTAL_GOAL = 'TOTAL GOAL'
    BTTS = 'BTTS'
    TEAM_TO_SCORE = 'TEAM TO SCORE'
    FINAL_SCORE = 'FINAL SCORE'
    # unable to parse
    UNKNOWN = 'UNKNOWN'


class BetResult(Enum):
    WIN = 'WIN'
    LOOSE = 'LOST'
    PUSH = 'PUSH'
    # only cash out before the game is counted as CASH OUT
    # In game cash out is categorized as either win or loose
    CASH_OUT = 'CASH_OUT'


@dataclass
class MatchMeta:
    bet_style: BetStyle
    bet_type: BetType
