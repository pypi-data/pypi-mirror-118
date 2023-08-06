import subprocess

from pylab.bet365.data_preprocessing.bet365.config import GOOGLE_SHEET_BIN, HISTORY_ORIG


def get_new_history():
    proc = subprocess.Popen(
        [GOOGLE_SHEET_BIN, '--mode=bet365'],
        stdin=subprocess.PIPE,
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

            # input user options
            if 'update bet history sheet' in line.decode('utf-8'):
                usr_option = input('option 1: generate bet365 histroy url, option 2: update bet history sheet \n')
                print(usr_option.encode('utf-8'))
                proc.stdin.write((usr_option + '\n').encode('utf-8'))  # need to add \n at the end of user input
                proc.stdin.flush()
                # stdout, stderr = proc.communicate(input=usr_option.encode('utf-8'), timeout=15)
                # for output in stdout.decode('utf-8').split('\n'):
                #     print(output)

    except subprocess.TimeoutExpired:
        proc.kill()


def download_history():
    proc = subprocess.Popen(
        [GOOGLE_SHEET_BIN, '--mode=download', '--sheetID={}'.format(HISTORY_ORIG['sheetID']),
         '--valueRange={}'.format(HISTORY_ORIG['valueRange']), '--csvFile={}'.format(HISTORY_ORIG['file_path'])],
        stdin=subprocess.PIPE,
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
                proc.stdin.write((oauth_result + '\n').encode('utf-8'))  # need to add \n at the end of user input
                proc.stdin.flush()
                # stdout, stderr = proc.communicate(input=oauth_result.encode('utf-8'), timeout=15)
                # for output in stdout.decode('utf-8').split('\n'):
                #     print(output)

    except subprocess.TimeoutExpired:
        proc.kill()
