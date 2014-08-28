#!/usr/bin/python
# Rollcode.com
# lcdDisplay class used for writing text on a Raspberry Pi LCD
 
import RPi.GPIO as GPIO
import time
import os
 
class lcdDisplay:
 
    # Define GPIO to LCD mapping
    LCD_RS = 25
    LCD_E  = 24
    LCD_D4 = 23
    LCD_D5 = 17
    LCD_D6 = 27
    LCD_D7 = 22
    #LED_ON = 15
 
    # Define some device constants
    LCD_WIDTH = 16    # Maximum characters per line
    LCD_CHR = True
    LCD_CMD = False
 
    LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
    LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
 
    # Timing constants
    E_PULSE = 0.00005
    E_DELAY = 0.00005
 
    def __init__(self):
        # Main program block
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)            # Use BCM GPIO numbers
        GPIO.setup(self.LCD_E, GPIO.OUT)  # E
        GPIO.setup(self.LCD_RS, GPIO.OUT) # RS
        GPIO.setup(self.LCD_D4, GPIO.OUT) # DB4
        GPIO.setup(self.LCD_D5, GPIO.OUT) # DB5
        GPIO.setup(self.LCD_D6, GPIO.OUT) # DB6
        GPIO.setup(self.LCD_D7, GPIO.OUT) # DB7
	GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button 
 
        # Initialise display
        self.lcd_byte(0x33,self.LCD_CMD)
        self.lcd_byte(0x32,self.LCD_CMD)
        self.lcd_byte(0x28,self.LCD_CMD)
        self.lcd_byte(0x0C,self.LCD_CMD)
        self.lcd_byte(0x06,self.LCD_CMD)
        self.lcd_byte(0x01,self.LCD_CMD)
 
    def printFirstLine(self, message, style):
 
        if( style == 1 or style == 2 or style == 3):
            self.lcd_byte(self.LCD_LINE_1, self.LCD_CMD)
            self.lcd_string(message,style)
        elif(style == 4):
            str_pad = " " * 16
            my_long_string = str(message)
            my_long_string = str_pad + my_long_string
            for i in range (0, len(my_long_string)):
                self.lcd_byte(self.LCD_LINE_1, self.LCD_CMD)
                lcd_text = my_long_string[i:(i+15)]
                self.lcd_string(lcd_text,1)
                time.sleep(0.4)
            self.lcd_byte(self.LCD_LINE_1, self.LCD_CMD)
            self.lcd_string(str_pad,1)
        else:
            print("No such format style")
 
 
    def printSecondLine(self, message, style):
 
        if( style == 1 or style == 2 or style == 3):
            self.lcd_byte(self.LCD_LINE_2, self.LCD_CMD)
            self.lcd_string(message,style)
        elif(style == 4):
            str_pad = " " * 16
            my_long_string = str(message)
            my_long_string = str_pad + my_long_string
            for i in range (0, len(my_long_string)):
                self.lcd_byte(self.LCD_LINE_2, self.LCD_CMD)
                lcd_text = my_long_string[i:(i+15)]
                self.lcd_string(lcd_text,1)
                time.sleep(0.4)
            self.lcd_byte(self.LCD_LINE_2, self.LCD_CMD)
            self.lcd_string(str_pad,1)
        else:
            print("No such format style")
 
    def lcd_string(self, message,style):
        # Send string to display
        # style=1 Left justified
        # style=2 Centred
        # style=3 Right justified
 
        if style==1:
            message = message.ljust(self.LCD_WIDTH," ")
        elif style==2:
            message = message.center(self.LCD_WIDTH," ")
        elif style==3:
            message = message.rjust(self.LCD_WIDTH," ")
 
        for i in range(self.LCD_WIDTH):
            self.lcd_byte(ord(message[i]),self.LCD_CHR)
 
    def lcd_byte(self, bits, mode):
        # Send byte to data pins
        # bits = data
        # mode = True  for character
        #        False for command
 
        GPIO.output(self.LCD_RS, mode) # RS
 
        # High bits
        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits&0x10==0x10:
            GPIO.output(self.LCD_D4, True)
        if bits&0x20==0x20:
            GPIO.output(self.LCD_D5, True)
        if bits&0x40==0x40:
            GPIO.output(self.LCD_D6, True)
        if bits&0x80==0x80:
            GPIO.output(self.LCD_D7, True)
 
        # Toggle 'Enable' pin
        time.sleep(self.E_DELAY)
        GPIO.output(self.LCD_E, True)
        time.sleep(self.E_PULSE)
        GPIO.output(self.LCD_E, False)
        time.sleep(self.E_DELAY)
 
        # Low bits
        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits&0x01==0x01:
            GPIO.output(self.LCD_D4, True)
        if bits&0x02==0x02:
            GPIO.output(self.LCD_D5, True)
        if bits&0x04==0x04:
            GPIO.output(self.LCD_D6, True)
        if bits&0x08==0x08:
            GPIO.output(self.LCD_D7, True)
 
        # Toggle 'Enable' pin
        time.sleep(self.E_DELAY)
        GPIO.output(self.LCD_E, True)
        time.sleep(self.E_PULSE)
        GPIO.output(self.LCD_E, False)
        time.sleep(self.E_DELAY)
 
# Original code for this script is from here
# https://github.com/JochenB/rpisysinfo
def getUptime():
        dataFile       = open("/proc/uptime")
        # In contents[0] we store the Raspberry Pi
        # Uptime in unix time format
        contents       = dataFile.read().split()
        dataFile.close()
        unixTime       = float(contents[0])
        minute         = 60
        hour           = minute * 60
        day            = hour * 24
        days           = int(unixTime / day)
        hours          = int((unixTime % day) / hour)
        minutes        = int((unixTime % hour) / minute)
        seconds        = int(unixTime % minute)
 
        raspberryUptime = ''
        if days > 0:
                raspberryUptime += str(days) + 'd'
        if len (raspberryUptime) > 0 or hours > 0:
                raspberryUptime     += str(hours) + 'h'
        if len (raspberryUptime) > 0 or minutes > 0:
                raspberryUptime     += str(minutes) + 'm'
        raspberryUptime += str( seconds ) + 's'
        return raspberryUptime

def getRAMinformations():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])
 
# Now, using the informations recevied from the getRAMinfo's method
# i build the getRAMpercentage method, so you can show the amount 
# of ram used in percentage
 
def getRAMpercentage(total, used):
    return((used * 100) / total)

def main():
    LCD = lcdDisplay()

    while True:
        infoRAM = getRAMinformations()
        totalRAM = round(int(infoRAM[0]) / 1000,1)
        usedRAM = round(int(infoRAM[1]) / 1000,1)
        percentRAM = getRAMpercentage(totalRAM, usedRAM)
	
	input_state = GPIO.input(18)
	# Uptime
        LCD.printFirstLine('Uptime: ' + getUptime(), 1)
	
	# Button	
	if input_state == 0:
		LCD.printSecondLine('Button pressed', 2)
	else:
       		LCD.printSecondLine(str(round(percentRAM,2)) + "% RAM used", 1)
 
if __name__ == '__main__':
  main()
