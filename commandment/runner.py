'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

import threading
import datetime
from .database import db_session
from .models import Device

runner_thread = None
runner_time = 15 * 60 # 15 min. in seconds
runner_start = 5 # in seconds

# TODO: currently we start this thread after the database context and
# configuration has already been. We envision a day when this runner runs
# standalone and thus we'll need to sort out seperate configuration routines
# etc.

def start_runner():
	global runner_thread
	start_time = runner_time if runner_thread else runner_start
	runner_thread = threading.Timer(start_time, runner, ())
	runner_thread.daemon = True
	runner_thread.start()

def stop_runner():
	global runner_thread
	if runner_thread is threading.Timer:
		runner_thread.cancel()

def runner():
	print 'runner() called', runner_time, datetime.datetime.now()

	start_runner()
