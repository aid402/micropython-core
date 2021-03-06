from simple import MQTTClient
from machine import Pin,reset
from time import sleep
import network,json,pzem,gc

# Modify below section as required
CONFIG = {
     # Configuration details of the MQTT broker
     "MQTT_BROKER": "192.168.2.103",
     "USER": "username",
     "PASSWORD": "password",
     "PORT": 1883,
     "CLIENT_ID": b"pzem004t"
}
Topic1=b"emon/pub"
Topic2=b"emon/sub"
state="on"
t=10
sleep(t)
print('Emod.')
emon=pzem.PZEM004T()
print('PZEM connected',emon.isReady())
client=None
ip=None

def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect('AP_NAME', 'password')
        while not sta_if.isconnected():
            pass
    else:
        global client
        client = MQTTClient(CONFIG['CLIENT_ID'], CONFIG['MQTT_BROKER'], user=CONFIG['USER'], password=CONFIG['PASSWORD'], port=CONFIG['PORT'])
        client.connect()
        sleep(1)
        print('MQTT connected.')
    global ip
    ip=sta_if.ifconfig()[0]


def main():
    while True:
        gc.collect()
        try:
            if state == "on":
                sensor = emon.readAll()
                print(ip)
                print(sensor)
                msg = json.dumps({'ip':ip,'pzem':sensor,'heap':gc.mem_free()})
                client.publish(Topic1,msg)
                sleep(3)
            else:
                sleep(t)
        except Exception as e:
            print(e)
            connect_wifi()
            continue

connect_wifi()
main()
