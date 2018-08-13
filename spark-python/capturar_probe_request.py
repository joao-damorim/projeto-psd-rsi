from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from mqtt import MQTTUtils
import json
from symbol import except_clause
from teste import sendThingsBoard

if __name__ == "__main__":

    sc = SparkContext()
    ssc = StreamingContext(sc, 60)

    brokerUrl = "tcp://localhost:1883"
    topic1 = "hall"
    key = "geral"
    
    lines_hall = MQTTUtils.createStream(ssc, brokerUrl, topic1)
    smallTime = 0
    arqv = open("tempos.txt","r")
    times = arqv.read().split("\n")
    countTime = 0
    
    def printGlobals():
        print(smallTime)
        
    def collectRddSmall(x):
        r = x.collect()[0]
        global smallTime 
        smallTime = r
        printGlobals()
        
    def rddToTxt(rdd):
        r = rdd.collect()[0]
        sendThingsBoard(r)
        global countTime
        if ( smallTime >= int(times[countTime])) :  
            arq = open("imagem_"+str(times[countTime])+".txt","w")
            arq.write(json.dumps(r))
            arq.close()
            countTime+=1
            
    # Split each line into macs
    macs = lines_hall.flatMap(lambda line: [json.loads(line)] )
    #Finding False Macs
    trueMacs = macs.filter(lambda json: json['Peer MAC'][2] not in ['2','3','6','7','A','B','E','F'])
    #bigestTime = macs.map(lambda prob : prob["timeStamp"]).reduce(lambda x, y: x if x > y else y)
    smallestTime = trueMacs.map(lambda prob : prob["timeStamp"]).reduce(lambda x, y: x if x < y else y)
    #bigestTime.foreachRDD(collectRddBig)
    smallestTime.foreachRDD(collectRddSmall)

    # Create pair with theirs own mac values
    pairs = trueMacs.map(lambda prob: ( prob["Peer MAC"] , prob))
    #pairs.pprint(100)
    #Eliminate repeated probs               
    macsCounts = pairs.reduceByKey(lambda x, y : x if ( int(x["RSSI"]) > int(y["RSSI"]) ) else (x if ( int(x["timeStamp"]) < int(y["timeStamp"])) else y))
    
    #generate a list of probs for that context
    window = macsCounts.map(lambda pair : (key, [pair[1]])).reduceByKey(lambda x, y: x + y).map(lambda geral: geral[1])
    #save prob list in a txt file
    #window.pprint(100)
    window.foreachRDD(rddToTxt)
   
    ssc.start()
ssc.awaitTermination()