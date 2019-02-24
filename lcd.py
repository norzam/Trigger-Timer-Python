import threading
from watertimer import *

lcd_menu_position = 0
lcd_menu_position_previous = 9

#Create a thread to run lcd

def glcd_start():

    initGraphicMode()

    while True():
        if lcd_menu_position == 0:
            if lcd_menu_position != lcd_menu_position_previous:
                printString3x5('Time : ', 0, 0)
                lcd_menu_position_previous = lcd_menu_position

            if lcd_menu_position == lcd_menu_position_previous:
                time = str(datetime.datetime.now())
                printString3x5(time, 7, 0)


'''
-------------ate & Time
-------------
current trigger.begin
current trigger.end

solenoid status = closed



'''
