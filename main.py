import fnmatch

import outfitAPI
from secret import *

data = outfitAPI.getPearlItems()

for i in outfit_list:
    obj = outfitAPI.OutfitAPI(i)
    for j in data:
        match = fnmatch.fnmatch(j['name'], f'*{i}*')
        if obj.count == 0:
            print(j['name'], " has zero buy orders at max")
        elif match:
            number_week = j['seven_day_volume'] / 7
            number_day = j['one_day_volume']
            number = (number_week + number_day) / obj.count
            description = "- Selling higher than normal today" if number_day > number_week else "- Selling lower " \
                                                                                                 "than normal today"
            print(j['name'], int(number), description)
