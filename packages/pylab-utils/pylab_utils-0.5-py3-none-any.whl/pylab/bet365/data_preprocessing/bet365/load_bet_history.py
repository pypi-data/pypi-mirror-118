"""
load bet365 history from csv to DB or google sheet
"""
import subprocess

import pandas as pd
from sqlalchemy import create_engine

from pylab.bet365.data_preprocessing.bet365.config import GOOGLE_SHEET_BIN, HISTORY_ENRICHED


class Loader:

    @staticmethod
    def load_to_database(file_path: str):
        engine = create_engine('mysql+pymysql://root:root@localhost:3306/bet365')

        csv_file = file_path or HISTORY_ENRICHED['file_path']
        print('Start loading {} to database'.format(csv_file))

        df = pd.read_csv(csv_file)

        df['Date'] = pd.to_datetime(df['Date'])

        df['Bet'] = df['Bet'].apply(Loader.to_float)
        df['Return'] = df['Return'].apply(Loader.to_float)
        df['Gain'] = df['Gain'].apply(Loader.to_float)
        df['Balance'] = df['Balance'].apply(Loader.to_float)

        df.to_sql('history', engine, if_exists='replace', index_label='id')  # use default index col

        print('Finished loading to database, exit...')

    @staticmethod
    def load_to_google_sheet(file_path: str, sheetID: str, valueRange: str):
        print('Start loading {} to google sheet'.format(file_path))

        proc = subprocess.Popen(
            [GOOGLE_SHEET_BIN, '--mode=upload', '--sheetID={}'.format(sheetID),
             '--valueRange={}'.format(valueRange), '--valueInputOption=RAW',
             '--csvFile={}'.format(file_path)], stdin=subprocess.PIPE,
            stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        try:
            while True:
                exit_code = proc.poll()
                if exit_code is not None:
                    print('Process exited with code: ', exit_code)
                    break

                # this is blocking
                # Read until newline or EOF and return a single str. If the stream is already at EOF,
                # an empty string is returned (will not raise or block forever)
                line = proc.stdout.readline()

                if line:
                    print(line.decode('utf-8'))

                # handle oauth in browser, then send the redirect url to stdin
                if 'Command finished' in line.decode('utf-8'):
                    oauth_result = input('oauth url: ')
                    proc.stdin.write((oauth_result + '\n').encode('utf-8'))
                    proc.stdin.flush()
                    # stdout, stderr = proc.communicate(input=oauth_result.encode('utf-8'), timeout=15)
                    # for output in stdout.decode('utf-8').split('\n'):
                    #     print(output)

        except subprocess.TimeoutExpired:
            proc.kill()


    @staticmethod
    def to_float(input):
        if isinstance(input, int) or isinstance(input, float):
            return input

        if isinstance(input, str):
            input = input.replace('$', '').replace(',', '')

        try:
            output = pd.to_numeric(input)
        except:
            print('fail to convert input to numeric value')
            raise

        return output
