import psutil
import time
import platform
from socket import gethostname
import json
import boto3
import datetime
from atlassian import Jira
from requests import HTTPError
import subprocess
import csv
import re
from getmac import get_mac_address as gma
import mysql.connector

nomeMaquina = gethostname()
macAddress = gma()

db_connection = mysql.connector.connect(host='localhost', user='aluno', password='sptech', database='TrackSecure')
cursor = db_connection.cursor()

json_py = []

jira =Jira(
    url = "https://sptech-team-it55r942.atlassian.net",
    username = "felipe.patroni@sptech.school",
    password = "" #TOKEN
)

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

            sql = "INSERT INTO Registro (porcentagemProcessador, porcentagemMemoria, porcentagemDisco, freqProcessador, memoriaUsada, discoUsado, fkServidor) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (cpu_porcent, ram_percent, disc_percent, cpu_speed, ram_used, disc_used, macAddress)
            cursor.execute(sql, values)
            db_connection.commit()

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

        problema_disco = False
        problema_ram = False
        problema_cpu = False

        if(disc_percent > 90):
            summary_disco = 'DISCO EMERGENCIA'
            description_disco = 'Disco está com uso extremamente elevado!'
            priority_disco = 'High'
            problema_disco = True
        elif(disc_percent >= 80):
            summary_disco = 'DISCO CRITICO'
            description_disco = 'Disco está com muito uso!'
            priority_disco = 'Medium'
            problema_disco = True
        elif(disc_percent >= 50):
            summary_disco = 'ATENÇÃO DISCO'
            description_disco = 'Disco está com uso elevado!'
            priority_disco = 'Low'
            problema_disco = True

        if(ram_percent > 90):
            summary_ram = 'RAM EMERGENCIA'
            description_ram = 'RAM está com uso extremamente elevado!'
            priority_ram = 'High'
            problema_ram = True
        elif(ram_percent >= 80):
            summary_ram = 'RAM CRITICA'
            description_ram = 'RAM está com muito uso!'
            priority_ram = 'Medium'
            problema_ram = True
        elif(ram_percent >= 30):
            summary_ram = 'ATENÇÃO RAM'
            description_ram = 'RAM está com uso elevado!'
            priority_ram = 'Low'
            problema_ram = True
        
        if(cpu_porcent > 90):
            summary_cpu = 'CPU EMERGENCIA'
            description_cpu = 'CPU está com uso extremamente elevado!'
            priority_cpu = 'High'
            problema_cpu = True
        elif(cpu_porcent >= 80):
            summary_cpu = 'CPU CRITICA'
            description_cpu = 'CPU está com muito uso!'
            priority_cpu = 'Medium'
            problema_cpu = True
        elif (cpu_porcent >= 50):
            summary_cpu = 'ATENÇÃO CPU'
            description_cpu = 'CPU está com uso elevado!'
            priority_cpu = 'Low'
            problema_cpu = True
        
        try:
            if (problema_disco):
                jira.issue_create(
                    fields={
                        'project': {
                            'key': 'TRAC' #SIGLA
                        },
                        'summary': summary_disco, #titulo do chamado
                        'description': description_disco, #descrição
                        'issuetype': {
                            "name": "Task" #Tipo de chamado 
                        },
                        'priority': {
                            'name': priority_disco
                        }
                    }
                )
                sql = "INSERT INTO Alerta (tipo, descricao, fkServidor) VALUES (%s, %s, %s)"
                values = (priority_disco, description_disco, macAddress)
                cursor.execute(sql, values)
                db_connection.commit()
            if (problema_ram):
                jira.issue_create(
                    fields={
                        'project': {
                            'key': 'TRAC' #SIGLA
                        },
                        'summary': summary_ram, #titulo do chamado
                        'description': description_ram, #descrição
                        'issuetype': {
                            "name": "Task" #Tipo de chamado 
                        },
                        'priority': {
                            'name': priority_ram
                        }
                    }
                )
                sql = "INSERT INTO Alerta (tipo, descricao, fkServidor) VALUES (%s, %s, %s)"
                values = (priority_ram, description_ram, macAddress)
                cursor.execute(sql, values)
                db_connection.commit()   
            if (problema_cpu):
                jira.issue_create(
                    fields={
                        'project': {
                            'key': 'TRAC' #SIGLA
                        },
                        'summary': summary_cpu, #titulo do chamado
                        'description': description_cpu, #descrição
                        'issuetype': {
                            "name": "Task" #Tipo de chamado 
                        },
                        'priority': {
                            'name': priority_cpu
                        }
                    }
                )
                sql = "INSERT INTO Alerta (tipo, descricao, fkServidor) VALUES (%s, %s, %s)"
                values = (priority_cpu, description_cpu, macAddress)
                cursor.execute(sql, values)
                db_connection.commit()    
        except HTTPError as e :
            print(e.response.text)

        if(resposta == "s"):
            continue
        else:
            break

data = str(datetime.datetime.now()).replace(" ", "_") 
data = data.replace(":", "_")
filename = f"dados_capturados_{data}_{nomeMaquina}.json"

with open(filename, "w") as arquivojson:
    json.dump(json_py, arquivojson)

s3 = boto3.client('s3')
with open(filename, "rb") as file:
    s3.upload_fileobj(file, "s3-raw-lab-tracksecure", filename)

# Executar o comando 'tasklist' e capturar a saída - este comando é o mesmo do CMD - sistema operacional
result = subprocess.run(['tasklist'], capture_output=True, text=True).stdout

print(result)

result = re.sub(r" K(?=\n)", "", result) # Expressão Regular para remover os "K" no uso de memória
result = re.sub(r" (?![0-9 ]|(Services)|(Console))", "_", result) # Expressão Regular para substituir espaços de palavras por '_'

lines = result.splitlines()[3:]

with open('tasks3.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Nome_da_Imagem', 'PID', 'Nome_da_Sessao', 'Sessao#', 'Uso_de_memoria (K)'])
   
    for line in lines:
        columns = line.split()
        csv_writer.writerow(columns)

with open("tasks3.csv", "rb") as file:
    s3.upload_fileobj(file, "s3-raw-lab-tracksecure", "tasks3.csv")