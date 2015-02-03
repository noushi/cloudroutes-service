#!/usr/bin/python
#####################################################################
# Cloud Routes Availability Manager: Control
# ------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------
# This is the control process for the availability manager.
# This process will periodically pull domains to check from redis
# and send the entries to message broker via zMQ
# ------------------------------------------------------------------
# Version: Alpha.20140308
# Original Author: Benjamin J. Cane - madflojo@cloudrout.es
# Contributors:
# - your name here
#####################################################################


# Imports
# ------------------------------------------------------------------

import sys
import zmq
import time
import yaml
import signal
import logconfig

from apscheduler.schedulers.blocking import BlockingScheduler
from retrieve import create_retriever

# Load Configuration
# ------------------------------------------------------------------

if len(sys.argv) != 2:
    print("Hey, thats not how you launch this...")
    print("%s <config file>") % sys.argv[0]
    sys.exit(1)

# Open Config File and Parse Config Data
configfile = sys.argv[1]
with open(configfile, "r") as cfh:
    config = yaml.safe_load(cfh)


# Make Connections
# ------------------------------------------------------------------

# Init logger
logger = logconfig.getLogger('monitors.control', config['use_syslog'])
logger.info("Using config %s" % configfile)

# Init monitor data retriever
mdr = create_retriever(config=config, logger=logger)
logger.info("Using {0} retriever".format(mdr.__class__.__name__))

# Start ZeroMQ listener
context = zmq.Context()
zsend = context.socket(zmq.PUSH)
connaddress = "tcp://%s:%d" % (config['broker_ip'],
                               config['broker_control_port'])
zsend.connect(connaddress)
logger.info("Connecting to broker at %s" % connaddress)


# Configure the scheduler
# ------------------------------------------------------------------

job_defaults = {
    'coalesce': True,
}

scheduler = BlockingScheduler(job_defaults=job_defaults, logger=logger)

@scheduler.scheduled_job('interval', seconds=config['sleep'],
                         id='watcher-{0}'.format(config['sleep']))
def watch():
    for jdata in mdr.retrieve():
        zsend.send(jdata)

    logger.info('Number of jobs in scheduler: ' \
                '{0}'.format(len(scheduler.get_jobs())))


# Handle Kill Signals Cleanly
# ------------------------------------------------------------------

def killhandle(signum, frame):
    ''' This will close connections cleanly '''
    logger.info("SIGTERM detected, shutting down")
    scheduler.shutdown()
    sys.exit(0)

signal.signal(signal.SIGTERM, killhandle)


# Run the scheduler
# ------------------------------------------------------------------

# Let the workers get started
time.sleep(20)

scheduler.start()
