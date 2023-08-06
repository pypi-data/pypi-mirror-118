from datetime import datetime


def get_today_str(date_format: str = "%Y%m%d"):
    """
    Returns today's date as string.
    """
    return datetime.today().strftime(date_format)
