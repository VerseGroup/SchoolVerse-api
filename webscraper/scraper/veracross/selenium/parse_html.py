# external imports
from bs4 import BeautifulSoup

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    log = open(f"logs/scraping/schedule/schedule.html", "w+") 
    log.write(soup.prettify())
    log.close()
