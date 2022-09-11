# python imports
import time, json
from bs4 import BeautifulSoup
from datetime import date, datetime

# internal imports
from src.config import SELENIUM_TYPE
from src.scraperV2.selenium_utils import generate_driver, get
from src.scraperV2.vc.auth import auth_veracross

# URLS
VERACROSS_URL = "https://accounts.veracross.com/hackley/portals/login"

# selenium imports
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

### Scrape Veracross ###
# this function specifically gets the users daily schedule

def scrape_veracross(username, password):

    TYPE = SELENIUM_TYPE

    TARGET_LINK = "https://portals.veracross.com/hackley/student/redirect/student_schedule"

    driver = generate_driver(TYPE)
    print(f"Selenium Running {TYPE} browser\n")

    try:
        driver = auth_veracross(driver, username, password)
    except:
        raise ValueError("Probably didn't enter username or password correctly")

    driver.get(TARGET_LINK)

    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, 'html.parser')

    '''
    # write html to a file in logs folder in above directory
    with open('logs/schedule.html', 'w') as f:
        f.write(str(soup))
    '''

    # parse the table
    schedule = parse_table(soup)

    return schedule

class Period():
    def __init__(self, start_time, end_time, course, block='', teacher="", room=""):
        self.start_time = start_time
        self.end_time = end_time
        self.course = course
        self.block = block

        # optional bc specials r grade wide meetings, etc.
        self.teacher = teacher
        self.room = room

    def serialize(self):
        return {
            "start_time" : self.start_time,
            "end_time" : self.end_time,
            "course" : self.course,
            "block" : self.block,
            "teacher" : self.teacher,
            "room" : self.room
        }

class Day():
    def __init__(self, num, first, special, second, seventy, lunch1, lunch2, four, five):
        self.num = num
        self.first = first
        self.special = special
        self.second = second
        self.seventy = seventy
        self.lunch1 = lunch1
        self.lunch2 = lunch2
        self.four = four
        self.five = five

    def serialize(self):
        return {
            "Period 1": self.first,
            "Period Special": self.special,
            "Period 2": self.second,
            "Period 70": self.seventy,
            "Period Lunch 1": self.lunch1,
            "Period Lunch 2": self.lunch2,
            "Period 4": self.four,
            "Period 5": self.five
        }

def parse_table(soup):
    days = soup.find_all("div", class_="day")

    current_day = 1
    for day in days:

        blocks = soup.find_all("div", class_="block")
        for block in blocks:

            # replacing br tags with commas so we can split by commas
            for br in block.find_all("br"):
                br.replace_with(",")
            
            text=block.p.text
            text = text.split(",")
            
            # normal period
            if len(text) == 3:
                name = text[0]
                time = text[1]

                time = time.split(" ")
                start_time = time[0]
                end_time = time[2]
                period_block = time[4] + time[5]

                try:
                    teacher = text[2]
                    teacher = teacher.split("-")
                    room = teacher[1]
                    teacher = teacher[0]
                except:
                    teacher = ""
                    room = text[2]

                period = Period(start_time, end_time, name, block, teacher, room)

            # special period/lunch
            elif len(text) == 2:
                name = text[0]
                time = text[1]

                time = time.split(" ")
                start_time = time[0]
                end_time = time[2]
                period_block = time[4] + time[5]

                period = Period(start_time, end_time, name, block)

            # homeroom
            elif len(text) == 1:
                text = text[0].split("-")
                name = text[0]
                start_time = text[1]
                end_time = ""

                period = Period(start_time, end_time, name)
            
            # next need to return periods, sort into days, sort into schedule, store in firebase

            
# testing

if __name__ == "__main__":
    import getpass
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    schedule = scrape_veracross(username, password)
    