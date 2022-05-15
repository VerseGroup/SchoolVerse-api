# flik
from src.webscraper.scraper.flik.scraper import scrape_flik
from src.webscraper.firebase.menu import write_menu
from datetime import date

# schoology
from src.webscraper.firebase.tasks import write_tasks
from src.webscraper.scraper.schoology.scraper import scrape_schoology
from src.webscraper.firebase.courses import write_courses

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

def veracross():
    pass