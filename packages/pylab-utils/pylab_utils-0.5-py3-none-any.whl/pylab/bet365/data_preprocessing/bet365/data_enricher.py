"""
enrich bet365 history data using heuristic approach
"""
import pandas as pd

from pylab.bet365.data_preprocessing.bet365.pipeline import HistoryUrl, BetStyleType, BetOutcome, TeamInformation, \
    BetIdentity, Report

from pylab.bet365.data_preprocessing.bet365.load_bet_history import Loader
from pylab.bet365.data_preprocessing.bet365.config import HISTORY_ORIG, HISTORY_ENRICHED, HISTORY_MANUAL_UPDATE, \
    HISTORY_DEBUG


class Processor:
    data_enrich_pipeline = [BetStyleType(), BetOutcome(), TeamInformation()]
    suggestion_pipeline = [HistoryUrl(), BetIdentity()]
    report_pipeline = [BetStyleType(), BetOutcome(), TeamInformation(), Report()]

    @staticmethod
    def enrich():
        df = pd.read_csv(HISTORY_ORIG['file_path'])
        df['Date'] = pd.to_datetime(df['Date'])

        for index, row in df.iterrows():
            for transformer in Processor.data_enrich_pipeline:
                transformer.set_context(df, row, index)
                transformer.transform()

        df.drop(columns=['Bet Type'], inplace=True)  # drop unused bet type

        df.to_csv(HISTORY_ENRICHED['file_path'], index=False)

        Loader.load_to_google_sheet(HISTORY_ENRICHED['file_path'], HISTORY_ENRICHED['sheetID'],
                                    HISTORY_ENRICHED['valueRange'])
        Loader.load_to_database(HISTORY_ENRICHED['file_path'])

    @staticmethod
    def suggest_update_history():
        df = pd.read_csv(HISTORY_ORIG['file_path'])
        df['Date'] = pd.to_datetime(df['Date'])

        for index, row in df.iterrows():
            for transformer in Processor.data_enrich_pipeline:
                transformer.set_context(df, row, index)
                transformer.transform()

        for index, row in df.iterrows():
            for transformer in Processor.suggestion_pipeline:
                transformer.set_context(df, row, index)
                transformer.transform()

        output_path = HISTORY_MANUAL_UPDATE['file_path']
        df.to_csv(output_path, index=False)
        Loader.load_to_google_sheet(output_path, HISTORY_MANUAL_UPDATE['sheetID'], HISTORY_MANUAL_UPDATE['valueRange'])

    @staticmethod
    def debug():
        path = HISTORY_DEBUG['file_path']
        Loader.load_to_google_sheet(path, HISTORY_DEBUG['sheetID'], HISTORY_DEBUG['valueRange'])

    @staticmethod
    def report():
        df = pd.read_csv(HISTORY_ORIG['file_path'])
        df['Date'] = pd.to_datetime(df['Date'])

        report_transformer = Processor.report_pipeline.pop()

        for index, row in df.iterrows():
            for transformer in Processor.report_pipeline:
                transformer.set_context(df, row, index)
                transformer.transform()

        report_transformer.set_context(df, None, None)
        report_transformer.transform()
