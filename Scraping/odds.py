from random import randint
from time import sleep
import calendar
from functools import reduce
import timeit

from bs4 import BeautifulSoup
import requests
import json

headers = {
    'User-Agent': 'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16'
}

def numberOfDays(year, month):
    days = calendar.monthcalendar(int(year), month)
    days = reduce(list.__add__, days)
    days = len([day for day in days if day != 0])
    return days

def parseOdds(startDate, endYear, endMonth, endDay, lastDate):
    startDate = startDate
    endYear = endYear
    endMonth = endMonth
    endDay = endDay

    endDate = '%d%02d%02d' % (endYear, endMonth, endDay)

    while endDate != lastDate:
        url = 'https://classic.sportsbookreview.com/betting-odds/nhl-hockey/?date=' + endDate

        for attempt in range(2):
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')

                with open('/Users/Milton/Developer/Hockey/data/Odds/' + endDate + '.html', 'w') as file:
                    file.write(response.text)

                print('Wrote ' + endDate + '.html')

                if endDay == numberOfDays(endYear, endMonth):
                    endDay = 1
                    if endMonth == 12:
                        endMonth = 1
                        endYear += 1
                    else:
                        endMonth += 1
                else:
                    endDay += 1
                endDate = '%d%02d%02d' % (endYear, endMonth, endDay)

                # sleep(randint(3, 10))
                break
            except requests.exceptions.RequestException as e:
                print(e)
        else:
            raise Exception('Reached error twice')


# Dates + 1
parseOdds('2017-10-04', 2017, 10, 1, '2018-4-10')
parseOdds('2016-10-12', 2016, 10, 12, '20170409')
parseOdds('2015-10-07', 2015, 10, 7, '20160410')
parseOdds('2014-10-08', 2014, 10, 8, '20150411')
parseOdds('2013-10-01', 2013, 10, 1, '20140413')
parseOdds('2011-10-06', 2011, 10, 6, '20120407')
parseOdds('2010-10-07', 2010, 10, 7, '20110410')
parseOdds('2009-10-01', 2009, 10, 1, '20100411')
parseOdds('2008-10-01', 2008, 10, 1, '20090412')
parseOdds('2007-9-29', 2007, 9, 29, '20080406')


