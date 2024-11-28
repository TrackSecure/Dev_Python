import mysql.connector
import platform
import time
import os

if (platform.system().lower()=="windows"):
    param = "-n 1"
else:
    param = "-c 1"

conector_db = mysql.connector.connect(host='localhost', port=3307, user="root", password="tracksecure", database="TrackSecure")
cursor = conector_db.cursor()

while(True):
    cursor.execute("SELECT MacAddress, ip FROM Servidor")

    servidores = cursor.fetchall()
    qtd_servidores = len(servidores)
    for i in range(qtd_servidores):
        resposta = os.system(f"ping {param} {servidores[i][1]}")
        status = resposta == 0 # Se a resposta for 0, não houve problema com o comando ping e o servidor está em uptime (status = True)
        fkServidor = servidores[i][0]
        sql = f"INSERT INTO ServidorStatus (uptime, fkServidor) VALUES ({status}, '{fkServidor}')"
        print(sql)
        cursor.execute(sql)
        conector_db.commit()
    time.sleep(600)