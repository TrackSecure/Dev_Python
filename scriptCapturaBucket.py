import psutil
import time
import platform
from socket import gethostname
import csv
import boto3

nomeMaquina = gethostname()

campos = ["Máquina", "SO", "PorcentCPU", "FreqCPU", "UsoRAM", "PorcentRAM", "UsoDisco", "PorcentDisco"]
linhas = []

while (True):
        qtdCapturas = int(input(("Quantas capturas deseja fazer? \n ")))
        intervaloTempo = int(input(("Qual o intervalo de tempo em segundos: ")))

        for i in range(qtdCapturas):

            cpu_porcent = psutil.cpu_percent(interval=1)
            cpu_speed = psutil.cpu_freq().current / pow(10,3)
            
            so = platform.system()

            if (so == 'Windows'):
                # DIRETÓRIO PARA WINDOWS    
                disc_used = psutil.disk_usage('C:\\').used / pow(10,9)
                disc_percent = psutil.disk_usage('C:\\').percent
            elif (so == 'Linux'):
                # DIRETÓRIO PARA LINUX
                disc_used = psutil.disk_usage('/bin').used / pow(10,9)
                disc_percent = psutil.disk_usage('/bin').percent    

            ram_used = (psutil.virtual_memory().used) / pow(10,9)
            ram_percent = psutil.virtual_memory().percent

            # Cria uma mensagem, com valores arredondados e printa essa mensagem

            mensagem = f"""
                      {i + 1}º captura   
                      Máquina: {nomeMaquina}
                      SO: {so}
                      Uso da CPU: {cpu_porcent:.2f}%
                      Frequência de Uso da CPU: {cpu_speed:.2f}Mhz
                      Uso em GB RAM: {ram_used:.2f} GB
                      Uso da memória RAM: {ram_percent:.2f} %
                      Uso do disco: {disc_used:.2f} GB
                      Porcentagem Disco usada: {disc_percent:.2f} %
                      """
            
            print(mensagem)
            
            linha = [nomeMaquina, so, cpu_porcent, cpu_speed, ram_used, ram_percent, disc_used, disc_percent]
            linhas.append(linha)

            # Coloca um intervalo de tempo a captura 

            time.sleep(intervaloTempo)

        resposta = input("Deseja continuar? s/n: ")

        if(resposta == "s"):
            continue
        else:
            break


filename = "dados_capturados.csv"

with open(filename, "w") as arquivocsv:
    csvwriter = csv.writer(arquivocsv)
    csvwriter.writerow(campos)
    csvwriter.writerows(linhas)

s3 = boto3.client('s3')
with open("dados_capturados.csv", "rb") as file:
    s3.upload_fileobj(file, "s3-raw-lab-tracksecure", "dados_capturados.csv")