# This Python file uses the following encoding: utf-8
#!/usr/bin/env python
import paho.mqtt.client as paho
import time
import json
from __builtin__ import type

mqtthost = "localhost"  
mqttuser = "psd"  
mqttpass = "psd"  
mqtttopic = "hall"  

client = paho.Client()
client.username_pw_set(mqttuser,mqttpass)
client.connect(mqtthost, 1883,60)

client.loop_start()

teste = open('simulacaoProb.txt', 'r')
probStr = teste.read()
dicSendTest = json.loads(probStr)
timeStamps = sorted(dicSendTest.keys())

# x = 0
for timeStampKey in timeStamps:
    if int(timeStampKey) >= 1533393840 :
        probList = dicSendTest[timeStampKey]
        for probDic in probList:
    
            bodyMessage = json.dumps(probDic)
            (rc, mid) = client.publish(mqtttopic, bodyMessage, qos=1)
            print (" [x] Sent %r:%r" % (timeStampKey, bodyMessage))
    
        time.sleep(1)