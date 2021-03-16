import RPi.GPIO as GPIO
from time import sleep

from logger import logger as log


save_path = "/home/pi/Documents/HLG1/SSHTx/"
while True:
    try:
        
        l = log(local_path = save_path)
    except:
        sleep(5)
        pass
    finally:
        print("Trying again ")
        
        


####################################################