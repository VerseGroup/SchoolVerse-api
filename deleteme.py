from webscraper.scraper.flik.scraper import scrape_flik

if '__main__' == __name__:
    menu = scrape_flik('lunch', '5', '2', '2022')
    print(menu)