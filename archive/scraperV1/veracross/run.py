""" # function to scrape veracross using selenium

# python imports
import time
from datetime import date

# internal imports
from src.webscraper.scraper.veracross.get_element import get
from src.webscraper.scraper.veracross.schedule import parse_html, get_day
from src.webscraper.scraper.veracross.driver import generate_driver
from src.webscraper.scraper.veracross.auth import auth_veracross
from src.webscraper.scraper.veracross.events import scrape_events
from src.config import SELENIUM_TYPE


# selenium imports
from selenium.webdriver.common.by import By

def get_schedule(driver, day, month, year) -> str:

    SCHEDULE_URL = f"https://portals.veracross.com/hackley/student/student/daily-schedule?date={year}-{month}-{day}"
    driver.get(SCHEDULE_URL)

    schedule_page = driver.page_source

    return schedule_page

def scrape_veracross(username, password, today=True) -> tuple:

    TYPE = SELENIUM_TYPE

    print("Executing...\n")
    driver = generate_driver(TYPE)
    print(f"Running {TYPE} browser\n")

    try:
        print("Authenticating veracross...\n")
        driver = auth_veracross(driver, username, password)
    except:
        raise ValueError("Probably didn't enter username or password correctly")

    if today==True:
        today = date.today()
        today = today.strftime("%d/%m/%Y")
        today = today.split('/')

    required_days = [1, 2, 3, 4, 5, 6, 7]
    required_days_count = len(required_days)
    count = 0
    days = []

    scraping_day = int(today[0])
    scraping_month = int(today[1]) - 2 # remove -=2

    while count < 30:

        scraping_day += 1

        if scraping_day > 28:
            scraping_day = 1
            scraping_month = scraping_month + 1

        print("Getting schedule...\n")
        html = get_schedule(driver, str(scraping_day), str(scraping_month), today[2])

        print("Parsing schedule...\n")
        schedule = parse_html(html)

        print("Getting day...\n")
        try:
            day = int(get_day(html))
            schedule['day'] =  f"Day {day}"
        except:
            count += 1
            continue

        print("Found new day...\n")
        if day in required_days:
            days.append(schedule)
            required_days.remove(int(day))
            required_days_count -= 1
            print(f"FOUND day {day}...\n")

        count += 1
        print(f"Loop Iterations: {count}")
        print(f"Required Days Remaining: {required_days}" + "\n")
        print(f"Number of Required Days Remaining: {required_days_count}" + "\n")

        if required_days_count == 0:
            break

    driver.close()
    driver.quit()

    if count == 30:
        print("Couldn't find all required days...\n")

    return days



 """