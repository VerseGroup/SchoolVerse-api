# python imports
import os
import sys

# adding dir to sys to allow local importing
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# for more direct imports
from veracross.selenium.veracross_driver import scrape_veracross
from schoology import scrape_schoology
