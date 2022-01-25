# internal imports
import os
import sys

# local dir for local imports
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# local imports
from scraper import scrape_schoology
