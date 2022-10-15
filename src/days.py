# # python imports
# import os
# import sys

# # adding directories for local imports
# parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
# sys.path.append(parentdir)
# currentdir = os.path.abspath(os.path.dirname(__file__))
# sys.path.append(currentdir)

# from src.scraperV2.vc.events import convert_all_school_events
# from src.config import ALL_SCHOOL_EVENTS_ICAL
# import json

# days, events = convert_all_school_events(ALL_SCHOOL_EVENTS_ICAL)

# with open('days.json', 'w') as f:
#     json.dump(days, f)