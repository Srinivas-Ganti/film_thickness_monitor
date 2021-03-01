import serial
import RPi.GPIO as GPIO
from time import sleep
#@{}

class HLG1_USB:        
    def __init__(self, port = "/dev/ttyUSB0",
                 devnum = 1, baudrate = 115200,
                 timeout = 0.01):
        
        ## Open the serial port to using DSD USB -RS485 /TTL converter device
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serialport = serial.Serial(self.port,
                                        baudrate = self.baudrate,
                                        timeout = self.timeout)
        self.devnum = devnum
        
    def set_zero(self):
        res = self.HLG1_com(f"%0{self.devnum}#WZS+00001**\r", self.serialport)
        if res == f"%0{self.devnum}$WZS**":
            message = "Zero is set"
            return message
        
    def laser_on(self):
        self.HLG1_com(f"%0{self.devnum}#WLR+00001**\r", self.serialport)
        sleep(0.1)
        
    def laser_off(self):
        self.HLG1_com(f"%0{self.devnum}#WLR+00000**\r", self.serialport)
        sleep(0.1)
        
    def reset(self):
        self.HLG1_com(f"%0{self.devnum}#WRS+00001**\r", self.serialport)
        sleep(0.1)
        
    def read_samplr(self):
        rsamplr_dict = {'%01$RSP+00000**\r':"200 us",
                       '%01$RSP+00001**\r':"500 us",
                       '%01$RSP+00002**\r':"1 ms",
                       '%01$RSP+00003**\r':"2 ms"
                       }
        self.res = self.HLG1_com(f"%0{self.devnum}#RSP**\r", self.serialport)
        print("Sampling at : ", rsamplr_dict[self.res])
        
    def set_samplr(self, cycle):
        wsamplr_dict = {"200 us": f"%0{self.devnum}#WSP+00000**\r",
                        "500 us": f"%0{self.devnum}#WSP+00001**\r",
                        "1 ms": "f%0{self.devnum}#WSP+00002**\r",
                        "2 ms": f"%0{self.devnum}#WSP+00003**\r"
                       }
        
        self.res = self.HLG1_com(wsamplr_dict[cycle], self.serialport)      

    def read_avgset(self):
        ravg_dict = {f"%0{self.devnum}$RAV+00000**\r": "Once",
                     f"%0{self.devnum}$RAV+00001**\r": "4",
                     f"%0{self.devnum}$RAV+00002**\r": "16",
                     f"%0{self.devnum}$RAV+00003**\r": "64",
                     f"%0{self.devnum}$RAV+00004**\r": "256",
                     f"%0{self.devnum}$RAV+00005**\r": "1024"
                     }
        self.res = self.HLG1_com(f"%0{self.devnum}#RAV**\r", self.serialport)        
        return ravg_dict[self.res]
        
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
        #print(self.res)
        
    def HLG1_com(self, wrdata,  serialport):
        """



        ########## Read current measurement value on sensor 01

        >>> wrdata = "%01#RMD**\r"

        ########## Reading all “logic” outputs of judgment output
        selection for sensor 01 in the RS-422 handshake
        mode or the RS-485 multi-mode

        >>> wrdata = "%01#RMB**\r"

        ########## Set zero - distance

        >>> wrdata = "%01#WZS+00001**\r"

        ########## Save settings

        >>>  wrdata = "%01#WWR+00001**\r"

        ########## Set/ Read buffering mode

        +00000 for continuous +00001 for trigger

        >>> wrdata = "%01#WBD+00000**\r"
        >>> wrdata = "%01#RBD+00000**\r"

        ########## Read buffering rate

        >>> wrdata = "%01#RBR**\r"

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