from setup import *
from get_time import today_date
from get_backup_date import get_backup_date


def backup_was_already_made():
    if today_date() in get_backup_date():
        return True
    else:
        return False