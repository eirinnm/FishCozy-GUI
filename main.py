#!/usr/bin/env python3
import datetime
import time
import sys
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.properties import NumericProperty,StringProperty,ListProperty
from kivy.uix.modalview import ModalView
from kivy.uix.slider import Slider
from kivy.uix.checkbox import CheckBox
from kivy.uix.switch import Switch
from kivy.uix.effectwidget import EffectBase 

from FishCozyHAL import FishCozyHAL

if len(sys.argv) < 2:
    print("Usage: main.py serial_port\nSerial_port can be 'auto', or 'false' for a simulation")
    sys.exit()
port = sys.argv[1]
if port == 'auto':
    port = None
if port == 'false':
    port = False

import platform
if platform.system() == 'Linux':
    #Window.fullscreen = True #seems to crash now and not necessary anyway
    pass
else:
    Window.size = (800, 480)




class LineCircle(Widget):
    pass


class RootWidget(BoxLayout):
    pass



class Toggle1(ToggleButton):

    newColor = ListProperty ([0,1,0,1])

    tickmarckColor1 = ListProperty ([51/255, 164/255, 208/255, 1])
    tickmarckColor2 = ListProperty ([51/255, 164/255, 208/255, 1])


    currentPower = NumericProperty(0)
    
    setTemperature = NumericProperty(28)
    setTime = NumericProperty(5)
    setTimeAngle = NumericProperty()

    setTemperature2 = NumericProperty(28)
    setTime2 = NumericProperty(5)
    setTimeAngle2 = NumericProperty()
 
    lapsedTime = NumericProperty()
    lapsedTime2 = NumericProperty()

    labelOffsetY =  -1
    labelOffsetX = -1
    currentTimeAngle = NumericProperty(0)
    seconds=0
    toggled=False
    running = False

    startingTime =.0

    targetTemperature = 28

    isTimePoint2On = False






    def setTimeZero(self):

        self.running = True
        self.ids.running.disabled = False
        self.ids.running.text = 'running'
        self.startingTime = time.clock()
       # print(self.startingTime)
        self.tickmarckColor1 =  ([51/255, 164/255, 208/255, 1])
        self.tickmarckColor2 =  ([51/255, 164/255, 208/255, 0])


    def updateTime(self):



        if self.running:

            
            self.seconds = round(time.clock() - self.startingTime)

        self.currentTimeAngle  = (310/self.setTime2/360)* self.seconds
        self.setTimeAngle = (self.setTime/self.setTime2)*310
       # self.setTimeAngle2 = (self.setTime+self.setTime2)/285 * self.setTime2

        
        

      #  print(self.setTime)

        
 
       #### Timer Updater #####

        if (self.seconds < self.setTime*60):
            self.lapsedTime = round((self.setTime*60 - self.seconds)/60,2)
            self.lapsedTime2 = round((self.setTime2*60 - self.seconds)/60,2)
            
            self.targetTemperature = 28

            if (self.seconds > self.setTime*60):
                self.lapsedTime = round((self.setTime2*60 - self.seconds)/60)
                self.tickmarckColor1 = ([60/255, 60/255, 60/255, 1])

                self.targetTemperature = self.setTemperature

            if (self.isTimePoint2On == False):
                self.tickmarckColor2 = ([51/255, 164/255, 208/255, 0])
                self.ids.onTimePoint2.disabled = True    
                self.setTimeAngle = 310
                self.ids.labelTime2.text = ''


            if (self.isTimePoint2On == True):
                

                self.tickmarckColor2 = ([51/255, 164/255, 208/255, 1])
                self.ids.onTimePoint2.disabled = False
                

            if (self.seconds > self.setTime2*60):
                self.tickmarckColor2 = ([60/255, 60/255, 60/255, 1])

                self.targetTemperature = self.setTemperature2
            
    
        # if ((self.seconds + 15)//30)%2 !=  0:
        #     self.labelOffsetY = 1
        # if   ((self.seconds+15)//30)%2 ==  0:
        #     self.labelOffsetY = -1

        # if ((self.seconds )//30)%2 !=  0:
        #     self.labelOffsetX = 1
           
        # if   ((self.seconds)//30)%2 ==  0:
        #     self.labelOffsetX = -1
  
       # print (MyPopup().ids.timePoint2Active.active)



    def startStop(self):

       # app.Starter.refreshStarter()
        app.root.ids.newStarter.refreshStarter()
        app.root.ids.editToggle.refreshEditer()
        if self.toggled == False:
            self.toggled = True
        else:
            self.toggled = False
        
      #  if self.running: 
     #       Starter.state = 'down'
     #   if self.running== False:
      #      Starter.state !='down'
        ####a ADD REFRESH EDIT BUTTON
   

 

