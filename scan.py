# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 15:28:19 2021

@author: shrig
"""
import RPi.GPIO as GPIO
from time  import sleep
from logger import logger as log

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)


l = log()

save_path = "/home/pi/Documents/HLG1/SSHTx/"

x, y = l.start_live_logger()


l.export_tdata(save_path, x,y)