import serial
import RPi.GPIO as GPIO
from time import sleep
import numpy as np

class HLG1_USB:        
    def __init__(self, port = "/dev/ttyUSB0",
                 devnum = 1, baudrate = 115200,
                 timeout = 0.01):
        
        """
        Initialize RS485-USB serial com control interface.
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serialport = serial.Serial(self.port,
                                        baudrate = self.baudrate,
                                        timeout = self.timeout)
        self.devnum = devnum
        self.trcondict = {"+00000" : "At timing input ON",
                          "+00001" : "At or higher than threshold",
                          "+00002" : "Lower than threshold",
                          "+00003" : "At alarm occured",
                          "+00004" : "At alarm released"
                          }
        self.outsta_dict = {"+00000":"OFF",
                       "+00001":"ON",
                       }
        self.error_dict = {"01" :"""Command error.\n
                                  - The command is undefined. Check value format""",
                           "02" : """Address error.\n
                                     - The start address is larger than the end address or the address is larger
                                     than 999999 when the RDD or WDD command is executed.\n
                                     - The address length has not reached the prescribed length when the RDD or WDD command is executed.""",
                           "03" : """Data error.\n - The data length does not correspond to the command.\n
                                     - The data length has not reached the prescribed length.""",
                           "04" : """BCC error. \n
                                     - BCC check was not conformable.""",
                           "11" : """Communication error - \n - A parity error occurred during data reception.\n
                                     - A framing error occurred during data reception.\n
                                     -  An overrun error occurred during data reception.\n""",
                           "21": """Control flow error. \n
                                    - The system is in setting mode.""",
                           "22": """Execution error. \n
                                    - Calibration or analog scaling is not executable.""",
                           "31": """Buffering condition error 1: \n
                                    - An attempt was made to make a buffering setting change without stopping buffering.""",
                           "32" : "Buffering condition error 2: An attempt was made to start buffering with an inadequate buffering setting.",
                           "33" : """Buffering condition error 3:\n - Data was read after buffering operation started.\n
                                   - Data was read while the system was not in the accumulation completed status.\n
                                   - Data in excess of the final data point was specified and read."""
                           }    
 
    def reset(self):
        self.res = self.HLG1_com(f"%0{self.devnum}#WRS+00001**\r", self.serialport)
        if "WRS" in self.res:
            print("Initialized")
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)                    
        sleep(0.1)
        
################ READ OUTPUTS        

    def read_alarm(self):
        alrsta_dict = {"+00000":"OFF",
                       "+00001":"ON",
                       }
        
        self.res = self.HLG1_com(f"%0{self.devnum}#ROA**\r", self.serialport)
        r = self.res.split("ROA")[1].split("**")[0]
        if "ROA" in self.res:
            print("Alarm status:", alrsta_dict[r])
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)
      
    def read_out1(self):
        self.res = self.HLG1_com(f"%0{self.devnum}#RZA**\r", self.serialport)
        r = self.res.split("RZA")[1].split("**")[0]
        if "RZA" in self.res:
            print("Out1 status:", self.outsta_dict[r])
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)
        
    def read_out2(self):
        self.res = self.HLG1_com(f"%0{self.devnum}#RZB**\r", self.serialport)
        r = self.res.split("RZB")[1].split("**")[0]
        if "RZB" in self.res:
            print("Out2 status:",  self.outsta_dict[r])
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)

    def read_out3(self):
        self.res = self.HLG1_com(f"%0{self.devnum}#RZC**\r", self.serialport)
        r = self.res.split("RZC")[1].split("**")[0]
        if "RZC" in self.res:
            print("Out3 status:",  self.outsta_dict[r])
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)        
 
 ################ MEASUREMENT SETTINGS
        
    def read_zeroSetAmt(self):
        self.res = self.HLG1_com(f"%0{self.devnum}#RZV**\r", self.serialport)
        if "RZV" in self.res:
            print(self.res)
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)
        
    def read_span(self):
        self.res = self.HLG1_com(f"%0{self.devnum}#RMK**\r", self.serialport)
        if "RMK" in self.res:
            print(self.res)
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)
        
    def set_span(self, span = "+10000"):
        self.res = self.HLG1_com(f"%0{self.devnum}#WMK{span}**\r", self.serialport)
        if "WMK" in self.res:
            print(self.res)
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)        
        
    def set_zero(self):
        self.res = self.HLG1_com(f"%0{self.devnum}#WZS+00001**\r", self.serialport)
        if self.res == f"%0{self.devnum}$WZS**\r":
            print("Zero is set")
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)
    
    def read_samplr(self):
        rsamplr_dict = {'%01$RSP+00000**\r':"200 us",
                       '%01$RSP+00001**\r':"500 us",
                       '%01$RSP+00002**\r':"1 ms",
                       '%01$RSP+00003**\r':"2 ms"
                       }
        self.sampr = self.HLG1_com(f"%0{self.devnum}#RSP**\r", self.serialport)
        print("Sampling at : ", rsamplr_dict[self.sampr])
        
    def set_samplr(self, cycle):
        wsamplr_dict = {"200 us": f"%0{self.devnum}#WSP+00000**\r",
                        "500 us": f"%0{self.devnum}#WSP+00001**\r",
                        "1 ms": "f%0{self.devnum}#WSP+00002**\r",
                        "2 ms": f"%0{self.devnum}#WSP+00003**\r"
                       }
        
        self.sampr = self.HLG1_com(wsamplr_dict[cycle], self.serialport)      

    def read_avgset(self):
        ravg_dict = {f"%0{self.devnum}$RAV+00000**\r": "Once",
                     f"%0{self.devnum}$RAV+00001**\r": "4",
                     f"%0{self.devnum}$RAV+00002**\r": "16",
                     f"%0{self.devnum}$RAV+00003**\r": "64",
                     f"%0{self.devnum}$RAV+00004**\r": "256",
                     f"%0{self.devnum}$RAV+00005**\r": "1024"
                     }
        self.avg = self.HLG1_com(f"%0{self.devnum}#RAV**\r", self.serialport)        
        return ravg_dict[self.avg]
        
    def write_avgset(self,avg):
        wavg_dict = {"Once": f"%0{self.devnum}#WAV+00000**\r",
                     "4" : f"%0{self.devnum}#WAV+00001**\r",
                     "16" : f"%0{self.devnum}#WAV+00002**\r",
                     "64" : f"%0{self.devnum}#WAV+00003**\r",
                     "256" : f"%0{self.devnum}#WAV+00004**\r",
                     "1024": f"%0{self.devnum}#WAV+00005**\r"
                     }
        self.res = self.HLG1_com(wavg_dict[avg], self.serialport)
        print("Averaging set to", self.read_avgset())
            
################ LASER CONTROL
        
    def laser_on(self):
        self.lr = self.HLG1_com(f"%0{self.devnum}#WLR+00001**\r", self.serialport)
        if self.lr == f"%0{self.devnum}$WLR**\r":
            print("Laser on")
        else:
            errc = self.lr.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)
        
    def laser_off(self):
        self.lr = self.HLG1_com(f"%0{self.devnum}#WLR+00000**\r", self.serialport)
        if self.lr == f"%0{self.devnum}$WLR**\r":
            print("Laser off")
        else:
            errc = self.lr.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)

################ DATA ACQUISITION
            
    def DataReadNormal(self, head = "00001", end = "03000"):  
        self.res = self.HLG1_com(f"%0{self.devnum}#RLA{head}{end}**\r", self.serialport)
        if "RLA" in self.res:
            r = self.res
            raw = r.split("RLA")[1].split("**")[0]
            print("Accumulated data : \n",
                  raw)
            if "-" in raw or "+" in raw:
                raw_p = r.split("RLA")[1].split("**")[0].split("-")[0].split("+")[1:]
                raw_p = np.array([float(i) for i in raw_p])
                return raw_p   
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)        
        
    def read_measurement(self):
        self.res = self.HLG1_com(f"%0{self.devnum}#RMD**\r", self.serialport)
        if 'RMD' in self.res:
            print(f"Measurement received ({self.read_avgset()} avgs):")
            r = self.res
            raw = r.split("RMD")[1].split("**")[0][
                :-1]+'.'+r.split("RMD")[
                    1].split("**")[0][-1]
            print(raw + " um")
            return raw
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)
            return None
                  
            
    def read_all_outputs(self):
        self.res = self.HLG1_com(f"%0{self.devnum}#RMB**\r", self.serialport)
        if 'RMB' in self.res:
            print(f"Measurements received ({self.read_avgset()} avgs):")
            r = self.res
            print("distance: ", r.split("RMB")[1].split("**")[0][:8],"\n",
                  "Intensity: ", r.split("RMB")[1].split("**")[0][8:12],"\n",
                  "Output 1: ", r.split("RMB")[1].split("**")[0][12:13],"\n",
                  "Output 2: ", r.split("RMB")[1].split("**")[0][13:14],"\n",
                  "Output 3: ", r.split("RMB")[1].split("**")[0][14:15], "\n",
                  "Alarm: ", r.split("RMB")[1].split("**")[0][15:16], "\n")
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)
        
################ BUFFER CONTROL, SETTINGS

    def save_settings(self):
        self.res = self.HLG1_com(f"%0{self.devnum}#WWR+00001**\r", self.serialport)
        if self.res == f"%0{self.devnum}$WWR**\r":
            print("Settings saved")
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)   

    def readAccAmt(self):
        self.res = self.HLG1_com(f"%0{self.devnum}#RBC**\r",
                                 self.serialport)
        if "RBC" in self.res:
            r = self.res
            raw = r.split("RBC")[1].split("**")[0]
            print("Read Accumulation amount :",
                  raw)                                 
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)
        
    def setAccAmt(self, val = "+03000"):
        self.res = self.HLG1_com(f"%0{self.devnum}#WBC{val}**\r",
                                 self.serialport)
        if "WBC" in self.res:
            r = self.res
            raw = r.split("WBC")[1].split("**")[0]
            print("Set Accumulation amount :",
                  val)                                 
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)                                                                                        
                                                  
    def set_bufferMode(self, mode):
        bmodict = {"cont": f"%0{self.devnum}#WBD+00000**\r",
                   "trig" : f"%0{self.devnum}#WBD+00001**\r"
                   } 
        self.res = self.HLG1_com(bmodict[mode], self.serialport)
        if self.res == f"%0{self.devnum}$WBD**\r":
            print("Buffering mode set - ", mode)
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)
        
    def read_bufferMode(self):
        rbmodict = {f"%0{self.devnum}$RBD+00000**\r":"cont",
                   f"%0{self.devnum}$RBD+00001**\r":"trig"
                   } 
        self.res = self.HLG1_com(f"%0{self.devnum}#RBD**\r", self.serialport)
        if "RBD" in self.res:
            print(f"Buffering mode is - {rbmodict[self.res]}")
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)
            
    def set_bufferRate(self,num_every_65535):
        """Select from 1 (all measurement data), 1/2, 1/4, etc. to 1/65535.
           The buffering rate is set to “1/10” by default.
           If 1/4 is selected for example, measurement data will
           be accumulated once every four sampling cycles."""
           
        self.res = self.HLG1_com(f"%0{self.devnum}#WBR+0000{num_every_65535}**\r",
                                 self.serialport)
        if "WBR" in self.res:
            r = self.res
            self.read_bufferRate()
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)          
                                      
    def read_bufferRate(self):  
        self.res = self.HLG1_com(f"%0{self.devnum}#RBR**\r", self.serialport)
        if "RBR" in self.res:
            r = self.res
            print("Buffering rate is : ",
                  r.split("RBR")[1].split("**")[0], "/65535")
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)
                                      
    def read_bufferStatus(self):
        bstdict = {"+00000":"Not Buffering",
                   "+00001":" Waiting for trigger",
                   "+00002":"Accumulating",
                   "+00003":"Accumulation completed",       
                   } 
        self.res = self.HLG1_com(f"%0{self.devnum}#RTS**\r", self.serialport)
        if "RTS" in self.res:
            
            r = self.res
            status = r.split("RTS")[1].split("**")[0]
            print("Buffering Status :", bstdict[status])   
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)

    def bufferReady(self, set_go = None):
        
        bufRdydict = {"+00000":"Stop",
                   "+00001":" Start",
                      "start": "+00001",
                      "stop": "+00000"
                   } 
        if set_go == None:
            self.res = self.HLG1_com(f"%0{self.devnum}#RBS**\r", self.serialport)
        elif (set_go == "Start") or (set_go == "start")or (set_go == "START")  :
            self.res = self.HLG1_com(f"%0{self.devnum}#WBS{bufRdydict['start']}**\r",
                                     self.serialport)
        elif (set_go == "Stop") or (set_go == "stop")or (set_go == "STOP")  :
            self.res = self.HLG1_com(f"%0{self.devnum}#WBS{bufRdydict['stop']}**\r",
                                     self.serialport)            
        if "RBS" in self.res:
            r = self.res
            status = r.split("RBS")[1].split("**")[0]
            print("Buffer state :", bufRdydict[status])
        elif "WBS" in self.res:
            r = self.res
            status = r.split("WBS")[0]
            print("Buffer action :", set_go)
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)
        

################ TRIGGER CONTROL

        
    def readTriggerCond(self):

        self.res = self.HLG1_com(f"%0{self.devnum}#RTR**\r", self.serialport)
        if "RTR" in self.res:
            r = self.res
            raw = r.split("RTR")[1].split("**")[0]
            print("Trigger condition : ",
                  self.trcondict[raw])                                 
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)

    def setTriggerCond(self, trig_cond):
        wtrcondict = {"0":"+00000",
                     "1":"+00001",
                     "2":"+00002",
                     "3":"+00003",
                     "4":"+00004" }
        self.res = self.HLG1_com(f"%0{self.devnum}#WTR{wtrcondict[trig_cond]}**\r",
                                 self.serialport)
        if "WTR" in self.res:
            r = self.res
            raw = r.split("WTR")[1].split("**")[0]
            print("Trigger condition set: ",
                  self.trcondict[wtrcondict[trig_cond]])                                 
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)
        
    def readThreshold(self):
        self.res = self.HLG1_com(f"%0{self.devnum}#RBL**\r", self.serialport)
        if "RBL" in self.res:
            r = self.res
            raw = r.split("RBL")[1].split("**")[0]
            print("Trigger threshold:",
                  raw)                                 
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)
        
    def setThreshold(self, threshold = "-0000110"):
        self.res = self.HLG1_com(f"%0{self.devnum}#WBL{threshold}**\r",
                                 self.serialport)
        if "WBL" in self.res:
            r = self.res
            raw = r.split("WBL")[1].split("**")[0]
            print("Trigger threshold set:",
                  raw)                                 
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg,"""\n Enter value between-9500000 to
        +9500000 (-950.0000 to 950.0000 [mm])""")        
        sleep(0.1)

    def readTriggerPoint(self):
        self.res = self.HLG1_com(f"%0{self.devnum}#RTP**\r",
                                 self.serialport)
        if "RTP" in self.res:
            r = self.res
            raw = r.split("RTP")[1].split("**")[0]
            print("Read Trigger point :",
                  raw)                                 
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)
        
    def setTriggerPoint(self, val = "+00001"):
        self.res = self.HLG1_com(f"%0{self.devnum}#WTP{val}**\r",
                                 self.serialport)
        if "WTP" in self.res:
            r = self.res
            raw = r.split("WTP")[1].split("**")[0]
            print("Set Trigger point :",
                  val)                                 
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)
        
    def readTriggerDelay(self):
        self.res = self.HLG1_com(f"%0{self.devnum}#RTL**\r",
                                 self.serialport)
        if "RTL" in self.res:
            r = self.res
            raw = r.split("RTL")[1].split("**")[0]
            print("Read Trigger delay :",
                  raw)                                 
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)
        
    def setTriggerDelay(self, val = "+00100"):
        self.res = self.HLG1_com(f"%0{self.devnum}#WTP{val}**\r",
                                 self.serialport)
        if "WTP" in self.res:
            r = self.res
            raw = r.split("WTP")[1].split("**")[0]
            print("Set Trigger delay :",
                  val)                                 
        else:
            errc = self.res.split("!")[0].split("%")[1]
            ermsg = self.error_dict[errc]
            print("Traceback: ", ermsg)        
        sleep(0.1)
        
    def HLG1_com(self, wrdata,  serialport):

        serialport.write(wrdata.encode())
        received_data = serialport.readline()
        if received_data:
            #print(received_data.decode())
            return received_data.decode()
        else:
            sleep(1)
            try:
                HLG1_com(self, wrdata, serialport)
            except:
                print("No response")


"""
To try out functions instantiate the class below and use the IDE/ TERMINAL console
"""
# Uncomment line below for tests
# hlg1 = HLG1_USB()