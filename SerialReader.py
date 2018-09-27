import serial
import datetime,time
import csv
import sys


#print (sys.argv)

if len(sys.argv) ==1:
    print ('error: define port (eg. COM4) ask Eirin how to check')
    sys.exit()
else:
    print('yey!!')
    port=sys.argv[1]

arduino = serial.Serial(port,timeout=1,baudrate=9600)



timeZero= int(time.time())
refreshRateSeconds = 5
date = str(datetime.datetime.fromtimestamp(timeZero).strftime('%Y%m%d_%H%M'))
print(date)
#fieldnames = ['time','temperature']
    #writer = csv.DictWriter(csv_file, fieldnames=fieldnames,delimiter='\t')
    #writer.writeheader()
    
while True:
    timeOne = int(time.time())
    arduinoRead = arduino.readline().decode().strip()
        
    if(timeOne - timeZero == refreshRateSeconds):
        with open (date+'.csv','a') as csv_file:
            outline = str(timeZero)+ '\t' + str(arduinoRead)
            print(outline)
            csv_file.write(outline+'\n')
                #writer.writerow({'time':str(timeZero),'temperature':str(arduinoRead)})

        timeZero= int(time.time())
        ### ADD CLOCK ###
        ### SET RETRIEVE DATA EVERY T ###
        ### PRINT SERIAL DATA AND T-STAMP ###
        ### SAVE EVERYTHING (AND PLOT?) ###

            
