import serial
import RPi.GPIO as GPIO
from time import sleep


class HLG1_USB:        
    def __init__(self, port = "/dev/ttyUSB0", devnum = 1, baudrate = 115200, timeout = 0.01):
        ## Open the serial port to using DSD USB -RS485 /TTL converter device
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serialport = serial.Serial(self.port, baudrate = self.baudrate, timeout = self.timeout)
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
        
        # Class methods        
           
    def HLG1_com(self, wrdata,  serialport):
        """
        ########## Reset the sensor head
         
        >>>  wrdata = "%01#WRS+00001**\r"

        ########## Turn off laser

        >>> wrdata = "%01#WLR+00000**\r"

        ########## Turn on laser

        >>> wrdata = "%01#WLR+00001**\r"


        ########## Read/Set the sampling rate of sensor 01 (HLG103 S-J)

        >>> wrdata = "%01#RSP**\r"
        >>> wrdata = "%01#WSP00000\r"


        ########## Set/Read the sample averaging on sensor 01

        >>> wrdata = "%01#WAV+00004**\r"
        >>> wrdata = "%01#RAV**\r"

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


# response = HLG1_com(port , "%01#RLA0000103000**\r")