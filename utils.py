from datetime import datetime

def get_current_time_period():
    now = datetime.now().time()
    if now >= datetime.strptime("00:00", "%H:%M").time() and now < datetime.strptime("06:00", "%H:%M").time():
        return 'overclock'
    elif now >= datetime.strptime("06:00", "%H:%M").time() and now < datetime.strptime("12:00", "%H:%M").time():
        return 'normal'
    elif now >= datetime.strptime("12:00", "%H:%M").time() and now < datetime.strptime("18:00", "%H:%M").time():
        return 'underclock'
    else:
        return 'curtail'


# ## TESTING#
# def get_current_time_period():
#     now = datetime.now()
#     second = now.second

#     if 0 <= second < 15:
#         return 'overclock'
#     elif 15 <= second < 30:
#         return 'normal'
#     elif 30 <= second < 45:
#         return 'underclock'
#     else:
#         return 'curtail'
