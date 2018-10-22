# -*- coding=UTF-8 -*-

DAYS_PER_MONTH = [None, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

class Date:
    def __init__(self, dat):
        self.year, self.month, self.day = list(map(int, [dat[:4], dat[4:6], dat[6:8]]))

    def __le__(self, other):
        if self.year < other.year:
            return True
        if self.year == other.year:
            if self.month < other.month:
                return True
            elif self.month == other.month and self.day <= other.day:
                return True
        return False

    def __sub__(self, other):
        assert other <= self
        if self.year == other.year:
            return sum(DAYS_PER_MONTH[other.month:self.month]) + self.day - other.day + (1 if self.isRoom(self.year) and other.month <= 2 and 2 < self.month else 0)
        first_part = 365 - (sum(DAYS_PER_MONTH[1:other.month]) + other.day)
        last_part = sum(DAYS_PER_MONTH[1:self.month]) + self.day
        if self.isRoom(other.year) and other.month < 3:
            first_part += 1
        if self.isRoom(self.year) and self.month >= 3:
            last_part += 1

        # process [(start_yr + 1) ~ (end_yr - 1)]
        add_days = len([None for yr in range(other.year+1, self.year) if self.isRoom(yr)])
        return first_part + last_part + add_days + (self.year-other.year-1)*365

    @staticmethod
    def isRoom(yr):
        return yr % 400 == 0 or (yr % 100 != 0 and yr % 4 == 0)

#start, end = '20180110', '23560115'
import numpy as np
import datetime
Date2 = lambda x: datetime.datetime.strptime(x, '%Y%m%d')
for yr in np.random.randint(1900, 2030, 1):
    for month in np.random.randint(1, 13, 10):
        for day in np.random.randint(1, 29, 10):
            start = '%d%02d%02d' % (yr, month, day)
            end = (Date2(start) + datetime.timedelta(days=np.random.randint(1000))).strftime('%Y%m%d')

            v1 = Date(end) - Date(start)
            v2 = (Date2(end) - Date2(start)).days
            assert v1 == v2, "%s ~ %s, %d vs %d" % (start, end, v1, v2)
