import serial
import time
from decimal import *

def find(str, ch):
    for i, ltr in enumerate(str):
        if ltr == ch:
            yield i

ser = serial.Serial("/dev/ttyS0",115200)

W_buff = ["AT+CGNSPWR=1\r\n", "AT+CGNSSEQ=\"RMC\"\r\n", "AT+CGNSINF\r\n", "AT+CGNSURC=2\r\n","AT+CGNSTST=1\r\n"]
ser.write(W_buff[0])
ser.flushInput()
data = ""
num = 0


while True:
    while ser.inWaiting() > 0:
        data += ser.read(ser.inWaiting())
    if data != "":
#        print data
        if  num < 4:    # the string have ok
            print num
            time.sleep(0.5)
            ser.write(W_buff[num+1])
            num =num +1
        if num == 4:
            time.sleep(0.5)
            ser.write(W_buff[4])
            num=0
        data = ""
        fd=ser.read(200)
        ps=fd.find('$GNGGA')

        if ps > 0:
            data=fd[ps:(ps+50)]
            
            p=list(find(data, ","))
            lat=data[(p[1]+1):p[2]]
            lon=data[(p[3]+1):p[4]]

            lat_deg=int(lat[0:2])
            lat_mins=float(lat[2:len(lat)])/60
            lat_dec=lat_deg+lat_mins
            print lat_dec
            
            lon_deg=int(lon[0:3])
            lon_mins=float(lon[3:len(lon)])/60
            lon_dec=lon_deg+lon_mins
            print lon_dec     