class Starter (ToggleButton):



    def __init__ (self, **kwargs):

        ToggleButton.__init__(self,**kwargs)
        self.text = 'Select Bays'
        self.disabled = True
    def toggleValue(self):
        
        
        app.started = self.state=='down'     

        if( self.state =='down'):  
            self.text = 'Stop Protocol'
            self.started = True
            for i, toggle in enumerate(app.toggles):
                if toggle.state == 'down':
                    toggle.setTimeZero()
                   # print(i)

            
          
       
        if( self.state == 'normal'):
            self.started = False
            self.text = 'Start Protocol'
            self.started = True
            for toggle in app.toggles:
                if toggle.state == 'down':
                    toggle.running = False
                    toggle.ids.running.disabled =True
                    toggle.ids.running.text = ''








    def refreshStarter (self):

        if any(toggle.state=='down' for toggle in app.toggles ):

            self.disabled = False

            if any(toggle.running for toggle in app.toggles if toggle.state=='down'):
                self.state = 'down'
                self.text = 'Stop Protocol'
            else:
                self.state = 'normal'
                self.text = 'Start Protocol'
                
        else:
            self.disabled = True
            self.state = 'normal'
            self.text = 'Select Bays'
        
        # for toggle in app.toggles:
        #     if toggle.state =='down':
        #         if toggle.running:
        #             self.state = 'down'
        #             self.text = 'Stop Protocol'
        #             break
        #         else:
        #             self.state = 'normal'
        #             self.text = 'Start Protocol'
        # print (self.state)
        


class Edit (Button):

    def refreshEditer(self):
        if any(toggle.state=='down' for toggle in app.toggles ):
            self.disabled = False

        else:
            self.disabled = True

    def toggleValue(self):

        if( self.state =='down'):
           
            p = MyPopup()
     
            p.open()






class MyPopup (Popup):


    displayedTimeDelta1 =StringProperty()
    displayedTimeDelta2 =StringProperty()

    selectedTemperature1 = NumericProperty()
    selectedTemperature2 = NumericProperty()
    
    selectedMinutes1 = NumericProperty()
    selectedMinutes2 = NumericProperty()

    selectedHours1 = NumericProperty() 
    selectedHours2 = NumericProperty()

    tempsetTime = NumericProperty()
    
    

    def __init__ (self, **kwargs):
        Popup.__init__(self,**kwargs)
        
        for toggle in app.toggles:
            if toggle.toggled:

                
                self.tempSetTime2 = toggle.setTime2-toggle.setTime

                self.ids.temperature.value = toggle.setTemperature
                self.selectedHours1 = toggle.setTime//60
                self.selectedMinutes1 = toggle.setTime%60                             ## YEAH ##
                self.ids.temperature2.value = toggle.setTemperature2
                self.selectedHours2 = self.tempSetTime2//60 
                self.selectedMinutes2 = self.tempSetTime2%60 

                self.ids.timePoint2Active.active = toggle.isTimePoint2On


    def increaseTimeHours(self):
            self.selectedHours1 +=1
            self.updateClockTime (self.selectedHours1,self.selectedMinutes1,self.selectedHours2,self.selectedMinutes2)
            
      
    def decreaseTimeHours(self):
        if self.selectedHours1>0 :
            self.selectedHours1 -=1     
            self.updateClockTime(self.selectedHours1,self.selectedMinutes1,self.selectedHours2,self.selectedMinutes2)



    def increaseTimeHoursFive(self):
            self.selectedHours1 +=5
            self.updateClockTime (self.selectedHours1,self.selectedMinutes1,self.selectedHours2,self.selectedMinutes2)
            
      
    def decreaseTimeHoursFive(self):
        if self.selectedHours1>=5 :
            self.selectedHours1 -=5     
            self.updateClockTime(self.selectedHours1,self.selectedMinutes1,self.selectedHours2,self.selectedMinutes2)
      
      

    def increaseTimeMinute(self):
        if self.selectedMinutes1 < 55:
            self. selectedMinutes1 += 5
            self.updateClockTime (self.selectedHours1,self.selectedMinutes1,self.selectedHours2,self.selectedMinutes2)

    def decreaseTimeMinute(self):
        if self.selectedMinutes1>0 :
            self. selectedMinutes1 -= 5
            self.updateClockTime (self.selectedHours1,self.selectedMinutes1,self.selectedHours2,self.selectedMinutes2)
      

    def increaseTimeHours2(self):
            self.selectedHours2 +=1
            self.updateClockTime (self.selectedHours1,self.selectedMinutes1,self.selectedHours2,self.selectedMinutes2)

    def decreaseTimeHours2(self):
        if self.selectedHours2>0 : 
            self.selectedHours2 -=1
            self.updateClockTime (self.selectedHours1,self.selectedMinutes1,self.selectedHours2,self.selectedMinutes2)

    def increaseTimeHoursFive2(self):
            self.selectedHours2 +=5
            self.updateClockTime (self.selectedHours1,self.selectedMinutes1,self.selectedHours2,self.selectedMinutes2)

    def decreaseTimeHoursFive2(self):
        if self.selectedHours2>=5 : 
            self.selectedHours2 -=5
            self.updateClockTime (self.selectedHours1,self.selectedMinutes1,self.selectedHours2,self.selectedMinutes2)
      

    def increaseTimeMinute2(self):
        if self.selectedMinutes2 < 55:
            self. selectedMinutes2 += 5
            self.updateClockTime (self.selectedHours1,self.selectedMinutes1,self.selectedHours2,self.selectedMinutes2)
    def decreaseTimeMinute2(self):
        if self.selectedMinutes2>0 :
            self.selectedMinutes2 -= 5
            self.updateClockTime (self.selectedHours1,self.selectedMinutes1,self.selectedHours2,self.selectedMinutes2)



    def updateClockTime(self,hoursToAdd,minutesToAdd,hoursToAdd2,minutesToAdd2):

        self.hoursToAdd =0
        self.minutesToAdd = 0
        self.hoursToAdd2 =0
        self.minutesToAdd2 = 0

        self.tempTime = datetime.datetime.now() + datetime.timedelta(hours = hoursToAdd, minutes=minutesToAdd)
        self.displayedTimeDelta1 = self.tempTime.strftime( "%H:%M")
        self.tempTime2 = self.tempTime +  datetime.timedelta(hours = hoursToAdd2, minutes=minutesToAdd2)
        self.displayedTimeDelta2 = self.tempTime2.strftime( "%H:%M")




    def submitPopup(self):

        self.selectedTemperature1 = self.ids.temperature.value
       
        self.selectedTemperature2 = self.ids.temperature2.value#
    

        for toggle in app.toggles:
            if toggle.toggled:

                toggle.setTemperature = self.selectedTemperature1
                toggle.setTime = self.selectedMinutes1 + (self.selectedHours1*60)

                toggle.setTemperature2 = self.selectedTemperature2
                toggle.setTime2 = toggle.setTime + self.selectedMinutes2 + (self.selectedHours2*60)

                toggle.isTimePoint2On = self.ids.timePoint2Active.active
            
           # print(toggle.setTime2)

        for toggle, chamber in zip (app.toggles, app.board.chambers):
            
            #print(chamber)
            chamber.setpoint = toggle.targetTemperature
            print(toggle.targetTemperature)
            
            
        
        self.dismiss()

    def closePopup(self):
        self.dismiss()



