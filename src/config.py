# APP CONFIG #
from dotenv import load_dotenv
import os

# load env variables
load_dotenv()

# dev or prod sandbox
MODE = os.getenv("MODE")
if MODE is None:
    MODE = "dev"

# selenium driver type to use (chrome or firefox)
SELENIUM_TYPE = "chrome"

# supported platforms to scrape
SUPPORTED_PLATFORMS=["sc", "vc"]

# number of api tasks at once
MAX_TASKS=2

# use auth token to verify user is from our client services
AUTH_TOKEN_REQUIRED=True

# max number of executions to limit firebase
MAX_EXECUTIONS=6 # flik and events scrapes 
MAX_USER_EXECUTIONS=10 # user tasks

# all school events ical from VC
ALL_SCHOOL_EVENTS_ICAL = "http://api.veracross.com/hackley/subscribe/EC34541C-40AC-408F-AD72-FF36D99A220C.ics?uid=A17227D1-8674-45F8-94E7-2AA4A7323593"

# top beta testers
TESTERS = []