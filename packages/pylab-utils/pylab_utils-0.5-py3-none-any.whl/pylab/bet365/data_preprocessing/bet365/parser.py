import re
from typing import Tuple

from pylab.bet365.data_preprocessing.bet365.model import MatchMeta, BetType, BetStyle, BetResult
from pylab.bet365.data_preprocessing.bet365.rules.team import TEAM_MAPPER


class MetaParser:
    """
    Parser for bet type and bet style
    """
    LIVE_BET_RE = re.compile('\(\d+-\d+\)')

    LIVE_BET_RE2 = re.compile('or Draw\s@', re.IGNORECASE)  # Wolverhampton or Draw @ 2.75

    ASIAN_HANDICAP_RE = re.compile('\s[\+, -]?\d\.\d.*?\s@')  # could be goal or corner, cannot conclude from meta str

    TOTAL_CORNER_GOAL_RE = re.compile('(Over|Under)\s(\d+\.\d)', re.IGNORECASE)  # total numeric value: match.group(2)

    BTTS_RE = re.compile('(Yes|No)\s@', re.IGNORECASE)

    TO_SCORE_RE = re.compile('to score', re.IGNORECASE)  # Bologna to score 3rd goal @ 2.50

    FINAL_SCORE_RE = re.compile('\s\d-\d\s@')  # Chelsea 3-2 @ 41.00

    FINAL_RESULT_RE = re.compile('^\D+\s@', re.ASCII)  # Brighton @ 3.25 $23.50 Single

    FINAL_RESULT_RE2 = re.compile('^Draw')  # Draw @ 6.50, this condition needs to be checked first

    @staticmethod
    def parse(meta_data: str) -> MatchMeta:
        bet_type = None

        # step1: parse bet style
        if MetaParser.LIVE_BET_RE.search(meta_data) or MetaParser.LIVE_BET_RE2.search(meta_data):
            bet_style = BetStyle.LIVE
        else:
            bet_style = BetStyle.PRE_MATCH

        # step2: parse bet type
        # more specific bet types are checked first to avoid regex conflict
        # order of the check:
        # BTTS
        # TEAM TO SCORE
        # FINAL SCORE
        # TOTAL GOAL/CORNER
        # ASIAN GOAL/CORNER HANDICAP
        # FINAL RESULT

        # check BTTS before FINAL_RESULT (regex conflict)
        if MetaParser.BTTS_RE.search(meta_data):
            bet_type = BetType.BTTS
        elif MetaParser.TO_SCORE_RE.search(meta_data):
            bet_type = BetType.TEAM_TO_SCORE
            bet_style = BetStyle.LIVE  # override bet style
        elif MetaParser.FINAL_SCORE_RE.search(meta_data):
            bet_type = BetType.FINAL_SCORE
        else:
            match = MetaParser.TOTAL_CORNER_GOAL_RE.search(meta_data)
            if match:
                num_total = match.group(2)
                try:
                    total = float(num_total)
                    # derive type based on the value of total, higher total implies corner
                    # most of the time the bet type is TOTAL_GOAL
                    if 7 < total < 20:
                        bet_type = BetType.TOTAL_CORNER
                    elif total <= 7:
                        bet_type = BetType.TOTAL_GOAL
                    else:
                        bet_type = BetType.UNKNOWN  # should be NBA or NFL
                except:
                    print('fail to parse total number from TOTAL_CORNER_GOAL_RE, match is ', match)
                    pass
            elif MetaParser.ASIAN_HANDICAP_RE.search(meta_data):
                bet_type = BetType.ASIAN_HANDICAP  # could be 'ASIAN CORNER HANDICAP', will conclude later
            elif MetaParser.FINAL_RESULT_RE2.search(meta_data) or MetaParser.FINAL_RESULT_RE.search(meta_data):
                bet_type = BetType.FINAL_RESULT
            else:
                print('!!!Cannot parse meta data: ', meta_data)
                bet_type = BetType.UNKNOWN

        return MatchMeta(bet_type=bet_type, bet_style=bet_style)


class TeamParser:
    @staticmethod
    def parse(meta_data: str, comment: str) -> Tuple[str, str]:
        matched = 0
        team_1 = None
        team_2 = None

        if comment:
            # comment type is 'float' if comment is nan
            if isinstance(comment, str):
                paragraphs = str(comment).split('\n')[0]

                for team_alias in TEAM_MAPPER.keys():
                    for alias in team_alias:
                        if alias.lower() in paragraphs.lower():
                            if matched == 0:
                                team_1 = TEAM_MAPPER[team_alias]
                                matched = matched + 1
                                break
                            elif matched == 1:
                                team_2 = TEAM_MAPPER[team_alias]
                                matched = matched + 1
                                break
                            else:
                                continue
                    if matched == 2:
                        break

                if matched == 0:
                    print('unmatched team name in comment: ', paragraphs)

        # if no match found in comment, try parse team name from match data (bet365 raw)
        if matched == 0:
            meta = meta_data.split('\n')[0]
            for team_alias in TEAM_MAPPER.keys():
                for alias in team_alias:
                    if alias.lower() in meta.lower():
                        team_1 = TEAM_MAPPER[team_alias]
                        matched = matched + 1
                        break

                if matched == 1:
                    break

        return team_1, team_2


class BetResultParser:
    """
    Parser for bet result, possible outcomes:
    1. WIN
    2. LOOSE
    3. PUSH
    4. CASH OUT
    """

    @staticmethod
    def parse(bet: float, bet_return: float):
        gain = bet_return - bet
        gain_pct = round(abs(gain) / bet, 2)

        if 0 < gain_pct < 0.1:
            return BetResult.CASH_OUT  # CASH OUT penalty is smaller than 10%

        if gain > 0:
            return BetResult.WIN
        if gain < 0:
            return BetResult.LOOSE

        if gain == 0:
            # the result could be cash out, will need more information to determine
            return BetResult.PUSH


main_scenarios = [
    'No @ 1.66 $50.00 Single',  # prematch BTTS
    ('Under 3.5 @ 1.700 $50.00 Single', 'Over 2.5 @ 1.970 $17.50 Single'),  # prematch total goal/total corner
    '(0-1) AC Milan 0.0 @ 2.375 $75.65 Single',  # live asian handicap
    '(1-2) Over 3.5 @ 1.820 $20.00 Single',  # live total goal/total corner
    ('Chelsea +0.5 @ 2.010 $100.00 Single', 'Sevilla 0.0,+0.5 @ 2.000 $50.00 Single'),  # prematch asian handicap
    'Brighton @ 3.25 $23.50 Single'  # prematch final result
]

minor_scenarios = [
    'Leeds to score 4th goal @ 2.62 $20.00 Single',  # live TTS (team to score)
    'Denmark 2-0 @ 29.00'  # regular final score
]

bet_time = ('prematch', 'live')
bet_types = ('total goal', 'total corner', 'asian handicap', 'corner handicap', 'btts', 'final result')
misc_bet_types = ('team to score', 'final score')
