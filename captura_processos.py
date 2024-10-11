import subprocess
import csv


# Executar o comando 'tasklist' e capturar a saída - este comando é o mesmo do CMD - sistema operacional
result = subprocess.run(['tasklist'], capture_output=True, text=True)

# Verificar o resultado da saída
print(result)

# Separar as linhas da saída está dando erro de ecoding no comando original
#lines = result.stdout.splitlines()
lines = result.stdout.splitlines()[2:]

# Abrir um arquivo CSV para escrita com codificação UTF-8  na mesma pasta deste projeto 
with open('tasks3.csv', 'w', newline='', encoding='utf-8') as csvfile:
    
    # Criar um objeto escritor CSV para importar
    csv_writer = csv.writer(csvfile)

    # Escrever o cabeçalho (opcional, ajustável de acordo com a saída do 'tasklist')
    csv_writer.writerow(['Nome_da_Imagem', 'PID', 'Nome_da_Sessao', 'Sessao#', 'Uso_de_memoria'])
   

    # Escrever as linhas de dados
    for line in lines:
        # Dividir a linha em colunas (ajustar os delimitadores se necessário)
        columns = line.split()
        csv_writer.writerow(columns)