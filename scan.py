# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 15:28:19 2021

@author: shrig
"""

from logger import logger as log
l = log()

save_path = "C:\\Users\\shrig\\OneDrive\\Documents\\SSHTx"

x, y = l.start_live_logger()


l.export_tdata(save_path, x,y)