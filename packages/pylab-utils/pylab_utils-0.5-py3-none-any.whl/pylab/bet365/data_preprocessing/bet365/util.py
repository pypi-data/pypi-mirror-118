from typing import Tuple
from datetime import datetime, timedelta


def date_within_n_days(date: datetime, n: int = 7) -> Tuple[datetime, datetime]:
    """
    find date range within n days
    :param n:
    :return:
    """
    start = date - timedelta(days=n)
    end = date + timedelta(days=n)

    return start, end


def parse_match_date(date: str) -> datetime:
    return datetime.strptime(date, '%m/%d/%Y %H:%M:%S')
