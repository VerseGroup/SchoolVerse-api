# parses pulled veracross schedule html into a specialized dict/array

# external imports
from bs4 import BeautifulSoup

# strips a string of white space
def strip_string(string) -> str:
    stripped_string = string.replace(" ", "")
    stripped_string = stripped_string.replace("\n", "")
    return stripped_string

def add_free(period, time):
    free_template = {
        "class_name" : "Free",
        "information" : "",
    }
    free_template["start_time"] = time
    free_template["period"] = period
    if time == "12:15pm" or time == "12:45pm":
        free_template["class_name"] = "Lunch"
    return free_template

# parses veracross schedule into period objects
def parse_html(html) -> list:
    soup = BeautifulSoup(html, 'html.parser')
    schedule = soup.find("div", class_="schedule")

    log = open(f"logs/schedule.html", "w+") 
    log.write(schedule.prettify())
    log.close()

    schedule_list = []

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
        teacher = strip_string(teacher).replace("•", "-")

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

        schedule_list.append(period)

    full_schedule = ["Period 1", "Period 2", "Period 3", "Period 4", "Period 5a", "Period 5b", "Period 6", "Period 7"]

    for period in schedule_list:
        if period['period'] in full_schedule:
            full_schedule.remove(period['period'])

    for period in full_schedule:

        if period == "Period 1":
            time = "8:15am"
        elif period == "Period 2":
            time = "9:05am"
        elif period == "Period 3":
            time = "9:55am"
        elif period == "Period 4":
            time = "11:00am"
        elif period == "Period 5a":
            time = "12:15pm"
        elif period == "Period 5b":
            time = "12:45pm"
        elif period == "Period 6":
            time = "1:30pm"
        elif period == "Period 7":
            time = "2:20pm"
        elif period == "Homeroom":
            time = "8:05am"

        schedule_list.append(add_free(period, time))  

    sorted_schedule_list = []

    for period in schedule_list:
        period_num = period['period']
        if period_num == "Homeroom":
            period_num = 0
        else:
            period_num = period_num.replace("Period ", "")
            if period_num == "5a":
                period_num = 5
            elif period_num == "5b":
                period_num = 5.5
        period_num = float(period_num)
        period['period_num'] = period_num

    print(schedule_list)

    # sort the schedule_list array into the sorted_schedule_list array by period number
    for period in sorted(schedule_list, key=lambda k: k['period_num']):
        sorted_schedule_list.append(period)

    for period in sorted_schedule_list:
        del period['period_num']
        
    new_schedule_list = {
        "periods" : sorted_schedule_list,
    } 
        
    return new_schedule_list

# returns the day being scraped
def get_day(html) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    day_container = soup.find("h2", class_="rotation-day-header")
    day = day_container.contents[0]
    day = day.replace(" ", "")
    day = day.replace("\n", "")
    day = day.replace("Day", "")

    print(f"\n \n \n DAY: {day} \n \n \n")

    return day