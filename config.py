
from enum import Enum

# Constants
EMISSIONS = {
        'nuclear' : 6,
        'solar': 105,
        'wind' : 13,
        'hydro' : 4,
        'gas' : 909,
        'biofuel' : 58,
        'buyable' : 258,
}

PRICES = {
        'nuclear' : 68,
        'solar': 481,
        'wind' : 133,
        'hydro' : 57,
        'gas' : 140,
        'biofuel' : 131,
        'buyable' : 160,
}

class Season(Enum):
        SUMMER = 0
        WINTER = 1

def get_season(inrow):
        if sum(inrow.temps) / len(inrow.temps) > 10:
                return Season.SUMMER
        return Season.WINTER

# blocks of time include start and exclude end
def consumer_rate(season, time):
        if time >= 21 or time < 7:  # off-peak, 21:00 - 7:00
                return 6.5
        elif time < 11 or time >= 17:  # 7:00 - 11:00 or 17:00 - 21:00
                return 9.4 if season == Season.SUMMER else 13.4

        # 11:00 - 17:00
        return 13.4 if season == Season.SUMMER else 9.4

