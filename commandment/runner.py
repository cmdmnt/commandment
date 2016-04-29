'''
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.
'''

import threading
import datetime
from .database import db_session
from .models import Device

from .utils.dep_utils import dep_configs_needing_updates, update_dep_configs
from .utils.dep_utils import unsubmitted_dep_profiles, submit_dep_profiles

runner_thread = None
runner_start = 5 # in seconds, time of first run
runner_time = 5 # in seconds, time of subsequent runs

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
	# TODO: catch everything so we don't interrupt the thread (and it never reschedules)
	dep_configs = dep_configs_needing_updates()
	if dep_configs:
		print 'runner() updating DEP configs', runner_time, datetime.datetime.now()
		update_dep_configs(dep_configs)

	dep_profiles = unsubmitted_dep_profiles()
	if dep_profiles:
		print 'runner() submitting DEP profiles', runner_time, datetime.datetime.now()
		submit_dep_profiles(dep_profiles)

	start_runner()
