import locale
import datetime


def get_days_name():
    # Set the locale for the current session to English (United States)
    locale.setlocale(locale.LC_TIME, 'en_US.utf8')

    # Get the abbreviated day name (e.g., "Mon", "Tue", etc.) for the current day
    abbreviated_day_name = datetime.datetime.today().strftime('%a')

    return str(abbreviated_day_name)