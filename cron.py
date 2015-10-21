#!/usr/bin/python
import os

import random
import time
import datetime

from main import main

dir_name = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir_name)

now = datetime.datetime.now()
if now.hour > 22 or now.hour <= 7:
    print '183R'
    exit(1)

minutes_to_sleep = random.randint(5, 30)
seconds_to_sleep = minutes_to_sleep * 60

time.sleep(seconds_to_sleep)

main()

