import csv
from random import randint
from time import sleep
import calendar
from functools import reduce
import timeit
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import requests
import json

from bs4 import BeautifulSoup

chromeFilePath = "/Users/Milton/Developer/Hockey/chromedriver"
driver = webdriver.Chrome(chromeFilePath)

def numberOfDays(year, month):
    days = calendar.monthcalendar(int(year), month)
    days = reduce(list.__add__, days)
    days = len([day for day in days if day != 0])
    return days

def checkTimeout():
    timeout = 20
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, "rt-table")))
    except TimeoutException:
        print("time out")
        driver.quit()

def parseStandings(startDate, endYear, endMonth, endDay, lastDate):
    startDate = startDate
    endYear = endYear
    endMonth = endMonth
    endDay = endDay#9

    endDate = '%d-%d-%d' % (endYear, endMonth, endDay)

    while endDate != lastDate:
        url = 'http://www.nhl.com/stats/team?aggregate=1&reportType=game&dateFrom=' + startDate + '&dateTo=' + endDate + '&gameType=2&filter=gamesPlayed,gte,1&sort=points,wins'

        for attempt in range(2):
            try:
                driver.get(url)

                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")

                timeout = 20
                WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, "rt-table")))

                headers = []
                rows = []

                table = soup.find('div', attrs={'class': 'rt-table'})
                if not headers:
                    for header in table.find_all('div', 'rt-header-cell'):
                        headers.append(header.get_text())
                for row in table.find_all('div', 'rt-tr-group'):
                    cells = []
                    for val in row.find_all('div', 'rt-td'):
                        if val.find('div'):
                            # if val.find('div').find('a'):
                            #     ref = val.find('div').find('a').attrs['href']
                            #     linkTitle = val.find('div').find('a').get_text()
                            #     cells.append(ref + ' | ' + linkTitle)
                            # else:
                            cells.append(val.find('div').get_text())
                        else:
                            cells.append(val.get_text())

                    rows.append(cells)

                with open('/Users/Milton/Developer/Hockey/data/Standings NHL/' + endDate + '.csv', 'w') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                    for row in rows:
                        writer.writerow(row)

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
            except TimeoutException:
                print("time out")
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
