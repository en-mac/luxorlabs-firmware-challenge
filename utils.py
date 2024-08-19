import os
from datetime import datetime, timedelta

def get_current_time_period():
    buffer = timedelta(seconds=15)  # Adjust the buffer as needed
    now = datetime.now()

    if os.getenv('TEST_MODE') == 'true':
        second = now.second
        if 0 <= second < 15:
            return 'overclock'
        elif 15 <= second < 30:
            return 'normal'
        elif 30 <= second < 45:
            return 'underclock'
        else:
            return 'curtail'
    else:
        # Production mode with buffer
        now_time = now.time()

        if (datetime.combine(now.date(), datetime.strptime("00:00", "%H:%M").time()) - buffer).time() <= now_time < (datetime.combine(now.date(), datetime.strptime("06:00", "%H:%M").time()) + buffer).time():
            return 'overclock'
        elif (datetime.combine(now.date(), datetime.strptime("06:00", "%H:%M").time()) - buffer).time() <= now_time < (datetime.combine(now.date(), datetime.strptime("12:00", "%H:%M").time()) + buffer).time():
            return 'normal'
        elif (datetime.combine(now.date(), datetime.strptime("12:00", "%H:%M").time()) - buffer).time() <= now_time < (datetime.combine(now.date(), datetime.strptime("18:00", "%H:%M").time()) + buffer).time():
            return 'underclock'
        else:
            return 'curtail'