class GeneralButton(Button):
    def onQuestionAsked(self):
        answer = MySecondPopup()
        answer.open()

class MySecondPopup (Popup):
    pass





###########################################################
####################### BUILD APP    ######################



class ScreenwidgetApp(App):



    currentTimeInMinutes = 0
    currentHour= 0
    currentMinutes=0


    def timer(self, dt):

        ######overallTimer

        if (int( datetime.datetime.now().strftime( "%H")))> 12:
            self.currentHour =   (int( datetime.datetime.now().strftime( "%H"))-12)*60
        else:
            self.currentHour =   (int( datetime.datetime.now().strftime( "%H")))*60

        self.currentMinutes = int( datetime.datetime.now().strftime( "%M"))
        self.currentTimeInMinutes = self.currentHour + self.currentMinutes
    
        # print (self.currentTimeInMinutes)

        self.board.refresh()


        self.time += 1 
        #self.currentDate =  time.strftime("%a, %d %b %Y %H:%M:%S")
        self.currentDate = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        app.root.ids.currentTimeLabel.text = self.currentDate
        
        

        

        for toggle in self.toggles:
            toggle.updateTime()

    #    print(self.board.chambers)
        

        for toggle, chamber in zip (app.toggles, app.board.chambers):

            chamber.setpoint = toggle.targetTemperature

            toggle.currentPower = chamber.power/255
          
            if toggle.currentPower  < .0 :
                toggle.newColor = ([51/255, 164/255, 208/255, 1])
            else:
                toggle.newColor = ([255/255, 159/255, 54/255,1])

            toggle.ids.currentTemp.text = str(round(chamber.temperature,1)) + '[sup]/' + str(toggle.targetTemperature) + '°C [/sup]'


    def build(self):



        

        ############## CONNECT TO BOARD ###################

        self.board = FishCozyHAL.Mainboard(port=port)
        self.board.connect()


        ##############

        self.started=False
        
        self.time=0
        Clock.schedule_interval(self.timer,.2) 
        app = RootWidget()

        ###############    INPUTS            ###############


        self.toggles = [
        app.ids.toggle0,
        app.ids.toggle1,
        app.ids.toggle2,
        app.ids.toggle3,
        app.ids.toggle4,
        app.ids.toggle5,
                    ]





        ####################################################





   
        return app


if __name__ == '__main__':
    app = ScreenwidgetApp()
   
    app.run()
    
#    print(app.root.ids)
