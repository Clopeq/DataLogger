# /*****************************************************************************
# * | File        :   ADS1263.py
# * | Author      :   Waveshare team
# * | Function    :   ADS1263 driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2020-12-15
# * | Info        :   
# ******************************************************************************/
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import backend.config as config
import RPi.GPIO as GPIO

# gain
GAIN = {
    'GAIN_1' : 0,   # GAIN   1
    'GAIN_2' : 1,   # GAIN   2
    'GAIN_4' : 2,   # GAIN   4
    'GAIN_8' : 3,   # GAIN   8
    'GAIN_16' : 4,  # GAIN  16
    'GAIN_32' : 5,  # GAIN  32
    'GAIN_64' : 6,  # GAIN  64
    
}
# ADC2 gain
ADC2_GAIN = {
    'GAIN_1'   : 0,    # GAIN  1
    'GAIN_2'   : 1,    # GAIN  2
    'GAIN_4'   : 2,    # GAIN  4
    'GAIN_8'   : 3,    # GAIN  8
    'GAIN_16'  : 4,    # GAIN  16
    'GAIN_32'  : 5,    # GAIN  32
    'GAIN_64'  : 6,    # GAIN  64
    'GAIN_128' : 7,    # GAIN  128
}
# data rate
DRATE = {
    '38400SPS'  : 0xF, 
    '19200SPS'  : 0xE,
    '14400SPS'  : 0xD,
    '7200SPS'   : 0xC,
    '4800SPS'   : 0xB,
    '2400SPS'   : 0xA,
    '1200SPS'   : 0x9,
    '400SPS'    : 0x8,
    '100SPS'    : 0x7,
    '60SPS'     : 0x6,
    '50SPS'     : 0x5,
    '20SPS'     : 0x4,
    '16d6SPS'   : 0x3,
    '10SPS'     : 0x2,
    '5SPS'      : 0x1,
    '2d5SPS'    : 0x0,
}
# ADC2 data rate
ADC2_DRATE = {
    '10SPS'    : 0,
    '100SPS'   : 1,
    '400SPS'   : 2,
    '800SPS'   : 3,
}
# Delay time
DELAY = {
    'DELAY_0s'      : 0,
    'DELAY_8d7us'   : 1,
    'DELAY_17us'    : 2,
    'DELAY_35us'    : 3,
    'DELAY_169us'   : 4,
    'DELAY_139us'   : 5,
    'DELAY_278us'   : 6,
    'DELAY_555us'   : 7,
    'DELAY_1d1ms'   : 8,
    'DELAY_2d2ms'   : 9,
    'DELAY_4d4ms'   : 10,
    'DELAY_8d8ms'   : 11,
}
# DAC out volt
DAC_VOLT = {
    'DAC_VLOT_4_5'      : 0b01001,      #4.5V
    'DAC_VLOT_3_5'      : 0b01000,
    'DAC_VLOT_3'        : 0b00111,
    'DAC_VLOT_2_75'     : 0b00110,
    'DAC_VLOT_2_625'    : 0b00101,
    'DAC_VLOT_2_5625'   : 0b00100,
    'DAC_VLOT_2_53125'  : 0b00011,
    'DAC_VLOT_2_515625' : 0b00010,
    'DAC_VLOT_2_5078125': 0b00001,
    'DAC_VLOT_2_5'      : 0b00000,
    'DAC_VLOT_2_4921875': 0b10001,
    'DAC_VLOT_2_484375' : 0b10010,
    'DAC_VLOT_2_46875'  : 0b10011,
    'DAC_VLOT_2_4375'   : 0b10100,
    'DAC_VLOT_2_375'    : 0b10101,
    'DAC_VLOT_2_25'     : 0b10110,
    'DAC_VLOT_2'        : 0b10111,
    'DAC_VLOT_1_5'      : 0b11000,
    'DAC_VLOT_0_5'      : 0b11001,
}
# registration definition
REG = {
    # Register address, followed by reset the default values
    'REG_ID'        : 0,    # xxh
    'REG_POWER'     : 1,    # 11h
    'REG_INTERFACE' : 2,    # 05h
    'REG_MODE0'     : 3,    # 00h
    'REG_MODE1'     : 4,    # 80h
    'REG_MODE2'     : 5,    # 04h
    'REG_INPMUX'    : 6,    # 01h
    'REG_OFCAL0'    : 7,    # 00h
    'REG_OFCAL1'    : 8,    # 00h
    'REG_OFCAL2'    : 9,    # 00h
    'REG_FSCAL0'    : 10,   # 00h
    'REG_FSCAL1'    : 11,   # 00h
    'REG_FSCAL2'    : 12,   # 40h
    'REG_IDACMUX'   : 13,   # BBh
    'REG_IDACMAG'   : 14,   # 00h
    'REG_REFMUX'    : 15,   # 00h
    'REG_TDACP'     : 16,   # 00h
    'REG_TDACN'     : 17,   # 00h
    'REG_GPIOCON'   : 18,   # 00h
    'REG_GPIODIR'   : 19,   # 00h
    'REG_GPIODAT'   : 20,   # 00h
    'REG_ADC2CFG'   : 21,   # 00h
    'REG_ADC2MUX'   : 22,   # 01h
    'REG_ADC2OFC0'  : 23,   # 00h
    'REG_ADC2OFC1'  : 24,   # 00h
    'REG_ADC2FSC0'  : 25,   # 00h
    'REG_ADC2FSC1'  : 26,   # 40h
}
# comand
CMD = {
    'CMD_RESET'     : 0x06, # Reset the ADC, 0000 011x (06h or 07h)
    'CMD_START1'    : 0x08, # Start ADC1 conversions, 0000 100x (08h or 09h)
    'CMD_STOP1'     : 0x0A, # Stop ADC1 conversions, 0000 101x (0Ah or 0Bh)
    'CMD_START2'    : 0x0C, # Start ADC2 conversions, 0000 110x (0Ch or 0Dh)
    'CMD_STOP2'     : 0x0E, # Stop ADC2 conversions, 0000 111x (0Eh or 0Fh)
    'CMD_RDATA1'    : 0x12, # Read ADC1 data, 0001 001x (12h or 13h)
    'CMD_RDATA2'    : 0x14, # Read ADC2 data, 0001 010x (14h or 15h)
    'CMD_SYOCAL1'   : 0x16, # ADC1 system offset calibration, 0001 0110 (16h)
    'CMD_SYGCAL1'   : 0x17, # ADC1 system gain calibration, 0001 0111 (17h)
    'CMD_SFOCAL1'   : 0x19, # ADC1 self offset calibration, 0001 1001 (19h)
    'CMD_SYOCAL2'   : 0x1B, # ADC2 system offset calibration, 0001 1011 (1Bh)
    'CMD_SYGCAL2'   : 0x1C, # ADC2 system gain calibration, 0001 1100 (1Ch)
    'CMD_SFOCAL2'   : 0x1E, # ADC2 self offset calibration, 0001 1110 (1Eh)
    'CMD_RREG'      : 0x20, # Read registers 001r rrrr (20h+000r rrrr)
    'CMD_RREG2'     : 0x00, # number of registers to read minus 1, 000n nnnn
    'CMD_WREG'      : 0x40, # Write registers 010r rrrr (40h+000r rrrr)
    'CMD_WREG2'     : 0x00, # number of registers to write minus 1, 000n nnnn
}

