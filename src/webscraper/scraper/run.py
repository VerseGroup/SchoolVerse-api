# flik
from src.webscraper.scraper.flik.scraper import scrape_flik
from src.webscraper.firebase.menu import write_menu
from datetime import date

# schoology
from src.webscraper.firebase.tasks import write_tasks
from src.webscraper.scraper.schoology.scraper import scrape_schoology
from src.webscraper.firebase.courses import write_courses
from src.webscraper.scraper.schoology.ensure import ensure_schoology

# veracross
from src.webscraper.scraper.veracross.run import scrape_veracross
from src.webscraper.firebase.schedule import write_schedule
from src.webscraper.firebase.events import write_events
from src.webscraper.scraper.veracross.events import get_events

def schoology(db, username, password, user_id):
    returns = scrape_schoology(username, password)
    tasks = returns['tasks']
    write_tasks(tasks, user_id, db)

    return {"message": "successfully scraped schoology"}

def flik(db, useToday=True, day=None):
    if useToday:
        today = date.today()
        today = today.strftime("%d/%m/%Y")
        day = today.split('/')

    menu = scrape_flik(day[0], day[1], day[2])
    write_menu(menu, db)

    return {"message": "successfully scraped flik"}

def veracross(db, username, password):
    days = scrape_veracross(username, password)
    write_schedule(1, days, db)

    return {"message": "successfully scraped veracross"}

def events(db, username, password):
    events = get_events(username, password)
    write_events(events, db)

    return {"message": "successfully scraped events"}

def link(db, ss, platform_code, username, password):
    if platform_code == 'sc':
        if not ensure_schoology(username, password):
            return {"message": "schoology credentials are incorrect"}
        else:
            pass