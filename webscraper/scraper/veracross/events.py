# external imports
from bs4 import BeautifulSoup
import json

def scrape_events(start_year, start_month, start_day, end_year, end_month, end_day, driver):
    url = f"https://portals.veracross.com/hackley/student/calendar/school/events?begin_date={start_month}%2F{start_day}%2F{start_year}&end_date={end_month}%2F{end_day}%2F{end_year}"
    
    print()
    print(url)
    print()

    driver.get(url)
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find_all('pre')[0].text
    
    json_data = data.json()
    return json_data