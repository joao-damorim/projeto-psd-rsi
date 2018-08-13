# Walk Tracking

## Sobre o projeto.

> O projeto é um sistema integrado desenvolvido para as disciplinas Projeto de Sistemas Distribuídos (Prof.: Victor Medeiros) e Redes e Sistemas de Internet (Prof.: Glauco Gonçalves), que faz um estudo do deslocamento de pessoas em shopping center. Através de uma análise probrabilistica utilizando como principais ferramentas as cadeias de Markov, placa NodeMCU composta por um módulo ESP8266, Python, Spark 2.2. O sistema entrega ao usuário final uma estimativa da concentração de pessoas em um determinado futuro, dado um acontecimento do passado com os mesmos parâmetros.

## Pré-requesitos

> Arduino 1.8.5 (IDE)

> Placa NodeMCU composta por um módulo ESP8266 (3 unidades)

> Python 2.7

> Spark Apache 2.2

## Tutorial para execução do sistema.

> Conectar a placa NodeMCU no computador.

> Executar no Arduino 1.8.5 (IDE) o arquivo [probe_request.ino].

> Executar a aplicação [read_serial.py] para geração do arquivo .txt com os probes request capturados.

> Executar a aplicação [formatacao_para_markov_10 min.py], o .txt gerado pela [read_serial.py] será consumido e serão gerados dois .txt com a imagem e com o real.

> Executar a aplicação [markov_gerador_matriz.py], os .txt gerados pela [formatacao_para_markov_10 min.py] serão consumidos e será gerado um .json com a matriz de transição referente.

> Executar a aplicação [read_serial.py], para geração do arquivo .txt com os probes request capturados.

> Executar a aplicação [simulacao_envio_probes.py], o .txt gerado pela [read_serial.py] será consumido e os probes serão enviados para RabbitMQ para a simulação dos envios.

> Executar a aplicação [capturar_probe_request.py], para geração do arquivo .txt com os probes request vindos do RabbitMQ de acordo com o tempo escolhido.

> Executar a aplicação [markov_spark_calculo_ubidots.py], vai ficar em modo sentinela aguardando o .txt gerado pela [capturar_probe_request.py], onde será realizado o cálculo e os resultados serão enviados para o ThingsBoard e Ubidots.
