import time
from Freenove_DHT import DHT
from LCD1602 import CharLCD1602
import requests

lon = 0
lat = 0

url = f"https://opendata-download-metfcst.smhi.se/api/category/pmpg3/version/2/geotype/point/lon/{lon}/lat/{lat}/data.json"

DHTPin = 17 #define the pin as 17, matches with the extension board
lcd = CharLCD1602()

def get_outside_temp():
    try:
        response = requests.get(url)
        data = response.json()

        current_temp = data['timeseries'][0]

        for param in current_temp['parameters']:
            if param['name'] == 't':
                return param['values'][0]
            
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
                print("DHT11 OK!")
                break
            
            time.sleep(0.1)
        lcd.clear()
        lcd.write(0 ,0, 'Humidity: ' + str(dht.getHumidity()))
        lcd.write(0 ,1, 'Temp: ' + str(dht.getTemperature()))
        print("Humidity : %.2f, \t Temperature : %.2f \n"%(dht.getHumidity(), dht.getTemperature()))
        outside_temp = get_outside_temp()
        print("\nOutside temp: ", outside_temp)
        time.sleep(2)
        
if __name__ == '__main__':
    print("Program starting")
    print("hej hej")
    
    try:
        loop()
    except KeyboardInterrupt:
        exit()
            
