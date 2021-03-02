import serial
import RPi.GPIO as GPIO
from time import sleep
#@{}

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
 
    def reset(self):
        self.HLG1_com(f"%0{self.devnum}#WRS+00001**\r", self.serialport)
        sleep(0.1)
        
    def set_zero(self):
        self.res = self.HLG1_com(f"%0{self.devnum}#WZS+00001**\r", self.serialport)
        if res == f"%0{self.devnum}$WZS**":
            print("Zero is set")
            
    def laser_on(self):
        self.lr = self.HLG1_com(f"%0{self.devnum}#WLR+00001**\r", self.serialport)
        if self.lr == '%01$WLR**\r':
            print("Laser on")
        else:
            print("error:", self.lr)            
        sleep(0.1)
        
    def laser_off(self):
        self.lr = self.HLG1_com(f"%0{self.devnum}#WLR+00000**\r", self.serialport)
        if self.lr == '%01$WLR**\r':
            print("Laser off")
        else:
            print("error: ", self.lr)
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

    def read_measurement(self):
        self.res = self.HLG1_com(f"%0{self.devnum}#RMD**\r", self.serialport)
        if 'RMD' in self.res:
            print(f"Measurement received ({self.read_avgset()} avgs):")
            r = self.res
            print(r.split("RMD")[1].split("**")[0][
                :-1]+'.'+r.split("RMD")[
                    1].split("**")[0][-1] + " um")
            
    def read_all(self):
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
            
    def save_settings(self):
        self.res = self.HLG1_com(f"%0{self.devnum}#WWR+00001**\r", self.serialport)
        if self.res == f"%0{self.devnum}$WWR**\r":
            print("Settings saved")
        else:
            print("error: ", self.res)
            
    def set_bufferMode(self, mode):
        bmodict = {"cont": f"%0{self.devnum}#WBD+00000**\r",
                   "trig" : f"%0{self.devnum}#WBD+00001**\r"
                   } 
        self.res = self.HLG1_com(bmodict[mode], self.serialport)
        if self.res == f"%0{self.devnum}$WBD**\r":
            print("Buffering mode set - ", mode)
        else:
            print("error: ", self.res)

    def read_bufferMode(self):
        rbmodict = {f"%0{self.devnum}$RBD+00000**\r":"cont",
                   f"%0{self.devnum}$RBD+00001**\r":"trig"
                   } 
        self.res = self.HLG1_com(f"%0{self.devnum}#RBD**\r", self.serialport)
        if "RBD" in self.res:
            print(f"Buffering mode is - {rbmodict[self.res]}")
        else:
            print("error: ", self.res)
            
    def set_bufferRate(self,num_every_65535):
        """Select from 1 (all measurement data), 1/2, 1/4, etc. to 1/65535.
           The buffering rate is set to “1/10” by default.
           If 1/4 is selected for example, measurement data will
           be accumulated once every four sampling cycles."""
           
        self.res = self.HLG1_com(f"%0{self.devnum}#WBR+0000{num_every_65535}**\r", self.serialport)

        if "WBR" in self.res:
            r = self.res
            self.read_bufferRate()
        else:
            print("error: ", self.res)            
                                      
    def read_bufferRate(self):  
        self.res = self.HLG1_com(f"%0{self.devnum}#RBR**\r", self.serialport)
        if "RBR" in self.res:
            r = self.res
            print("Buffering rate is : ",
                  r.split("RBR")[1].split("**")[0], "/65535")
        else:
            print("error: ", self.res)            
                                         
                                         
    def HLG1_com(self, wrdata,  serialport):
        """
        ########## Read/ Write accumulated amount (+00001 to +03000)

        >>> wrdata = "%01#RBC**\r"
        >>> wrdata = "%01#WBC+03000**\r"

        ########## Read/ Write Trigger point (+00001 to +03000)

        >>> wrdata = "%01#RTP**\r"
        >>> wrdata = "%01#WTP**\r"

        ########## Read/ Write Trigger delay (+00000 to +65535)
        >>> wrdata = "%01#RTL**\r"
        >>> wrdata = "%01#WTL**\r"

        ########## Read/ Write trigger conditions

        >>> wrdata = "%01#RTR**\r"
        >>> wrdata = "%01#WTR+00001**\r"

        +00000 - At timing input ON
        +00001 - At or higher than threshold
        +00002 - Lower than threshold
        +00003 - At alarm occured
        +00004 - At alarm released

        ########## Set threshold for Trigger

        -9500000 to
        +9500000 (-950.0000 to 950.0000 [mm])

        >>> wrdata = "%01WBL-000208**\r"
        >>> wrdata = "%01RBL**\r"

        ########## Buffering Operation - Read/ Write status
        stop +00000
        start +00001

        >>> wrdata = "%01#WBS+00001**\r"
        >>> wrdata = "%01#RBS**\r"

        ########## Buffering status readout

        >>> wrdata = "%01#RTS**\r"

        +00000 - Not buffering
        +00001 - Waiting for trigger
        +00002 - Accumulating
        +00003 - Accumulation completed


        ########## Data read (Normal)
        from head - tail buffer memory
        00001 to 03000

        >>> wrdata = "%01#RLA0000103000**\r")



        """
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


hlg1 = HLG1_USB()