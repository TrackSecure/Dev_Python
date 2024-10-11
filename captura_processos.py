import subprocess
import csv
import re


# Executar o comando 'tasklist' e capturar a saída - este comando é o mesmo do CMD - sistema operacional
result = subprocess.run(['tasklist'], capture_output=True, text=True).stdout

print(result)

result = re.sub(r" (?![0-9 ]|(Services)|(Console))", "_", result)
lines = result.splitlines()[3:]

with open('tasks3.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Nome_da_Imagem', 'PID', 'Nome_da_Sessao', 'Sessao#', 'Uso_de_memoria'])
   
    for line in lines:
        columns = line.split()
        csv_writer.writerow(columns)