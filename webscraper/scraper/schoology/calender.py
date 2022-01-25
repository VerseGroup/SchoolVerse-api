# python imports
import os
import sys

# adding parentdirs for internal imports
# adding directories for local imports
parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)
doubleparentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
sys.path.append(doubleparentdir)

# internal imports
from models import Event, Task


def parse_calender(calender_json):

    for event in calender_json:
        pass
