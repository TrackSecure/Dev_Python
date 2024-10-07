import psutil
import time
import mysql.connector
import platform
from socket import gethostname

# Chave que vai declarar quando sair do WHILE
chave = 0

fkServidor = 0
# Variável para capturar o nome da máquina que será realizada a captura

nomeMaquina = gethostname()
maquinaExiste = False
# Conexão feita com o banco de dados

db_connection = mysql.connector.connect(
    host="10.18.32.12", 
    user="capturaDados", 
    passwd="SPTech#2024", 
    database="TrackSecure"
)


# Variavel para enviar e fazer comandos MySQL

cursor = db_connection.cursor()

# Seleciona todos os nomes que já existem se servidores

cursor.execute("SELECT nome FROM Servidor")

listaNomes = []

resultadoBanco = cursor.fetchall()

# Coloca esse resultado em uma lista 

for linha in resultadoBanco:
    listaNomes.append(linha[0]) 

# Verifica se esse nome já existe cadastrado, baseado no nome de sua máquina 
for nome in listaNomes:
    if nome == nomeMaquina:
        maquinaExiste = True
        break

# Se não existir, ele cadastra, se existir ele seleciona o id dela para colocar no insert

if maquinaExiste == False:
    insert = "INSERT INTO Servidor VALUES (DEFAULT, %s, 1)"
    cursor.execute(insert, [nomeMaquina])
    db_connection.commit()
    cursor.execute('SELECT idServidor FROM Servidor ORDER BY idServidor DESC LIMIT 1')
    fkServidor = (int(cursor.fetchone()) + 1)[0]
else:
    cursor.execute('SELECT idServidor FROM Servidor WHERE nome = %s', (nomeMaquina,))
    fkServidor = cursor.fetchone()[0]


if db_connection.is_connected():
    print("A Conexão ao MySql foi iniciada ")
else:
    print("Houve erro ao conectar")


while chave != 2:
    # Pergunta ao usuário o que ele deseja 
     
    chave = int(input(("O que deseja Fazer: \n 1 - Capturar Dados \n 2 - Sair \n ")))

    if chave == 1:
        # Se ele desejar fazer capturas, capturará quantidade a digitar com tempo estipulado pelo input também

        qtdCapturas = int(input(("Quantas capturas deseja fazer? \n ")))
        intervaloTempo = int(input(("Qual o intervalo de tempo em segundos: ")))

        # Começará a rodar as capturas, até o limte desejado

        for i in range(qtdCapturas):
            qtd_core = psutil.cpu_count(logical=False)

            cpu_porcent = psutil.cpu_percent(interval=1)
            cpu_speed = psutil.cpu_freq().current / pow(10,3)
            cpu_speed_max = psutil.cpu_freq().max / pow(10,3)   
            
            # Validação para saber o sistema operacional, para captura do disco
            so = platform.system()

            if (so == 'Windows'):
                # DIRETÓRIO PARA WINDOWS    
                disc_total = psutil.disk_usage('C:\\').total / pow(10,9)
                disc_used = psutil.disk_usage('C:\\').used / pow(10,9)
                disc_percent = psutil.disk_usage('C:\\').percent
            elif (so == 'Linux'):
                # DIRETÓRIO PARA LINUX
                disc_total = psutil.disk_usage('/bin').total / pow(10,9)
                disc_used = psutil.disk_usage('/bin').used / pow(10,9)
                disc_percent = psutil.disk_usage('/bin').percent    

            ram_total = (psutil.virtual_memory().total) / pow(10,9)
            ram_used = (psutil.virtual_memory().used) / pow(10,9)
            ram_percent = psutil.virtual_memory().percent

            # Cria uma mensagem, com valores arredondados e printa essa mensagem

            mensagem = f"""
                      {i + 1}º captura   
                      Máquina: {nomeMaquina}
                      SO: {so}
                      Quantidade de CPUs: {qtd_core}
                      Uso da CPU: {cpu_porcent:.2f}%
                      Frequência de Uso da CPU: {cpu_speed:.2f}Mhz
                      Máximo de freqência da CPU: {cpu_speed_max:.2f}Mhz
                      Total de memória: {ram_total:.2f} GB
                      Uso em GB RAM: {ram_used:.2f} GB
                      Uso da memória RAM: {ram_percent:.2f} %
                      Tamanho do disco: {disc_total:.2f} GB
                      Uso do disco: {disc_used:.2f} GB
                      Porcentagem Disco usada: {disc_percent:.2f} %
                      """
            
            print(mensagem)

            # Coloca um intervalo de tempo a captura 

            time.sleep(intervaloTempo)

            sql = "INSERT INTO Registro (so, dtHora, porcentagemProcessador, freqProcessador, freqMaxProcessador, porcentagemMemoria, memoriaUsada, memoriaTotal, porcentagemDisco, discoTotal, discoUsado, fkServidor) VALUES (%s, now(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

            values = (so, round(cpu_porcent, 2), round(cpu_speed, 2), round(cpu_speed_max, 2), round(ram_percent, 2), 
                      round(ram_used, 2), round(ram_total, 2), round(disc_percent, 2), round(disc_total, 2), round(disc_used, 2), fkServidor)

            cursor.execute(sql, values)
            db_connection.commit()
    else:
        print("Tchauuu :)")

