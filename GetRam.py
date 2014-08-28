#!/usr/bin/python
# Rollcode.com
 
import os 
import RPi.GPIO as GPIO
import time
 
LCD_RS = 25
LCD_E  = 24
LCD_D4 = 23
LCD_D5 = 17
LCD_D6 = 27
LCD_D7 = 22
 
LCD_WIDTH = 16
LCD_CHR = True
LCD_CMD = False
 
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
 
E_PULSE = 0.00005
E_DELAY = 0.00005
 
# I got the getRAMinformations method from PhJulien's post
# From here http://www.raspberrypi.org/phpBB3/viewtopic.php?f=32&t=22180
# Return the RAM informations (unit=kb) in a list                                        
# Index 0: total RAM                                                                
# Index 1: used RAM                                                                 
# Index 2: free RAM                    
                                              
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
 
    GPIO.setmode(GPIO.BCM)       
    GPIO.setup(LCD_E, GPIO.OUT)  
    GPIO.setup(LCD_RS, GPIO.OUT) 
    GPIO.setup(LCD_D4, GPIO.OUT) 
    GPIO.setup(LCD_D5, GPIO.OUT) 
    GPIO.setup(LCD_D6, GPIO.OUT) 
    GPIO.setup(LCD_D7, GPIO.OUT) 
     
    lcd_init()
     
    # Get data
    infoRAM = getRAMinformations()
    totalRAM = round(int(infoRAM[0]) / 1000,1)
    usedRAM = round(int(infoRAM[1]) / 1000,1)
    percentRAM = getRAMpercentage(totalRAM, usedRAM)
 
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("You are using:",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string(str(round(percentRAM,2)) + "% RAM",2) # we need only 2 decimals
 
def lcd_init():
    lcd_byte(0x33,LCD_CMD)
    lcd_byte(0x32,LCD_CMD)
    lcd_byte(0x28,LCD_CMD)
    lcd_byte(0x0C,LCD_CMD)  
    lcd_byte(0x06,LCD_CMD)
    lcd_byte(0x01,LCD_CMD)  
 
def lcd_string(message,style):
    # Send string to display
    # style=1 Left justified
    # style=2 Centered
    # style=3 Right justified
     
    if style==1:
        message = message.ljust(LCD_WIDTH," ")  
    elif style==2:
        message = message.center(LCD_WIDTH," ")
    elif style==3:
        message = message.rjust(LCD_WIDTH," ")
     
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)
 
def lcd_byte(bits, mode):
    GPIO.output(LCD_RS, mode) 
     
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x10==0x10:
        GPIO.output(LCD_D4, True)
    if bits&0x20==0x20:
        GPIO.output(LCD_D5, True)
    if bits&0x40==0x40:
        GPIO.output(LCD_D6, True)
    if bits&0x80==0x80:
        GPIO.output(LCD_D7, True)
     
    time.sleep(E_DELAY)    
    GPIO.output(LCD_E, True)  
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)  
    time.sleep(E_DELAY)      
     
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x01==0x01:
        GPIO.output(LCD_D4, True)
    if bits&0x02==0x02:
        GPIO.output(LCD_D5, True)
    if bits&0x04==0x04:
        GPIO.output(LCD_D6, True)
    if bits&0x08==0x08:
        GPIO.output(LCD_D7, True)
     
    time.sleep(E_DELAY)    
    GPIO.output(LCD_E, True)  
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)  
    time.sleep(E_DELAY)   
     
if __name__ == '__main__':
  main()
