# internal imports
import os
import sys

currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

from scraper import scrape_schoology
