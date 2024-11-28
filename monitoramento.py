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
import re
from getmac import get_mac_address as gma
import mysql.connector

nomeMaquina = gethostname()
# macAddress = gma()
macAddress = '00:00:00:00:00:00'
# É necessário descomentar a linha acima na implementação definitiva

db_connection = mysql.connector.connect(host='localhost', user='aluno', password='tracksecure', database='TrackSecure')
cursor = db_connection.cursor()

json_py = []

# jira =Jira(
#     url = "https://sptech-team-it55r942.atlassian.net",
#     username = "felipe.patroni@sptech.school",
#     password = "" #TOKEN
# )

while (True):
        # qtdCapturas = int(input(("Quantas capturas deseja fazer? \n ")))
        qtdCapturas = 3
        # intervaloTempo = int(input(("Qual o intervalo de tempo em segundos: ")))
        intervaloTempo = 1

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
            pacotes = psutil.net_io_counters().packets_recv

            sql = "INSERT INTO Registro (porcentagemProcessador, porcentagemMemoria, porcentagemDisco, freqProcessador, memoriaUsada, discoUsado, pacotesRecebidos, fkServidor) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            values = (cpu_porcent, ram_percent, disc_percent, cpu_speed, ram_used, disc_used, pacotes, macAddress) # Linha com MacAddress para teste
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
                      Pacotes recebidos: {pacotes}
                      """
                      # É necessário arredondar para duas casas na ETL Java
            
            print(mensagem)
            
            linha = {"Maquina":nomeMaquina, "SO":so, "PorcentCPU":cpu_porcent, "FreqCPU":cpu_speed, 
            "UsoRAM":ram_used, "PorcentRAM":ram_percent, "UsoDisco":disc_used, "PorcentDisco":disc_percent}
            json_py.append(linha)

            # Coloca um intervalo de tempo a captura 

            time.sleep(intervaloTempo)

        # resposta = input("Deseja continuar? s/n: ")
        resposta = "n"

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

# Executar o comando 'top' e capturar a saída
result = subprocess.run(['top', '-b', '-n', '1'], capture_output=True, text=True).stdout

print(result)

# Remover as primeiras linhas que contêm informações de cabeçalho e outras não relevantes
lines = result.splitlines()[7:]  

processos = {}

# Para cada linha de processo capturada
for line in lines:
    columns = re.split(r'\s+', line)  

    if len(columns) > 12:
        process_name = columns[12]
        memory_usage = columns[10]  
        
        memory_usage = memory_usage.replace(',', '.')
            
        memory_usage_value = round(float(memory_usage), 2)

        if process_name in processos:
          processos[process_name] += memory_usage_value
        else:
          processos[process_name] = memory_usage_value
        
for process_name, memory_usage_value in processos.items():
  if memory_usage_value > 0.0:
    sql = f"INSERT INTO Processo (nome, usoMemoria, fkServidor) VALUES ('{process_name}', {memory_usage_value}, '{macAddress}')"
    
    print(process_name, memory_usage_value)
    cursor.execute(sql)
    db_connection.commit()

data = str(datetime.datetime.now()).replace(" ", "_") 
data = data.replace(":", "_")
filename = f"dados_capturados_{data}_{nomeMaquina}.json"

with open(filename, "w") as arquivojson:
    json.dump(json_py, arquivojson)

s3 = boto3.client('s3')
with open(filename, "rb") as file:
    s3.upload_fileobj(file, "s3-raw-lab-tracksecure", filename)