# parses pulled veracross schedule html into a specialized dict/array

# external imports
from bs4 import BeautifulSoup

# strips a string of white space
def strip_string(string) -> str:
    stripped_string = string.replace(" ", "")
    stripped_string = stripped_string.replace("\n", "")
    return stripped_string

# parses veracross schedule into period objects
def parse_html(html) -> list:
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
            continue

        if time == "8:05am":
            period_number = "Homeroom"
        elif time == "8:15am":
            period_number = "Period 1"
        elif time == "9:05am":
            period_number = "Period 2"
        elif time == "9:55am":
            period_number = "Period 3"
        elif time == "11:00am":
            period_number =  "Period 4"
        elif time == "12:15pm":
            period_number = "Period 5a"
        elif time == "12:45pm":
            period_number = "Period 5b"
        elif time == "1:30pm":
            period_number = "Period 6"
        elif time == "2:20pm":
            period_number = "Period 7"
        else:
            period_number = None

        if period_number is None:
            continue

        period = {
            "class_name" : class_,
            "information" : teacher,
            "start_time" : time,
            "period" : period_number,
        }

        schedule_list[period_number] = period
        
    return schedule_list

# returns the day being scraped
def get_day(html) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    day_container = soup.find("h2", class_="rotation-day-header")
    day = day_container.contents[0]
    day = day.replace(" ", "")
    day = day.replace("\n", "")
    day = day.replace("Day", "")

    return day