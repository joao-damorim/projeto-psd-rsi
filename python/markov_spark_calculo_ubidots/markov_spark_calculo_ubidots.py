# ADVICE: With PyDev, take care about unused imports (and also unused variables),
# please comment them all, otherwise you will get any errors at the execution.
# Note that even the trick like the directives @PydevCodeAnalysisIgnore and
# @UnusedImport will never solve that issue.

# Imports the PySpark libraries
from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext

# The 'os' library allows us to read the environment variable SPARK_HOME defined in the IDE environment
import os
import numpy as np
import json
import pika
import time
import requests
import sys
import paho.mqtt.client as mqtt


class Markov():

    def qtd_de_pessoas(self, lista_pessoa):

        total = len(lista_pessoa)

        return total

    def localizacao_pessoa(self, lista_pessoa):

        localizacao = {}
        localizacao['local_1'] = []
        localizacao['local_2'] = []
        localizacao['local_3'] = []
        for pessoa in lista_pessoa:
            if pessoa['local'] == 'local_1':
                localizacao['local_1'].append(pessoa)
            elif pessoa['local'] == 'local_2':
                localizacao['local_2'].append(pessoa)
            elif pessoa['local'] == 'local_3':
                localizacao['local_3'].append(pessoa)

        return localizacao

    def qtd_de_pessoas_em_cada_local(self, dicionario_locais_pessoas):

        qtd_pessoas_local = {}
        local_1 = len(dicionario_locais_pessoas['local_1'])
        qtd_pessoas_local['local_1'] = local_1
        local_2 = len(dicionario_locais_pessoas['local_2'])
        qtd_pessoas_local['local_2'] = local_2
        local_3 = len(dicionario_locais_pessoas['local_3'])
        qtd_pessoas_local['local_3'] = local_3

        return qtd_pessoas_local

    def calcular_total_de_pessoas_por_lugar_porcentagem(self, total_de_pessoas, qtd_pessoas_local):

        a11 = (qtd_pessoas_local['local_1'] / float(total_de_pessoas)) * 100
        a12 = (qtd_pessoas_local['local_2'] / float(total_de_pessoas)) * 100
        a13 = (qtd_pessoas_local['local_3'] / float(total_de_pessoas)) * 100

        matriz = np.matrix([
            [a11, a12, a13],
        ])

        return matriz

TOKEN = "A1E-ErTiDmO2fCGKHwBgJoCV6wwv1djLUv"  # Put your TOKEN here
DEVICE_LABEL = "walk-tracking"  # Put your device label here
VARIABLE_LABEL_1 = "Local_1"  # Put your first variable label here
VARIABLE_LABEL_2 = "Local_2"  # Put your second variable label here
VARIABLE_LABEL_3 = "Local_3"  # Put your second variable label here


def build_payload(variable_1, variable_2, variable_3, value_1, value_2, value_3):
    # Creates two random values for sending data
    # Creates a random gps coordinates
    payload = {variable_1: value_1,
               variable_2: value_2,
               variable_3: value_3}

    return payload


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://things.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def main(controle):

    arqTempo = open('tempos.txt', 'r')
    tempos = arqTempo.read().split("\n")
    arqTempo.close()

    path = os.getcwd()
    listDir = os.listdir(path)

    for arquivo in listDir:
        try:
            if (arquivo == "imagem_" + str(tempos[controle]) + ".txt"):
                print("aqui")

                timeout = 1  # [seconds]

                timeout_start = time.time()

                while time.time() < timeout_start + timeout:
                    try:
                        print(str(tempos[controle]))
                        arq = open('imagem_' + str(tempos[controle]) + '.txt', 'r')
                        x = arq.read()
                        listaImagem = json.loads(x)

                        m = Markov()

                        total_de_pessoas_3_locais = m.qtd_de_pessoas(listaImagem)
                        # print(total_de_pessoas_3_locais)

                        localizacao_pessoas_3_locais = m.localizacao_pessoa(listaImagem)
                        # print(localizacao_pessoas_3_locais)

                        total_de_pessoas_em_cada_local = m.qtd_de_pessoas_em_cada_local(localizacao_pessoas_3_locais)
                        # print(total_de_pessoas_em_cada_local)

                        array_atual = m.calcular_total_de_pessoas_por_lugar_porcentagem(total_de_pessoas_3_locais,
                                                                                        total_de_pessoas_em_cada_local)
                        # print(array_atual)

                        with open('matriz_de_transicao_' + str(controle) + '.json', 'r') as f:
                            matriz_transicao_passada = json.load(f)

                        linha_1 = matriz_transicao_passada[0]
                        linha_2 = matriz_transicao_passada[1]
                        linha_3 = matriz_transicao_passada[2]

                        matriz_transicao_passada = np.matrix([
                            linha_1,
                            linha_2,
                            linha_3,
                        ])

                        array_futuro = np.dot(array_atual, matriz_transicao_passada)

                        local_1 = array_futuro.item(0)

                        local_2 = array_futuro.item(1)

                        local_3 = array_futuro.item(2)

                        print(local_1)
                        print(local_2)
                        print(local_3)

                        payload = build_payload(
                            VARIABLE_LABEL_1, VARIABLE_LABEL_2, VARIABLE_LABEL_3, local_1, local_2, local_3)

                        print("[INFO] Attemping to send data")
                        post_request(payload)
                        print("[INFO] finished")

                    except IOError:
                        print
                        "Fim da execucao da aplicacao!"
                        sys.exit()

        except IndexError:
            print
            "Fim da execucao da aplicacao!"
            sys.exit()

if __name__ == '__main__':
    while (True):
        controle = 0
        path = os.getcwd()
        listDir = os.listdir(path)
        start = "imagem_1533393900.txt"
        if (start in listDir):
            while (True):
                main(controle)
                controle += 1
                time.sleep(5)
        print("Procurando arquivo de imagem para estimativa!")
        time.sleep(10)
