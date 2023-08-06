import pandas as pd
from datetime import datetime, timedelta
from urllib.parse import quote_plus

from pylab.bet365.data_preprocessing.bet365.parser import MetaParser, BetResultParser, TeamParser
from pylab.bet365.data_preprocessing.bet365.model import MatchMeta, BetType, BetStyle, BetResult

from pylab.bet365.data_preprocessing.bet365.util import parse_match_date, date_within_n_days


class BasePipeline:
    def __init__(self):
        self.row = None
        self.df = None
        self.idx = None

    def set_context(self, df: pd.DataFrame, row: pd.Series, idx: int):
        self.df = df
        self.idx = idx
        self.row = row

    def transform(self):
        raise NotImplementedError

    def should_transform(self):
        raise NotImplementedError


class BetStyleType(BasePipeline):
    def transform(self):
        if self.should_transform():
            meta = self.row['Match'].replace('\n', '')
            result: MatchMeta = MetaParser.parse(meta)

            # override according to meta data
            if 'corner' in str(self.row['Bet Type']):
                result.bet_type = BetType.ASIAN_CORNER_HANDICAP
            if 'live' in str(self.row['Bet Type']):
                result.bet_style = BetStyle.LIVE

            self.df.loc[self.idx, 'BET_TYPE'] = result.bet_type.value
            self.df.loc[self.idx, 'BET_STYLE'] = result.bet_style.value

    def should_transform(self):
        # FIXME: always parse bet type to fix history data, change this later
        return True


class BetOutcome(BasePipeline):
    def transform(self):
        if self.should_transform():
            bet_result: BetResult = BetResultParser.parse(self.row['Bet'], self.row['Return'])

            if bet_result == BetResult.PUSH:
                # when gain is 0, need to see if it's a cash out or push
                # will default to PUSH unless it is manually commented as 'cash out'
                if 'cash out' in str(self.row['Bet Type']):
                    bet_result = BetResult.CASH_OUT

            self.df.loc[self.idx, 'BET_RESULT'] = bet_result.value

    def should_transform(self):
        # FIXME: always parse bet outcome to fix history data, change this later
        return True


class TeamInformation(BasePipeline):
    def transform(self):
        if self.should_transform():
            team1, team2 = TeamParser.parse(self.row['Match'], self.row['Comments'])

            if team1:
                self.df.loc[self.idx, 'TEAM_1'] = team1
            if team2:
                self.df.loc[self.idx, 'TEAM_2'] = team2

    def should_transform(self):
        return True


class HistoryUrl(BasePipeline):
    """
    add bet365 history url to important bets that's missing information (suggestion for manual edit)
    """
    BASE_URL = 'https://members.bet365.com/members/Services/History/SportsHistory/HistorySearch/?BetStatus=0&SearchScope=3&datefrom={}&dateto={}'

    def transform(self):
        if self.should_transform():
            match_date: datetime = self.row['Date']
            # match_date: datetime = parse_match_date(match_date)
            self.df.loc[self.idx, 'URL'] = self.compose_url(match_date)

    def should_transform(self):
        return abs(self.row['Gain']) > 50 and (pd.isnull(self.row['Comments']) and pd.isnull(self.row['Bet Type']))

    def compose_url(self, match_date: datetime) -> str:
        # date format: DD/MM/YYYY H:M:S
        fmt = '%d/%m/%Y %H:%M:%S'
        from_date = (match_date - timedelta(days=1)).strftime(fmt)
        to_date = (match_date + timedelta(days=1)).strftime(fmt)

        return self.BASE_URL.format(quote_plus(from_date), quote_plus(to_date))


class BetIdentity(BasePipeline):
    """
    identify bets that belongs to the same match ((suggestion for manual edit))
    """

    def transform(self):
        if self.should_transform():
            history_helper = HistoryUrl()
            # match_date = parse_match_date(self.row['Date'])
            match_date = self.row['Date']
            start, end = date_within_n_days(match_date, 4)

            df_to_inspect = self.df[
                (self.df['Date'] > start) & (self.df['Date'] < end) & (self.df['Date'] != match_date)]

            for index, row in df_to_inspect.iterrows():
                if not pd.isnull(row['TEAM_1']) and not pd.isnull(row['TEAM_2']):
                    if self.row['TEAM_1'] == row['TEAM_1'] or self.row['TEAM_1'] == row['TEAM_2']:
                        # consider proximity
                        if abs(self.idx - index) < 7:
                            self.df.loc[
                                self.idx, 'SIMIAR_MATCH_SUGGESTION'] = index + 2  # +2 to compensate csv header and zero index

                            self.df.loc[self.idx, 'URL'] = history_helper.compose_url(match_date)

    def should_transform(self):
        return self.row['Bet'] >= 30 and self.row['TEAM_1'] and not not pd.isnull(self.row['TEAM_2'])


class Report(BasePipeline):
    def transform(self):
        report_df = self.df[self.df['BET_RESULT'] != BetResult.CASH_OUT.value]  # exclude cashout

        # report_df = report_df[report_df['Date'] > datetime.fromisoformat('2019-08-01')]  # optionally set time range

        live_bet_df = report_df[report_df['BET_STYLE'] == BetStyle.LIVE.value]
        prematch_bet_df = report_df[report_df['BET_STYLE'] == BetStyle.PRE_MATCH.value]
        asian_bet_df = report_df[report_df['BET_TYPE'] == BetType.ASIAN_HANDICAP.value]
        final_result_df = report_df[report_df['BET_TYPE'] == BetType.FINAL_RESULT.value]
        corner_bet_df = report_df[report_df['BET_TYPE'] == BetType.ASIAN_CORNER_HANDICAP.value]
        total_goal_df = report_df[report_df['BET_TYPE'] == BetType.TOTAL_GOAL.value]

        Report.report(prematch_bet_df, 'PREMATCH BET')
        Report.report(live_bet_df, 'LIVE BET')
        Report.report(asian_bet_df, 'ASIAN HANDICAP BET')
        Report.report(final_result_df, 'EURO FINAL RESULT BET')
        Report.report(corner_bet_df, 'CORNER BET')
        Report.report(total_goal_df, 'TOTAL GOAL BET')

    def should_transform(self):
        return True

    @staticmethod
    def report(df, bet_signature):
        """
        report template method
        :param df:
        :param bet_signature: identify the bet
        :return:
        """
        print(f"""{bet_signature} report: avg stake: {Report._avg_stake(df)}, ROE: {Report._roe(
            df)}, Change of lost: {Report._lost_percentage(df)} \n""")

    @staticmethod
    def _avg_stake(df: pd.DataFrame):
        """
        avg stake per bet
        :return:
        """
        weighted_total_bet = 0
        total_bet = 0
        for _, row in df.iterrows():
            weighted_total_bet = weighted_total_bet + row['Bet'] * row['Odds']
            total_bet = total_bet + row['Bet']

        return round(weighted_total_bet / total_bet, 2)

    @staticmethod
    def _roe(df):
        """
        return on investment
        :return:
        """
        total_bet = 0
        total_gain = 0
        for _, row in df.iterrows():
            total_bet = total_bet + row['Bet']
            total_gain = total_gain + row['Gain']

        return round(total_gain / total_bet, 2)

    @staticmethod
    def _lost_percentage(df):
        lost = 0
        for _, row in df.iterrows():
            if row['BET_RESULT'] == BetResult.LOOSE.value:
                lost = lost + 1

        return round(lost / df.shape[0], 2)
