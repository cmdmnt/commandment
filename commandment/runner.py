# -*- coding: utf-8 -*-
"""
Copyright (c) 2015 Jesse Peterson
Licensed under the MIT license. See the included LICENSE.txt file for details.

Attributes:
    runner_thread (threading.Timer):
    runner_start (int): In seconds, time of first run
    runner_time (int): In seconds, time of subsequent runs

Todo:
    * Currently we start this thread after the database context and
      configuration has already been. We envision a day when this runner runs
      standalone and thus we'll need to sort out separate configuration routines etc.
"""

import threading
import datetime
from .models import db, Device

runner_thread = None
runner_start = 5
runner_time = 5


def start_runner():
    """Start the runner thread"""
    global runner_thread
    start_time = runner_time if runner_thread else runner_start
    runner_thread = threading.Timer(start_time, runner, ())
    runner_thread.daemon = True
    runner_thread.start()


def stop_runner():
    """Stop the runner thread"""
    global runner_thread
    if runner_thread is threading.Timer:
        runner_thread.cancel()


def runner():
    """Runner thread main procedure

    Todo:
        * Catch everything so we don't interrupt the thread (and it never reschedules)
        * Certificate expiration warnings/emails
    """
    # dep_configs = dep_configs_needing_updates()
    # if dep_configs:
    #     print('runner() updating DEP configs', runner_time, datetime.datetime.now())
    #     update_dep_configs(dep_configs)
    #
    # dep_profiles = unsubmitted_dep_profiles()
    # if dep_profiles:
    #     print('runner() submitting DEP profiles', runner_time, datetime.datetime.now())
    #     submit_dep_profiles(dep_profiles)

    start_runner()
