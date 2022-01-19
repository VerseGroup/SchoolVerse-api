# external imports
from bs4 import BeautifulSoup

def strip_string(string):
    stripped_string = string.replace(" ", "")
    stripped_string = stripped_string.replace("\n", "")
    return stripped_string

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    log = open(f"logs/scraping/schedule/schedule.html", "w+") 
    log.write(soup.prettify())
    log.close()

    schedule_list = {}

    schedule = soup.find("div", class_="schedule")
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

        schedule_list[time] = [class_, teacher]

    return schedule_list
