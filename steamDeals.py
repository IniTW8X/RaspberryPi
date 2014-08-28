#!/usr/bin/python
# Rollcode.com
import feedparser
import time
import RPi.GPIO as GPIO
  
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
 
def getDeals():
    dealsXML = feedparser.parse("http://www.steamprices.com/xml/rss/pricetracker_eu_discounts.xml")
    return dealsXML
 
def main():
    GPIO.setmode(GPIO.BCM)       
    GPIO.setup(LCD_E, GPIO.OUT)  
    GPIO.setup(LCD_RS, GPIO.OUT) 
    GPIO.setup(LCD_D4, GPIO.OUT) 
    GPIO.setup(LCD_D5, GPIO.OUT) 
    GPIO.setup(LCD_D6, GPIO.OUT) 
    GPIO.setup(LCD_D7, GPIO.OUT) 
  
    lcd_init()
    dealsData = getDeals()
 
    for oneDeal in dealsData.entries:
        time.sleep(5)
        # [17:] this will cut out the Discount x% from the string
        # We only need the name of the game and the price after the discount
        firstLine =  oneDeal.title[17:45] 
        secondLine =  oneDeal.title[-9:] 
        lcd_byte(LCD_LINE_1, LCD_CMD)
        lcd_string(firstLine,1) # Game name
        lcd_byte(LCD_LINE_2, LCD_CMD)
        lcd_string(secondLine,1) # Game price
  
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
