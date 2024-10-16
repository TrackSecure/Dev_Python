import psutil
import time
import platform
from socket import gethostname
import json
import boto3

nomeMaquina = gethostname()

json_py = []

while (True):
        qtdCapturas = int(input(("Quantas capturas deseja fazer? \n ")))
        intervaloTempo = int(input(("Qual o intervalo de tempo em segundos: ")))

        for i in range(qtdCapturas):

            cpu_porcent = psutil.cpu_percent(interval=1)
            cpu_speed = psutil.cpu_freq().current #/ pow(10,3)
            
            so = platform.system()

            if (so == 'Windows'):
                # DIRETÓRIO PARA WINDOWS    
                disc_used = psutil.disk_usage('C:\\').used #/ pow(10,9)
                disc_percent = psutil.disk_usage('C:\\').percent
            elif (so == 'Linux'):
                # DIRETÓRIO PARA LINUX
                disc_used = psutil.disk_usage('/bin').used #/ pow(10,9)
                disc_percent = psutil.disk_usage('/bin').percent    

            ram_used = (psutil.virtual_memory().used) #/ pow(10,9)
            ram_percent = psutil.virtual_memory().percent

            # Cria uma mensagem, com valores arredondados e printa essa mensagem

            mensagem = f"""
                      {i + 1}º captura   
                      Máquina: {nomeMaquina}
                      SO: {so}
                      Uso da CPU: {cpu_porcent}%
                      Frequência de Uso da CPU: {cpu_speed} MHz
                      Uso em GB RAM: {ram_used} Bytes
                      Uso da memória RAM: {ram_percent} %
                      Uso do disco: {disc_used} Bytes
                      Porcentagem Disco usada: {disc_percent} %
                      """
                      # É necessário arredondar para duas casas na ETL Java
            
            print(mensagem)
            
            linha = {"Maquina":nomeMaquina, "SO":so, "PorcentCPU":cpu_porcent, "FreqCPU":cpu_speed, 
            "UsoRAM":ram_used, "PorcentRAM":ram_percent, "UsoDisco":disc_used, "PorcentDisco":disc_percent}
            json_py.append(linha)

            # Coloca um intervalo de tempo a captura 

            time.sleep(intervaloTempo)

        resposta = input("Deseja continuar? s/n: ")

        if(resposta == "s"):
            continue
        else:
            break


filename = "dados_capturados.json"

with open(filename, "w") as arquivojson:
    json.dump(json_py, arquivojson)

s3 = boto3.client('s3')
with open("dados_capturados.json", "rb") as file:
    s3.upload_fileobj(file, "s3-raw-lab-tracksecure", "dados_capturados.json")