import sys
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from random import randint
from time import sleep
import calendar
from functools import reduce
from datetime import datetime


chromeFilePath = "/Users/Milton/Developer/Hockey/chromedriver"
driver = webdriver.Chrome(chromeFilePath)

headers = []
rows = []


def checkTimeout():
    timeout = 20
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, "rt-table")))
    except TimeoutException:
        print("time out")
        driver.quit()


def parse():
    global row
    table = soup.find('div', attrs={'class': 'rt-table'})
    if not headers:
        for header in table.find_all('div', 'rt-header-cell'):
            headers.append(header.get_text())
    for row in table.find_all('div', 'rt-tr-group'):
        cells = []
        for val in row.find_all('div', 'rt-td'):
            if val.find('div'):
                if val.find('div').find('a'):
                    ref = val.find('div').find('a').attrs['href']
                    linkTitle = val.find('div').find('a').get_text()
                    cells.append(ref + ' | ' + linkTitle)
                else:
                    cells.append(val.find('div').get_text())
            else:
                cells.append(val.get_text())

        rows.append(cells)
        # print(len(rows))


def parseMonth(year, month, fromDay, toDay):
    global soup
    for x in range(fromDay, toDay + 1):
        date = '%d-%d-%d' % (year, month, x)
        page_link = 'http://www.nhl.com/stats/team?reportType=game&dateFrom=' + date + '&dateTo=' + date + '&gameType=2&filter=gamesPlayed,gte,1&sort=points,wins'
        driver.get(page_link)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        # soup = BeautifulSoup(open("/Users/Milton/Developer/Hockey/NHL.com - Stats.html"), "html.parser")

        checkTimeout()

        parse()
        # if x % 5 == 0:
        #     sleep(randint(1, 8))


def parseSeason(year):
    for month in range(10, 16):
        newMonth = month
        if newMonth == 13:
            year += 1
        if newMonth > 12:
            newMonth = newMonth - 12
        days = calendar.monthcalendar(int(year), newMonth)
        days = reduce(list.__add__, days)
        days = len([day for day in days if day != 0])

        parseMonth(year, newMonth, 1, days)

        writeCsv(newMonth, year)


def writeCsv(newMonth, year):
    global rows, headers
    with open('/Users/Milton/Developer/Hockey/data/%d-%d.csv' % (newMonth, year), 'w') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)

    print('Wrote CSV %d-%d.csv of row length: %d' % (newMonth, year, len(rows)))
    headers = []
    rows = []





def parseDay(year, month, startDay, endDay):
    parseMonth(year, month, startDay, endDay)
    writeCsv(month, year)



# for year2 in range(2015, 2017):
#     start2 = datetime.now()
#     states2 = parseSeason(year2)
#     finish2 = datetime.now() - start2
#     print(finish2)


# parseDay(2016, 4, 1, 10)
# parseDay(2017, 4, 1, 9)


parseDay(2018, 4, 1, 9)



driver.close()






# import sys
# import requests
# from bs4 import BeautifulSoup
#
# # library to generate user agent
# from user_agent import generate_user_agent
# # generate a user agent
# headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
# #headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.63 Safari/537.36'}

# page_link = 'http://www.nhl.com/stats/team?reportType=game&dateFrom=2017-10-04&dateTo=2018-04-09&gameType=2&filter=gamesPlayed,gte,1&sort=points,wins'
# page_response = requests.get(page_link, timeout = 5, headers=headers)
#
# soup = BeautifulSoup(page_response.content, "html.parser")
#
# table = soup.find('div', attrs={'class': 'rt-table'})
# # headers = [header.text for header in table.find_all('rt-th')]
#
# print(soup)
