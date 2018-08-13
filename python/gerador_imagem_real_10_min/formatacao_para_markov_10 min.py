import json
nameArq = 'probListLog_Local_'
versão = 0

# 1533392782 menor de todos os tempos de coleta 08/04/2018 @ 2:26pm (UTC)
timeStampStart = 1533393900 # 08/04/2018 @ 2:45pm (UTC)
timeStampFinish = 1533396600 # 08/04/2018 @ 3:30pm (UTC)

pImagem = 60 # passo de 1 minuto
pReal = 600 # passo de 10 minuto
probDic = {}
probList = []
timeStampList=[]


for i in (1,2,3):
    nome = nameArq+ str(i) + '_Formatada'
    print(nome)
    arq = open( nome+ '.txt','r')
    listProb = arq.read().split('\n')
    for prob in listProb :
        try:
            dic = json.loads(prob)
        except:
            print(prob)

        probList.append(dic)
        time = int(dic['timeStamp'])

        try:
            probDic[time].append(dic)
        except:
            probDic[time] = []
            probDic[time].append(dic)
            
        if time not in timeStampList:
            timeStampList.append(time)
           
timeSort = sorted(timeStampList)
start = timeStampStart
bound = start + pImagem
finish = bound + pReal
cont = 0

while True:
    imageList =  []
    resultImage = {}
    realList = []
    resultReal ={}
    print(start, bound)
    
    for time in range(start, bound + 1):
        try:
            secondListed =  probDic[time]
        except:
            print(time)
        for prob in secondListed:
            mac = prob['Peer MAC']
            resultImage[mac] = prob
    for key in resultImage.keys():
        imageList.append(resultImage[key])
    
    for time in range(bound, finish + 1):
        try:
            secondListed =  probDic[time]
        except:
            print(time)
        for prob in secondListed:
            mac = prob['Peer MAC']
            resultReal[mac] = prob
            
    for key in resultReal.keys():
        realList.append(resultReal[key])
        
    img = open('Imagem_'+str(cont)+'.txt','w')
    real = open('Real_'+str(cont)+'.txt','w')
    img.write(json.dumps(imageList))
    real.write(json.dumps(realList))
    img.close()
    real.close()
    cont+=1
    
    start = finish
    bound = start + pImagem
    finish = bound + pReal

    if finish > timeStampFinish:
        print(finish,'f')
        break
