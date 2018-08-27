from random import randint
from time import sleep
import calendar
from functools import reduce
import timeit

import requests
import json

headers = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'youremail@domain.com'  # This is another valid field
}

def numberOfDays(year, month):
    days = calendar.monthcalendar(int(year), month)
    days = reduce(list.__add__, days)
    days = len([day for day in days if day != 0])
    return days

def parseStandings(startDate, endYear, endMonth, endDay, lastDate):
    startDate = startDate
    endYear = endYear
    endMonth = endMonth#4
    endDay = endDay#9

    endDate = '%d-%d-%d' % (endYear, endMonth, endDay)

    while endDate != lastDate:
        url = 'https://api.dailyfaceoff.com/api/team_corsica_stats.json?api_key=LueJsHh7g7LjSaActxMxZUz1&start_date=' + startDate + '&end_date=' + endDate + '&state=Any&session=Any&venue=Any&report=On-Ice&aggregate=true&adjust=false&format=json'

        for attempt in range(2):
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()

                data = response.json()
                with open('/Users/Milton/Developer/Hockey/data/Standings All/' + endDate + '.json', 'w') as file:
                    file.write(response.text)

                print('Wrote ' + endDate + '.json')

                if endDay == numberOfDays(endYear, endMonth):
                    endDay = 1
                    if endMonth == 12:
                        endMonth = 1
                        endYear += 1
                    else:
                        endMonth += 1
                else:
                    endDay += 1
                endDate = '%d-%d-%d' % (endYear, endMonth, endDay)

                # sleep(randint(1, 3))
                break
            except requests.exceptions.RequestException as e:
                print(e)
        else:
            raise Exception('Reached error twice')


parseStandings('2017-10-04', 2017, 10, 4, '2017-11-2')
parseStandings('2016-10-12', 2016, 10, 12, '2016-11-2')
parseStandings('2015-10-07', 2015, 10, 7, '2015-11-2')
parseStandings('2014-10-08', 2014, 10, 8, '2014-11-2')
parseStandings('2013-10-01', 2013, 10, 1, '2013-11-2')
parseStandings('2011-10-06', 2011, 10, 6, '2011-11-2')
parseStandings('2010-10-07', 2010, 10, 7, '2010-11-2')
parseStandings('2009-10-01', 2009, 10, 1, '2009-11-2')
parseStandings('2008-10-01', 2008, 10, 1, '2008-11-2')
parseStandings('2007-9-29', 2007, 9, 29, '2007-11-2')
