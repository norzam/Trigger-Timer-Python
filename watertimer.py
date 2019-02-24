import threading
from glcd12864zw import *
import datetime

trigger_array_position = 0
trigger_status = 0 # 0 no fire, 1 firing



#####################################
# Raspberry Pi Pin Assignment
#####################################




####################################
# GLOBAL LCD VARIABLES
#####################################

lcd_menu_position_current = 0
lcd_menu_position_previous = 10

#####################################


class Trigger:
    def __init__(self, name, hour, minute, sec, end):
        self.name = name
        self.hour = hour
        self.minute = minute
        self.sec = sec
        self.end = end
        print(self.name)

        #create new begin time

        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day

        self.begintime = datetime.datetime(year, month, day, int(self.hour), int(self.minute), int(sec))

        #create new end time

        self.endtime = self.begintime + datetime.timedelta(minutes = int(end))

def trigger_load():
    #will open trigger.txt, load is an object of Trigger class. Return temp2 list.
    print('trigger_load(): running')
    global temp, temp2

    file = open('trigger.txt', 'r')
    temp = []
    temp = file.read().split('\n')
    temp2 = []
    #print(len(temp))
    for i in range(0, len(temp)):

        if temp[i] != '':

            name = 'trigger' + str(i)
            hour, minute, sec, end = temp[i].split(',')

            newTrigger = Trigger(name, hour, minute, sec, end)

            temp2.append(newTrigger)
            #print(newTrigger.begintime)

    file.close()

#####################################
# TRIGGER SORT LOGIC - must run trigger_load()
#####################################
def trigger_sort():

    print('trigger_sort: running')
    global now, temp2
    #will return trigger value closest to current time

    trigger_array_position = 0
    now = datetime.datetime.now()

    for i in range(0, len(temp2)):

        global trigger_array_position

        if now > temp2[i].begintime:
            print(str(temp2[i].name) + ' : ' + str(temp2[i].begintime) + 'value is smaller than time.now')


       # if now < temp2[i].begintime:
       #     print(temp2[i].name + 'is larger than time.now')
       #     trigger_array_position = i

        if now < temp2[i].begintime and temp2[i].begintime < temp2[trigger_array_position].begintime:
            print(temp2[i].name + 'is smaller than' + str(temp2[trigger_array_position].name) + \
                    str(temp2[trigger_array_position].begintime) + 'Setting new trigger_array_position')
            trigger_array_position = i

    print('trigger_sort(): decision : next trigger at ' + str(temp2[trigger_array_position].begintime))


#####################################
# TRIGGER FIRING LOGIC
#####################################
def trigger_firing():
    #check temp2[trigger_array_position].begintime and compare with datetime.datetime.now() to start trigger
    #check temp2[trigger_array_position].endtime and compare with datetime.datetime.now() to stop trigger
    #execute trigger_load() after complete stop trigger
    #execute trigger_sort() after complete stop trigger to get closest trigger value to time.now

    print('trigger_firing() : comparing trigger value with current time :')
    global temp2, trigger_array_position, trigger_status

    previous = datetime.datetime(2011,1,1,1,1)

    while True:

        now = datetime.datetime.now()

        if now.hour == temp2[trigger_array_position].begintime.hour and now.minute == temp2[trigger_array_position].begintime.minute:
            if trigger_status == 0:
                print('trigger detected : Fire')
                trigger_status0 = 1

        if now.hour == temp2[trigger_array_position].endtime.hour and now.minute == temp2[trigger_array_position].endtime.minute:
            if trigger_status == 1:
                print('trigger detected : Cease Fire')
                trigger_status = 0
                trigger_load()
                trigger_sort()

        if trigger_status == 0:
            if previous.second != now.second:
                next_to_firing = temp2[trigger_array_position].begintime - now
                print('Next trigger at : ' + str(temp2[trigger_array_position].begintime) + \
                        ' Seconds countdown to firing '  + str(next_to_firing.seconds) + ' Seconds')
                previous = now

        if trigger_status == 1:
            if previous.second != now.second:
                next_to_firing = temp2[trigger_array_position].endtime - now
                print('Next trigger at : ' + str (temp2[trigger_array_position].endtime) + \
                        ' Seconds countdown to cease fire '+ str(next_to_firing.seconds) + ' Seconds')
                previous = now



def welcome_note():
    print('+------------------------------------------------+')
    print('| Trigger Array by Norzam                        |')
    print('+------------------------------------------------+')


def runtime():
    welcome_note()   # < --
    trigger_load()   # < --  run once
    trigger_sort()   # < --
    trigger_firing() # < --- runtime loop
    glcd_start()

def glcd_start():

    global lcd_menu_position_current, lcd_menu_position_previous

    init()
    clearGraphic()
    initGraphicMode()


    if lcd_menu_position_current != lcd_menu_position_previous:
        print('Writing to screen')
        printString3x5(datetime.datetime.now().ctime(), 0, 0)
        printString3x5('Hello world', 0, 10)
        printString3x5('This is another test', 0, 20)
        lcd_menu_position_previous = lcd_menu_position_current




#####################################
# RUNTIME CALL
#####################################

glcd_start()
runtime()
