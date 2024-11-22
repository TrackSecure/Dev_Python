import subprocess
import re
import mysql.connector

macAddress = "00:00:00:00:00:00"

db_connection = mysql.connector.connect(host='localhost', user='aluno', password='sptech', database='TrackSecure')
cursor = db_connection.cursor()

# Executar o comando 'top' e capturar a saída
result = subprocess.run(['top', '-b', '-n', '1'], capture_output=True, text=True).stdout

print(result)

# Remover as primeiras linhas que contêm informações de cabeçalho e outras não relevantes
lines = result.splitlines()[7:]  

# Para cada linha de processo capturada
for line in lines:
    columns = re.split(r'\s+', line)  

    if len(columns) > 12:
        process_name = columns[12]
        memory_usage = columns[10]  
        
        memory_usage = memory_usage.replace(',', '.')
            
        sql = f"INSERT INTO Processo (nome, usoMemoria, fkServidor) VALUES ('{process_name}', {memory_usage}, '{macAddress}')"
        cursor.execute(sql)
        db_connection.commit()
