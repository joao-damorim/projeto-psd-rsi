import numpy as np
import json

class Markov:

    def calcular_total_de_pessoas_por_lugar_porcentagem(total_de_pessoas, qtd_pessoas_local):
        a11 = qtd_pessoas_local['local_1'] / total_de_pessoas
        a12 = qtd_pessoas_local['local_1'] / total_de_pessoas
        a13 = qtd_pessoas_local['local_1'] / total_de_pessoas

        matriz = np.matrix([
            [a11, a12, a13],
        ])

        return matriz

    def qtd_de_pessoas(lista_pessoa):

        total = len(lista_pessoa)

        return total

    def localizacao_pessoa(lista_pessoa):

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

    def qtd_de_pessoas_em_cada_local(dicionario_locais_pessoas):

        qtd_pessoas_local = {}
        local_1 = len(dicionario_locais_pessoas['local_1'])
        qtd_pessoas_local['local_1'] = local_1
        local_2 = len(dicionario_locais_pessoas['local_2'])
        qtd_pessoas_local['local_2'] = local_2
        local_3 = len(dicionario_locais_pessoas['local_3'])
        qtd_pessoas_local['local_3'] = local_3

        return qtd_pessoas_local

    def calcular_matriz_de_transicao(qtd_pessoas_local, localizacao_pessoa_inicial_1_min, localizacao_pessoa_60_min):

        total_de_pessoas_local_1 = qtd_pessoas_local['local_1']
        total_de_pessoas_local_2 = qtd_pessoas_local['local_2']
        total_de_pessoas_local_3 = qtd_pessoas_local['local_3']

        total_a11 = total_de_pessoas_local_1
        total_a12 = 0
        total_a13 = 0
        total_a21 = 0
        total_a22 = total_de_pessoas_local_2
        total_a23 = 0
        total_a31 = 0
        total_a32 = 0
        total_a33 = total_de_pessoas_local_3

        for local, lista_pessoa in localizacao_pessoa_inicial_1_min.items():
            if local == 'local_1':
                for pessoa in lista_pessoa:
                    mac = pessoa['Peer MAC']
                    for local_60, lista_pessoa_60 in localizacao_pessoa_60_min.items():
                        if local_60 == 'local_2':
                            for pessoa_60 in lista_pessoa_60:
                                mac_60 = pessoa_60['Peer MAC']
                                if mac == mac_60:
                                    total_a11 -= 1
                                    total_a12 += 1
                    for local_60_2, lista_pessoa_60_2 in localizacao_pessoa_60_min.items():
                        if local_60_2 == 'local_3':
                            for pessoa_60_2 in lista_pessoa_60_2:
                                mac_60_2 = pessoa_60_2['Peer MAC']
                                if mac == mac_60_2:
                                    total_a11 -= 1
                                    total_a13 += 1

            elif local == 'local_2':
                for pessoa in lista_pessoa:
                    mac = pessoa['Peer MAC']
                    for local_60, lista_pessoa_60 in localizacao_pessoa_60_min.items():
                        if local_60 == 'local_1':
                            for pessoa_60 in lista_pessoa_60:
                                mac_60 = pessoa_60['Peer MAC']
                                if mac == mac_60:
                                    total_a22 -= 1
                                    total_a21 += 1

                    for local_60_2, lista_pessoa_60_2 in localizacao_pessoa_60_min.items():
                        if local_60_2 == 'local_3':
                            for pessoa_60_2 in lista_pessoa_60_2:
                                mac_60_2 = pessoa_60_2['Peer MAC']
                                if mac == mac_60_2:
                                     total_a22 -= 1
                                     total_a23 += 1

            elif local == 'local_3':
                for pessoa in lista_pessoa:
                    mac = pessoa['Peer MAC']
                    for local_60, lista_pessoa_60 in localizacao_pessoa_60_min.items():
                        if local_60 == 'local_1':
                            for pessoa_60 in lista_pessoa_60:
                                mac_60 = pessoa_60['Peer MAC']
                                if mac == mac_60:
                                    total_a33 -= 1
                                    total_a31 += 1
                    for local_60_2, lista_pessoa_60_2 in localizacao_pessoa_60_min.items():
                        if local_60_2 == 'local_2':
                            for pessoa_60_2 in lista_pessoa_60_2:
                                mac_60_2 = pessoa_60_2['Peer MAC']
                                if mac == mac_60_2:
                                     total_a33 -= 1
                                     total_a32 += 1

        a11 = total_a11/total_de_pessoas_local_1

        a12 = total_a12/total_de_pessoas_local_1

        a13 = total_a13/total_de_pessoas_local_1

        a21 = total_a21/total_de_pessoas_local_2

        a22 = total_a22/total_de_pessoas_local_2

        a23 = total_a23/total_de_pessoas_local_2

        a31 = total_a31/total_de_pessoas_local_3

        a32 = total_a32/total_de_pessoas_local_3

        a33 = total_a33/total_de_pessoas_local_3

        matriz = [[a11, a12, a13],[a21, a22, a23],[a31, a32, a33]]

        return matriz

for i in (0,1,2,3):
    num =  str(i)
    arq= open('Imagem_'+num+'.txt','r')
    x = arq.read()
    listaImagem = json.loads(x)
    arq = open('Real_'+num+'.txt','r')
    x = arq.read()
    listaReal = json.loads(x)

    localizacao_imagem = Markov.localizacao_pessoa(listaImagem)
    localizacao_real = Markov.localizacao_pessoa(listaReal)

    qtd_pessoas_em_cada_local_imagem = Markov.qtd_de_pessoas_em_cada_local(localizacao_imagem)
    print(qtd_pessoas_em_cada_local_imagem)

    matriz_transicao = Markov.calcular_matriz_de_transicao(qtd_pessoas_em_cada_local_imagem, localizacao_imagem, localizacao_real)


    with open('matriz_de_transicao_'+num+'.json', 'w') as f:
        json.dump(matriz_transicao, f)

