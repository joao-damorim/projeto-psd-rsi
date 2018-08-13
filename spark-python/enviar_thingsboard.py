# This Python file uses the following encoding: utf-8
#!/usr/bin/env python

import paho.mqtt.client as paho
import json

def sendThingsBoard(Listdic):
    mqtthost = "localhost"  
     
    mqtttopic = "v1/devices/me/telemetry"  
    
    client = paho.Client()
    acessToken = "I7egcEY61i7NcDbal2I3"#token aq
    mqttpass = ""
    client.username_pw_set(acessToken ,mqttpass)
    client.connect(mqtthost, 18830, 60)
    
    client.loop_start()
    
    for dic in Listdic:
        try:
            time = dic["timeStamp"] * 1000
            dicSend = {"ts": time, "values": dic}
            
        except:
            
            dicSend = dic
            
        bodyMessage = json.dumps(dicSend)
        x = client.publish(mqtttopic, bodyMessage, qos=1)
        print(x)
        print (" [x] Sent %r:%r" % ("enviando dados...", bodyMessage))
        