# python imports
import time, json
from bs4 import BeautifulSoup
from datetime import date, datetime

# internal imports
from src.config import SELENIUM_TYPE
from src.scraperV2.selenium_utils import generate_driver, get
from src.scraperV2.vc.auth import auth_veracross

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

def parse_table(soup):
    days = soup.find_all("div", class_="day")

    schedule = {}

    current_day = 1
    for day in days:

        day = []

        blocks = soup.find_all("div", class_="block")
        for block in blocks:

            # replacing br tags with commas so we can split by commas
            for br in block.find_all("br"):
                br.replace_with(",")
            
            text=block.p.text
            text = text.split(",")
            
            # removing unwanted list values
            try:
                text = text.remove("\n")
            except:
                pass

            try:
                text = [x.strip() for x in text]
                text[:] = [x for x in text if x]
            except:
                pass

            if text is None or len(text) == 0:
                continue

            print(text, end="\n\n")
            
            # normal period
            if len(text) == 3:
                name = text[0]
                time = text[1]

                time = time.split(" ")
                start_time = time[0]
                end_time = time[2]
                try:
                    period_block = time[4] + " " + time[5]
                except:
                    try:
                        period_block = time[4]
                    except:
                        period_block = ""

                try:
                    teacher = text[2]
                    teacher = teacher.split("-")
                    room = teacher[1]
                    teacher = teacher[0]
                except:
                    teacher = ""
                    room = text[2]

                period = Period(start_time, end_time, name, period_block, teacher, room)

            # special period/lunch
            elif len(text) == 2:
                name = text[0]
                time = text[1]

                time = time.split(" ")
                start_time = time[0]
                end_time = time[2]
                period_block = time[4] + time[5]

                period = Period(start_time, end_time, name, period_block)

            # homeroom
            elif len(text) == 1:
                text = text[0].split("-")
                name = text[0]
                try:
                    start_time = text[1]
                except:
                    start_time = ""
                end_time = ""

                period = Period(start_time, end_time, name)

            day.append(period.serialize())
        
        schedule[current_day] = day

    return schedule