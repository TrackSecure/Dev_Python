import psutil
import time

def capturar_dados(listaComponentes, listaMonitorar, qtdCapturas, intervaloTempo):
    for i in range(qtdCapturas):
            print(f"\n\nCaptura {i + 1}:")
            for componente in listaComponentes:
                if componente == "CPU":
                    print("\nComponente: CPU")
                    if f"PorcentagemCPU" in listaMonitorar:
                        cpu_percent = psutil.cpu_percent(interval=1)
                        print(f"Uso de CPU: {cpu_percent}%")
                    if f"FreqCPU" in listaMonitorar:
                        cpu_freq = psutil.cpu_freq().current
                        print(f"Frequência da CPU: {cpu_freq} GHz")
                elif componente == "Memoria":
                    print("\nComponente: Memória")
                    if f"PorcentagemMemoria" in listaMonitorar:
                        ram_percent = psutil.virtual_memory().percent
                        print(f"Uso de Memória: {ram_percent}%")
                    if f"EspacoMemoria" in listaMonitorar:
                        ram_used = psutil.virtual_memory().used / (1024 ** 3)  
                        print(f"Memória usada: {ram_used} GB")
                elif componente == "Disco":
                    print("\nComponente: Disco")
                    if f"PorcentagemDisco" in listaMonitorar:
                        disk_percent = psutil.disk_usage('/').percent
                        print(f"Uso de Disco: {disk_percent}%")
                    if f"EspacoDisco" in listaMonitorar:
                        disk_used = psutil.disk_usage('/').used / (1024 ** 3)  
                        print(f"Espaço de Disco usado: {disk_used} GB")

            time.sleep(intervaloTempo)

def editar_dados(listaComponentes, listaMonitorar):
    while True:
        print(
        """
        \nVocê deseja 
        1 - Remover um componente
        2 - Adicionar um componente
        3 - Finalizar edição
        """)

        escolhaEditar = input("Digite a opção selecionada: ")

        if escolhaEditar == "1":
            print("\n Componentes monitorados")
            c = 1
            for a in listaComponentes:
                print(f"{c} - {a}")
                c += 1
            
            escolhaRemover = input("Digite os componentes que deseja remover (Separado por vírgula): ").split(',')

            k = 1
            for i in escolhaRemover:
                componente_removido = listaComponentes[int(i) - k]
                listaComponentes.pop(int(i) - k)
                print(f"Componente {componente_removido} removido da lista")
                k += 1
    
        
        elif escolhaEditar == "2":
            todosComponentes = ["CPU", "Memoria", "Disco"]

            componentesDisponiveis = [comp for comp in todosComponentes if comp not in listaComponentes]

            if componentesDisponiveis:
                print("\nComponentes disponíveis para adicionar: ")
                for idx, componente in enumerate(componentesDisponiveis, 1):
                    print(f"{idx} - {componente}")

                componentes_adicionar = input("Quais componentes deseja adicionar (Digite o número separado por vírgula): ").split(",")

                novosComponentes = []
                for idx in componentes_adicionar:
                    try:
                        idx = int(idx) - 1
                        if 0 <= idx < len(componentesDisponiveis):
                            novoComponente = componentesDisponiveis[idx]
                            listaComponentes.append(novoComponente)
                            novosComponentes.append(novoComponente)
                    except ValueError:
                        print("Entrada inválida, tente novamente.")
            else:
                print("Todos os componentes já estão sendo monitorados.")

            
            for componente in novosComponentes:
                print(f"\nNome do Componente: {componente}")
                print(f"""
                1 - Porcentagem
                2 - {"Frequência do processador" if componente == "CPU" else "GigaBytes de Uso"}      
                """)
                monitorar = input(f"O que do componente {componente} você deseja monitorar: ").split(',')

                if "1" in monitorar and f"Porcentagem{componente}" not in listaMonitorar:
                    listaMonitorar.append(f"Porcentagem{componente}")
                if "2" in monitorar and (f"Freq{componente}" if componente == "CPU" else f"Espaco{componente}") not in listaMonitorar:
                    listaMonitorar.append(f"{'Freq' if componente == 'CPU' else 'Espaco'}{componente}")

                else: 
                    break

        return listaComponentes, listaMonitorar


chave = 0

while chave != 2:
    print(
        """
        1 - Capturar Dados 
        2 - Sair
        """)

    chave = int(input("O que você deseja fazer: "))

    if chave == 1: 
        print("""
        1 - CPU
        2 - Memória 
        3 - Disco
        """)

        componentes = input("Quais componentes deseja monitorar (Digite o número separado por vírgula): ").split(",")

        listaComponentes = []

        if "1" in componentes:
            listaComponentes.append("CPU")
        if "2" in componentes:
            listaComponentes.append("Memoria")
        if "3" in componentes:
            listaComponentes.append("Disco")

        listaMonitorar = []

        for componente in listaComponentes:
            print(f" \n Nome do Componente: {componente}")

            print(f"""
            1 - Porcentagem
            2 - {"Frequência do processador" if componente == "CPU" else "GigaBytes de Uso"}      
            """)
            monitorar = input(f"O que do componente {componente} você deseja monitorar: ").split(',')

            if "1" in monitorar:
                listaMonitorar.append(f"Porcentagem{componente}")
            if "2" in monitorar:
               listaMonitorar.append(f"{'Freq' if componente == 'CPU' else 'Espaco'}{componente}")


        qtdCapturas = int(input("Quantas capturas deseja fazer? "))
        intervaloTempo = int(input("Qual o intervalo de tempo em segundos: "))

        capturar_dados(listaComponentes, listaMonitorar, qtdCapturas, intervaloTempo)

        while True:
            print(
            """
            \n Deseja remover ou adicionar algum componente ?
            1 - Sim
            2 - Não 
            """)
            escolhaEditar = input("Digite o número da opção selecionada: ")

            if escolhaEditar == "1":
                listaComponentes, listaMonitorar = editar_dados(listaComponentes, listaMonitorar)
                capturar_dados(listaComponentes, listaMonitorar, qtdCapturas, intervaloTempo)
            else:
                break

    else:
        print("Tchauu")
