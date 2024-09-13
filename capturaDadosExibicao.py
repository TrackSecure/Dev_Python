import psutil
import time
import platform
from socket import gethostname

nomeMaquina = gethostname()

while True:
        qtdCapturas = int(input(("Quantas capturas deseja fazer? \n ")))
        intervaloTempo = int(input(("Qual o intervalo de tempo em segundos: ")))

        for i in range(qtdCapturas):
            qtd_core = psutil.cpu_count(logical=False)

            cpu_porcent = psutil.cpu_percent(interval=1)
            cpu_speed = psutil.cpu_freq().current / pow(10,3)
            cpu_speed_max = psutil.cpu_freq().max / pow(10,3)   
            
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