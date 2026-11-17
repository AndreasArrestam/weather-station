import time
from Freenove_DHT import DHT 
from LCD1602 import CharLCD1602
import json
import requests


lon = 0
lat = 0

url = f"https://api.temperatur.nu/tnu_1.20.php?p=lnkpcity&sensor_type=all&cli=api_demo_v1.20"

DHTPin = 17 #define the pin as 17, matches with the extension board
lcd = CharLCD1602()

def get_outside_temp():
    try:
        response = requests.get(url)
        data = response.json()

        station = data['stations']

        temp = float(station[0]['temp'])

        return(temp)
            
    except:
        print("error getting data")
        return None

def loop():
    dht = DHT(DHTPin)
    lcd.init_lcd()
    time.sleep(1)
    counts = 0
    
    while(True):
        counts+=1
        print("measurement counts: ", counts)
        for i in range(0,15):
            chk = dht.readDHT11()
            if(chk == 0):
                break
            
            time.sleep(0.1)
        outside_temp = get_outside_temp()
        lcd.clear()
        lcd.write(0 ,0, 'Humidity: ' + str(dht.getHumidity()))
        lcd.write(0 ,1, 'Temp: ' + str(dht.getTemperature()) + ', ' + str(outside_temp))
        print("Humidity : %.2f, \t Temperature : %.2f "%(dht.getHumidity(), dht.getTemperature()))
        
        print("Outside temp: ", outside_temp, "\n")
        time.sleep(2)
        
if __name__ == '__main__':
    print("Program starting") 
    try:
        loop()
    except KeyboardInterrupt:
        exit()
            
