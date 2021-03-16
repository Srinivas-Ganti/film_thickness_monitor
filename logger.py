# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 21:29:06 2021

@author: shrig
"""
import csv
import os
from HLG103 import HLG1_USB
from time import sleep, time
import RPi.GPIO as GPIO
#@{}
from datetime import datetime


class logger():
    def __init__(self,local_path):
        self.hlg1 = HLG1_USB()
#         self.hlg1.set_zero()
        self.local_path = local_path
        sleep(1)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        self.res = GPIO.add_event_detect(21, GPIO.BOTH,
                                         callback = self.start_live_logger(),
                                         bouncetime = 10)

#     def start_live_logger(self):
#         # Typical single acq time - 28.890013 - 30 us        
#         xs = [] #store trials here (n)
#         ys = [] #store relative distance here
#         
#         i=0
#         # This function is called periodically from FuncAnimation
#         start = time()
#         while True:
#             try:
#                 measurement = self.hlg1.read_all_outputs()
#                 
#                 xs.append(i)
#                 i+=1
#                 ys.append(measurement)
# 
#             except KeyboardInterrupt:
#                 print("""Pressed Ctrl-C\nMeasurement finishing""")
#                 sleep(0.5)
#                 break
#         if xs[-1] > len(ys):
#             xs = xs[:len(ys)]
#         elif len(ys) > xs[-1]:
#             ys = ys[:len(xs)]
#         
#         if len(ys) == len(xs):
#             end = time()
#             print(f"Done: {len(xs)} samples taken in {end - start} seconds")
#             self.hlg1.serialport.close()
#             print("""Closing serial port:""")                   
#         return xs,ys

    def start_live_logger(self):
        # Typical single acq time - 28.890013 - 30 us
        while True:
            self.hlg1.set_zero()
            xs = [] #store trials here (n)
            ys = [] #store relative distance here
            
            i=0
            # This function is called periodically from FuncAnimation
            start = GPIO.input(21)
            delay = 1
            sleep(delay)
            now = GPIO.input(21)
            
            if ((now == 0) and (now == start)):
                start = time()
                while GPIO.input(21) == 0:
                    try:
                        measurement = self.hlg1.read_all_outputs()
                        
                        xs.append(i)
                        i+=1
                        ys.append(measurement)

                    except:
                        if GPIO.input(21) == 1:
                            print("""Button released - Ctrl-C\nMeasurement finishing""")
                            sleep(0.5)
                            break
                        
                if xs[-1] > len(ys):
                    xs = xs[:len(ys)]
                elif len(ys) > xs[-1]:
                    ys = ys[:len(xs)]
                
                if len(ys) == len(xs):
                    end = time()
                    print(f"Done: {len(xs)} samples taken in {end - start} seconds")
                    self.hlg1.serialport.close()
                    print("""Closing serial port:""")
                    GPIO.cleanup()
                    self.export_tdata(self.local_path, xs, ys)




    def export_tdata(self, local_path, xs, ys): 
        date = str(datetime.now())[:10]
        output_folder_name = f"{date}"
        file_export_path = self.save_data_temp(local_path
                                                ,dir_name = output_folder_name)
        self.scandf2csv(xs,ys, file_export_path)

    def scandf2csv(self,xs,ys,csv_path):
        time_now = str(datetime.now())[11:-7]
        name = f"{time_now}".replace(":","-")
        with open(csv_path+'/'+name+'.csv', mode='w') as hlg1_file:      
            print("Writing: " + csv_path+'/'+name+'.csv') 
            file_writer = csv.writer(hlg1_file, delimiter=','
                                     ,lineterminator='\n')
            file_writer.writerow(["Observation","Thickness","Intensity","Output 1","Output 2","Output 3","Alarm"])
            for obs, d in zip(xs, ys):
                file_writer.writerow([obs,-1*d["distance"],d["Intensity"],d["Output 1"],d["Output 2"],d["Output 3"],d["Alarm"]])
        print(f"HLG1 measurement file written to {csv_path}")        
       
    def save_data_temp(self, export_path, dir_name = 'temp_data_dir'):
        dir_name = dir_name
        path = os.path.join(export_path, dir_name)
        try:
            os.mkdir(path)
            print(f"Created Directory : {dir_name}")
        except:
            print("Dir exists, path updated")
        return path  