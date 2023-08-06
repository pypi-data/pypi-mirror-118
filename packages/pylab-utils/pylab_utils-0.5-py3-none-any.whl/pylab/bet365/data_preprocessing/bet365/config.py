import os

GOOGLE_SHEET_BIN = os.path.join(os.path.dirname(__file__), '../../bin/google-sheet-util')

HISTORY_ORIG = {
    'sheetID': '1i4zZaT-KcKqvTfpgouEJPPofWXA2EueKJ9yNNZvWMPA',
    'valueRange': 'raw!A:J',
    'file_path': os.path.join(os.path.dirname(os.path.realpath(__file__)), './input/bet365_history.csv')
}

HISTORY_MANUAL_UPDATE = {
    'sheetID': '1R-VtDkVxM_WP8DEervhmodUW-JaV20zw60fErliIjEg',
    'valueRange': 'manual!A:CZ',
    'file_path': os.path.join(os.path.dirname(os.path.realpath(__file__)), './output/manual_edit.csv')
}

HISTORY_ENRICHED = {
    'sheetID': '1R-VtDkVxM_WP8DEervhmodUW-JaV20zw60fErliIjEg',
    'valueRange': 'enriched!A:CZ',
    'file_path': os.path.join(os.path.dirname(os.path.realpath(__file__)), './output/enriched.csv')
}

HISTORY_DEBUG = {
    'sheetID': '1R-VtDkVxM_WP8DEervhmodUW-JaV20zw60fErliIjEg',
    'valueRange': 'manual!A:CZ',
    'file_path': os.path.join(os.path.dirname(os.path.realpath(__file__)), './output/debug.csv')
}
