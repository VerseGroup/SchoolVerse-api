from webscraper.scraper.veracross.events import get_events

def do_events(username, password):
    events = get_events(username, password)
    return events