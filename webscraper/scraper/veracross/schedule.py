# parses pulled veracross schedule html into a specialized dict/array

# external imports
from bs4 import BeautifulSoup

# strips a string of white space
def strip_string(string):
    stripped_string = string.replace(" ", "")
    stripped_string = stripped_string.replace("\n", "")
    return stripped_string

# parses veracross schedule into period objects
def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    schedule = soup.find("div", class_="schedule")

    log = open(f"logs/schedule.html", "w+") 
    log.write(schedule.prettify())
    log.close()

    schedule_list = {}

    try:
        columns = schedule.contents
    except:
        return None

    for column in columns:

        if column.name != 'div':
            continue

        rows = column.contents

        time = rows[1].contents[0].string
        class_ = rows[3].contents[1].string
        teacher = rows[3].contents[5].string

        time = strip_string(time)
        teacher = strip_string(teacher)

        if time == '':
            time = "ALWAYS"

        period = {
            "class" : class_,
            "information" : teacher,
        }

        schedule_list[time] = period

    return schedule_list

# returns the day being scraped
def get_day(html):
    soup = BeautifulSoup(html, 'html.parser')
    day_container = soup.find("h2", class_="rotation-day-header")
    day = day_container.contents[0]
    day = day.replace(" ", "")
    day = day.replace("\n", "")
    day = day.replace("Day", "")

    return day