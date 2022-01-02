# python imports
import os
import sys

# adding dir to sys to allow local importing
currentdir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentdir)

# importing packages in the init for shorter imports in other files
from .decrypt import decrypt # soon change to just importing network_manager which will handle decryption itself
from .network_manager import get_credentials