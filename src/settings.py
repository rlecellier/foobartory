import logging
import os
import pathlib

import getconf


ROBOT_NAME = 'robot'
BAR_NAME = 'bar'
CURRENCY_NAME = 'currency'
FOO_NAME = 'foo'
FOOBAR_NAME = 'foobar'


ROOT_DIR = pathlib.Path(__file__).parent.absolute()
ini_config_files = [
    os.path.join(ROOT_DIR, 'config/config.ini'),
    os.path.join(ROOT_DIR, 'config/local_config.ini'), # for dev only, git ignored
]
config = getconf.ConfigGetter('foobartory', ini_config_files)

# Make silent logs to keep foobartory only.
logging.basicConfig(level=logging.INFO)
logging.getLogger("apscheduler").addHandler(logging.NullHandler())
logging.getLogger("apscheduler").setLevel(logging.WARNING)
logging.getLogger("getconf").setLevel(logging.WARNING)

ini_config_files = [
    os.path.join(ROOT_DIR, 'config/actions_config.ini'),
    os.path.join(ROOT_DIR, 'config/local_actions_config.ini'), # for dev only, git ignored
]
actions_config = getconf.ConfigGetter('foobartory', ini_config_files)

# Simulation configuration
TICK_DURATION_IN_SECONDS = config.getfloat('default.tick_duration_in_second', 0.5)
NB_INITIAL_ROBOTS = config.getint('default.nb_initial_robots', 2)
NB_WINING_ROBOTS = config.getint('default.nb_wining_robots', 30)

# Strategy configuration
FOOBAR_STOCK_LIMIT = config.getint('default.foobar_stock_limit', 10)
