#!/usr/bin/python3
import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/4F00/chloroplasts/hook_system/processor/Src') #Needs to be set to where the source code is
from Src import app as application