class ADS1263:
    def __init__(self, gain='GAIN_1', rate='14400SPS', ref=5.0, Mode=0):
        self.rst_pin = config.RST_PIN
        self.cs_pin = config.CS_PIN
        self.drdy_pin = config.DRDY_PIN
        self.ScanMode = 0 # 0 is signeChnnel, 1 is diffChannel
        self.REF = ref # Reference voltage, modify according to actual voltage

        self.tareValue = [0 for i in range(10)]
        self.cal_factor = [1 for i in range(10)]

        self.init_ADC1(gain, rate)

        

    # Hardware reset
    def reset(self):
        config.digital_write(self.rst_pin, GPIO.HIGH)
        config.delay_ms(200)
        config.digital_write(self.rst_pin, GPIO.LOW)
        config.delay_ms(200)
        config.digital_write(self.rst_pin, GPIO.HIGH)
        config.delay_ms(200)
    
    
    def WriteCmd(self, reg):
        config.digital_write(self.cs_pin, GPIO.LOW)#cs  0
        config.spi_writebyte([reg])
        config.digital_write(self.cs_pin, GPIO.HIGH)#cs 1
    
    
    def WriteReg(self, reg, data):
        config.digital_write(self.cs_pin, GPIO.LOW)#cs  0
        config.spi_writebyte([CMD['CMD_WREG'] | reg, 0x00, data])
        config.digital_write(self.cs_pin, GPIO.HIGH)#cs 1
        
        
    def ReadData(self, reg):
        config.digital_write(self.cs_pin, GPIO.LOW)#cs  0
        config.spi_writebyte([CMD['CMD_RREG'] | reg, 0x00])
        data = config.spi_readbytes(1)
        config.digital_write(self.cs_pin, GPIO.HIGH)#cs 1
        return data

    
    # Check Data
    def CheckSum(self, val, byt):
        sum = 0
        mask = 0xff     # 8 bits mask
        while(val) :
            # print(sum, val)
            sum += val & mask   # only add the lower values
            val = val >> 8      # shift down
        sum += 0x9b
        # print(sum, byt)
        return (sum&0xff) ^ byt     # if sum equal byt, this will be 0
    
    
    # waiting for a busy end, just for ADC1
    def WaitDRDY(self):
        i = 0
        while(1):
            i+=1
            if(config.digital_read(self.drdy_pin) == 0):
                break
            if(i >= 400000):
                print ("Time Out ...\r\n")
                break
        
    # Check chip ID, success is return 1
    def ReadChipID(self):
        id = self.ReadData(REG['REG_ID'])
        return id[0] >> 5
    
    
    def SetMode(self, Mode):
        self.ScanMode = Mode
        
        
    #The configuration parameters of ADC, gain and data rate
    def ConfigADC(self, gain, drate):
        MODE2 = 0x80    # 0x80:PGA bypassed, 0x00:PGA enabled
        MODE2 |= (gain << 4) | drate
        self.WriteReg(REG['REG_MODE2'], MODE2)
        if(self.ReadData(REG['REG_MODE2'])[0] == MODE2):
            print("REG_MODE2 success")
        else:
            print("REG_MODE2 unsuccess")

        REFMUX = 0x24   # 0x00:+-2.5V as REF, 0x24:VDD,VSS as REF
        self.WriteReg(REG['REG_REFMUX'], REFMUX)
        if(self.ReadData(REG['REG_REFMUX'])[0] == REFMUX):
            print("REG_REFMUX success")
        else:
            print("REG_REFMUX unsuccess")
            
        MODE0 = DELAY['DELAY_35us']
        self.WriteReg(REG['REG_MODE0'], MODE0)
        if(self.ReadData(REG['REG_MODE0'])[0] == MODE0):
            print("REG_MODE0 success")
        else:
            print("REG_MODE0 unsuccess")

        MODE1 = 0x84    # Digital Filter; 0x84:FIR, 0x64:Sinc4, 0x44:Sinc3, 0x24:Sinc2, 0x04:Sinc1
        self.WriteReg(REG['REG_MODE1'], MODE1)
        if(self.ReadData(REG['REG_MODE1'])[0] == MODE1):
            print("REG_MODE1 success")
        else:
            print("REG_MODE1 unsuccess")

    #The configuration parameters of ADC2, gain and data rate
    def ConfigADC2(self, gain, drate):
        ADC2CFG = 0x20          # REF, 0x20:VAVDD and VAVSS, 0x00:+-2.5V
        ADC2CFG |= (drate << 6) | gain
        self.WriteReg(REG['REG_ADC2CFG'], ADC2CFG)
        if(self.ReadData(REG['REG_ADC2CFG'])[0] == ADC2CFG):
            print("REG_ADC2CFG success")
        else:
            print("REG_ADC2CFG unsuccess")
            
        MODE0 = DELAY['DELAY_35us']
        self.WriteReg(REG['REG_MODE0'], MODE0)
        if(self.ReadData(REG['REG_MODE0'])[0] == MODE0):
            print("REG_MODE0 success")
        else:
            print("REG_MODE0 unsuccess")
            

    # Set ADC1 Measuring channel
    def SetChannel(self, channel):
        if channel > 10:
            return 0
        INPMUX = (channel << 4) | 0x0a
        self.WriteReg(REG['REG_INPMUX'], INPMUX)
        if(self.ReadData(REG['REG_INPMUX'])[0] == INPMUX):
            # print("REG_INPMUX success")
            pass
        else:
            print("REG_INPMUX unsuccess")


    # Set ADC2 Measuring channel
    def SetChannel_ADC2(self, channel):
        if channel > 10:
            return 0
        INPMUX = (channel << 4) | 0x0a
        self.WriteReg(REG['REG_ADC2MUX'], INPMUX)
        if(self.ReadData(REG['REG_ADC2MUX'])[0] == INPMUX):
            # print("REG_ADC2MUX success")
            pass
        else:
            print("REG_ADC2MUX unsuccess")
            

    # Set ADC1 Measuring differential channel
    def SetDiffchannel(self, channel):
        if channel == 0:
            INPMUX = (0<<4) | 1     #Diffchannel    AIN0-AIN1
        elif channel == 1:
            INPMUX = (2<<4) | 3     #Diffchannel    AIN2-AIN3
        elif channel == 2:
            INPMUX = (4<<4) | 5     #Diffchannel    AIN4-AIN5
        elif channel == 3:
            INPMUX = (6<<4) | 7     #Diffchannel    AIN6-AIN7
        elif channel == 4:
            INPMUX = (8<<4) | 9     #Diffchannel    AIN8-AIN9
        self.WriteReg(REG['REG_INPMUX'], INPMUX)
        if(self.ReadData(REG['REG_INPMUX'])[0] == INPMUX):
            # print("REG_INPMUX success")
            pass
        else:
            print("REG_INPMUX unsuccess")
            

    # Set ADC2 Measuring differential channel
    def SetDiffchannel_ADC2(self, channel):
        if channel == 0:
            INPMUX = (0<<4) | 1     #Diffchannel    AIN0-AIN1
        elif channel == 1:
            INPMUX = (2<<4) | 3     #Diffchannel    AIN2-AIN3
        elif channel == 2:
            INPMUX = (4<<4) | 5     #Diffchannel    AIN4-AIN5
        elif channel == 3:
            INPMUX = (6<<4) | 7     #Diffchannel    AIN6-AIN7
        elif channel == 4:
            INPMUX = (8<<4) | 9     #Diffchannel    AIN8-AIN9
        self.WriteReg(REG['REG_ADC2MUX'], INPMUX)
        if(self.ReadData(REG['REG_ADC2MUX'])[0] == INPMUX):
            # print("REG_ADC2MUX success")
            pass
        else:
            print("REG_ADC2MUX unsuccess")
            

    # Device initialization (ADC1)
    def init_ADC1(self, gain='GAIN_1', rate='14400SPS'):
        if (config.module_init() != 0):
            return -1
        self.reset()
        id = self.ReadChipID()
        if id == 0x01 :
            print("ID Read success  ")
        else:
            print("ID Read failed   ")
            return -1
        self.WriteCmd(CMD['CMD_STOP1'])
        self.ConfigADC(GAIN[gain], DRATE[rate])
        self.WriteCmd(CMD['CMD_START1'])
        return 0
        

    # Device initialization (ADC2)
    def init_ADC2(self, gain='GAIN_1', rate='400SPS'):
        if (config.module_init() != 0):
            return -1
        self.reset()
        id = self.ReadChipID()
        if id == 0x01 :
            print("ID Read success  ")
        else:
            print("ID Read failed   ")
            return -1
        self.WriteCmd(CMD['CMD_STOP2'])
        self.ConfigADC2(ADC2_GAIN[gain], ADC2_DRATE[rate])
        return 0

        
    # Read ADC data
    def Read_ADC_Data(self):
        config.digital_write(self.cs_pin, GPIO.LOW)#cs  0
        while(1):
            config.spi_writebyte([CMD['CMD_RDATA1']])
            # config.delay_ms(10)
            if(config.spi_readbytes(1)[0] & 0x40 != 0):
                break
        buf = config.spi_readbytes(5)
        config.digital_write(self.cs_pin, GPIO.HIGH)#cs 1
        read  = (buf[0]<<24) & 0xff000000
        read |= (buf[1]<<16) & 0xff0000
        read |= (buf[2]<<8) & 0xff00
        read |= (buf[3]) & 0xff
        CRC = buf[4]
        # print(read, CRC)
        if(self.CheckSum(read, CRC) != 0):
            print("ADC1 data read error!")
        return read
 
 
    # Read ADC2 data
    def Read_ADC2_Data(self):
        read = 0
        config.digital_write(self.cs_pin, GPIO.LOW)#cs  0
        while(1):
            config.spi_writebyte([CMD['CMD_RDATA2']])
            # config.delay_ms(10)
            if(config.spi_readbytes(1)[0] & 0x80 != 0):
                break
        buf = config.spi_readbytes(5)
        config.digital_write(self.cs_pin, GPIO.HIGH)#cs 1
        read |= (buf[0]<<16) & 0xff0000
        read |= (buf[1]<<8) & 0xff00
        read |= (buf[2]) & 0xff
        CRC = buf[4]
        if(self.CheckSum(read, CRC) != 0):
            print("ADC2 data read error!")
        return read
        
        
    # Read ADC1 specified channel data
    def GetChannelValue(self, Channel):
        if(self.ScanMode == 0):# 0  Single-ended input 10 channel Differential input 5 channel 
            if(Channel>10):
                print("The number of channels must be less than 10")
                return 0
            self.SetChannel(Channel)
            self.WaitDRDY()
            Value = self.Read_ADC_Data()
        else:
            if(Channel>4):
                print("The number of channels must be less than 5")
                return 0
            self.SetDiffchannel(Channel)
            self.WaitDRDY()
            Value = self.Read_ADC_Data()
        return Value


    # Read ADC2 specified channel data
    def GetChannelValue_ADC2(self, Channel):
        if(self.ScanMode == 0):# 0  Single-ended input 10 channel Differential input 5 channel
            if(Channel>10):
                print("The number of channels must be less than 10")
                return 0
            self.SetChannel_ADC2(Channel)
            # config.delay_ms(2)
            self.WriteCmd(CMD['CMD_START2'])
            # config.delay_ms(2)
            Value = self.Read_ADC2_Data()
        else:
            if(Channel>4):
                print("The number of channels must be less than 5")
                return 0
            self.SetDiffchannel_ADC2(Channel)
            # config.delay_ms(2) 
            self.WriteCmd(CMD['CMD_START2'])
            # config.delay_ms(2) 
            Value = self.Read_AD2C_Data()
        return Value
        
    def read(self, channel, raw=False):
        ref = self.REF

        result = -1
        raw_value = self.GetChannelValue(channel)

        if(raw_value>>31 == 1):
            result = -(ref*2 - raw_value * ref / 0x80000000)
        else:
            result = raw_value * ref / 0x7fffffff # 32bit

        if raw:
            return result
        else:
            return self.cal_factor[channel] * (result + self.tareValue[channel])
        
    def tare(self, channel, value = 0):
        self.tareValue[channel] = -self.read(channel, True)
        return self.tareValue[channel]
    
    def calibrate(self, channel, actualValue):
        self.cal_factor[channel] = actualValue/self.read(channel, True)
        return self.cal_factor[channel]

    def setRef(self, ref):
        self.REF = ref
        return self.REF

    def read2(self, channel, ref=None):
        if ref is None:
            ref = self.REF

        result = -1
        raw_value = self.GetChannelValue(channel)
        
        if(raw_value>>23 == 1):
            result = -(ref*2 - raw_value * ref / 0x800000)
        else:
            result = raw_value * ref / 0x7fffff # 24bit

        return result

    def GetAll(self, List):
        ADC_Value = []
        for i in List:
            ADC_Value.append(self.GetChannelValue(i))
        return ADC_Value
          
          
    def GetAll_ADC2(self):
        ADC_Value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(0, 10, 1):
            ADC_Value[i] = self.GetChannelValue_ADC2(i)
            self.WriteCmd(CMD['CMD_STOP2'])
            config.delay_ms(20) 
        return ADC_Value
        
        
    def RTD_Test(self):
        Delay = DELAY['DELAY_8d8ms']
        Gain = GAIN['GAIN_1']
        Drate = DRATE['20SPS']
        
        #MODE0 (CHOP OFF)
        MODE0 = Delay 
        self.WriteReg(REG['REG_MODE0'], MODE0) 
        config.delay_ms(1) 

        #(IDACMUX) IDAC2 AINCOM,IDAC1 AIN3
        IDACMUX = (0x0a<<4) | 0x03 
        self.WriteReg(REG['REG_IDACMUX'], IDACMUX) 
        config.delay_ms(1) 

        #((IDACMAG)) IDAC2 = IDAC1 = 250uA
        IDACMAG = (0x03<<4) | 0x03 
        self.WriteReg(REG['REG_IDACMAG'], IDACMAG) 
        config.delay_ms(1) 

        MODE2 = (Gain << 4) | Drate 
        self.WriteReg(REG['REG_MODE2'], MODE2) 
        config.delay_ms(1) 

        #INPMUX (AINP = AIN7, AINN = AIN6)
        INPMUX = (0x07<<4) | 0x06 
        self.WriteReg(REG['REG_INPMUX'], INPMUX) 
        config.delay_ms(1) 

        # REFMUX AIN4 AIN5
        REFMUX = (0x03<<3) | 0x03 
        self.WriteReg(REG['REG_REFMUX'], REFMUX) 
        config.delay_ms(1) 

        #Read one conversion
        self.WriteCmd(CMD['CMD_START1']) 
        config.delay_ms(10) 
        self.WaitDRDY() 
        Value = self.Read_ADC_Data() 
        self.WriteCmd(CMD['CMD_STOP1']) 
    
        return Value
        
    
    def DAC_Test(self, isPositive, isOpen):
        Volt = DAC_VOLT['DAC_VLOT_3']
        
        if(isPositive):
            Reg = REG['REG_TDACP']  # IN6
        else:
            Reg = REG['REG_TDACN']  # IN7

        if(isOpen):
            Value = Volt | 0x80
        else:
            Value = 0x00

        self.WriteReg(Reg, Value) 
        
        
    def Exit(self):
        config.module_exit()
        
### END OF FILE ###

