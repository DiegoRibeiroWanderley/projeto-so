"""
Dupla:
- Diego Ribeiro Wanderley - 20250017738
- Saulo Ramos Rodrigues - 20250017818
"""

import sys


class Processo:

    # Atributos de cada processo
    def __init__(self, tempo_chegada: int, tempo_pico: int):
        self.tempo_chegada = tempo_chegada
        self.tempo_pico = tempo_pico
        self.tempo_retorno = 0
        self.tempo_resposta = 0
        self.tempo_espera = 0
        self.resposta_definida = False  # True quando tempo de resposta foi definido

    def __str__(self):
        return f"{self.tempo_chegada} {self.tempo_pico} {self.tempo_resposta} {self.tempo_espera} {self.tempo_retorno}"


# Lê os processos do arquivo de entrada
def instancia_processos(nome_arquivo: str):

    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.readlines()
        processos = []
        # Adiciona os processos a uma lista
        for line in conteudo:
            processos.append(Processo(int(line.split()[0]), int(line.split()[1])))
        # Retorna a lista de processos
        return processos


def first_come_first_served(processos: list):
    # Cria cópias dos processos para não modificar os originais
    processos_copy = sorted(
        [Processo(p.tempo_chegada, p.tempo_pico) for p in processos],
        key=lambda p: p.tempo_chegada,
    )
    fila_fcfs = []  # Fila de processos
    em_execucao = None  # Processo em execução
    processos_concluidos = []  # Processos concluídos
    cont = 0  # Contador

    # Enquanto todos os processos ainda não tiverem sido concluídos executa
    while len(processos_concluidos) != len(processos):

        # Vê quais processos chegaram no momento e
        # coloca-os na fila e retira-os da lista de processos
        while processos_copy and processos_copy[0].tempo_chegada == cont:
            fila_fcfs.append(processos_copy[0])
            processos_copy.remove(processos_copy[0])

        # Se tiver alguém na fila e ninguém executando
        # Retira da fila e começa a execução
        # (while: processo com pico 0 conclui na hora e o próximo é despachado)
        while fila_fcfs and em_execucao is None:
            em_execucao = fila_fcfs.pop(0)
            # Tempo de resposta: quanto esperou desde a chegada até ganhar a CPU
            em_execucao.tempo_resposta = cont - em_execucao.tempo_chegada
            if em_execucao.tempo_pico == 0:
                processos_concluidos.append(em_execucao)
                em_execucao = None

        # Contador incrementa em 1
        cont += 1

        # O processo em execução vai:
        # Decrementar o tempo de pico necessário para conclusão
        # Incrementar o tempo retorno
        # E os outros processos na fila irão incrementar tempo de espera e retorno
        if em_execucao:
            em_execucao.tempo_pico -= 1
            em_execucao.tempo_retorno += 1
            for p in fila_fcfs:
                p.tempo_espera += 1
                p.tempo_retorno += 1
        # Como essa fila é FCFS tempo de espera == tempo de resposta

        # Se o processo em execução tiver seu tempo de pico faltando igual a 0
        # Então ele foi finalizado, logo sai do processo em execução e
        # Entra na lista de processos concluídos
        if em_execucao and em_execucao.tempo_pico <= 0:
            processos_concluidos.append(em_execucao)
            em_execucao = None

    # Calcula o tempo médio dos tempos de retorno, resposta e espera
    tempo_retorno = sum(p.tempo_retorno for p in processos_concluidos) / len(
        processos_concluidos
    )
    tempo_resposta = sum(p.tempo_resposta for p in processos_concluidos) / len(
        processos_concluidos
    )
    tempo_espera = sum(p.tempo_espera for p in processos_concluidos) / len(
        processos_concluidos
    )

    # Retorna as médias dos tempos (usando vírgula como separador decimal)
    return f"FCFS {tempo_retorno:.1f} {tempo_resposta:.1f} {tempo_espera:.1f}".replace(
        ".", ","
    )


def shortest_job_first(processos: list):
    # Cria cópias dos processos para não modificar os originais
    processos_copy = sorted(
        [Processo(p.tempo_chegada, p.tempo_pico) for p in processos],
        key=lambda p: p.tempo_chegada,
    )
    fila_prontos = []  # Fila de processos prontos
    em_execucao = None  # Processo em execução
    processos_concluidos = []  # Processos concluídos
    cont = 0  # Contador de tempo

    # Enquanto todos os processos ainda não tiverem sido concluídos executa
    while len(processos_concluidos) != len(processos):
        # Vê quais processos chegaram no momento e coloca-os na fila
        while processos_copy and processos_copy[0].tempo_chegada == cont:
            fila_prontos.append(processos_copy[0])
            processos_copy.remove(processos_copy[0])

        # Se não tiver ninguém executando e houver processos na fila
        # Escolhe o processo com menor tempo de pico (SJF não-preemptivo)
        # (while: processo com pico 0 conclui na hora e o próximo é despachado)
        while em_execucao is None and fila_prontos:
            # Ordena por tempo de pico (menor primeiro)
            fila_prontos.sort(key=lambda p: p.tempo_pico)
            em_execucao = fila_prontos.pop(0)
            # Tempo de resposta: quanto esperou desde a chegada até ganhar a CPU
            em_execucao.tempo_resposta = cont - em_execucao.tempo_chegada
            if em_execucao.tempo_pico == 0:
                processos_concluidos.append(em_execucao)
                em_execucao = None

        # Incrementa o contador
        cont += 1

        # O processo em execução decrementa seu tempo de pico
        # Incrementa o tempo de retorno
        # Processos na fila incrementam tempo de espera e retorno
        if em_execucao:
            em_execucao.tempo_pico -= 1
            em_execucao.tempo_retorno += 1
            for p in fila_prontos:
                p.tempo_espera += 1
                p.tempo_retorno += 1

        # Se o processo em execução terminou
        if em_execucao and em_execucao.tempo_pico <= 0:
            processos_concluidos.append(em_execucao)
            em_execucao = None

    # Calcula as médias
    tempo_retorno = sum(p.tempo_retorno for p in processos_concluidos) / len(
        processos_concluidos
    )
    tempo_resposta = sum(p.tempo_resposta for p in processos_concluidos) / len(
        processos_concluidos
    )
    tempo_espera = sum(p.tempo_espera for p in processos_concluidos) / len(
        processos_concluidos
    )

    return f"SJF {tempo_retorno:.1f} {tempo_resposta:.1f} {tempo_espera:.1f}".replace(
        ".", ","
    )


def round_robin(processos: list, quantum: int = 2):
    # Cria cópias dos processos para não modificar os originais
    processos_copy = sorted(
        [Processo(p.tempo_chegada, p.tempo_pico) for p in processos],
        key=lambda p: p.tempo_chegada,
    )
    fila_prontos = []  # Fila de processos prontos
    em_execucao = None  # Processo em execução
    processos_concluidos = []  # Processos concluídos
    cont = 0  # Contador de tempo
    tempo_quantum = 0  # Contador de quantum atual
    preempted = None  # Processo preemptado no final da unidade de tempo anterior

    # Enquanto todos os processos ainda não tiverem sido concluídos executa
    while len(processos_concluidos) != len(processos):
        # 1. Adiciona chegadas no tempo atual (devem entrar antes do preemptado)
        while processos_copy and processos_copy[0].tempo_chegada == cont:
            fila_prontos.append(processos_copy[0])
            processos_copy.remove(processos_copy[0])

        # 2. Adiciona processo preemptado do final da unidade de tempo anterior
        if preempted is not None:
            fila_prontos.append(preempted)
            preempted = None

        # 3. Se CPU ocioso, despacha próximo processo
        # (while: processo com pico 0 conclui na hora e o próximo é despachado)
        while em_execucao is None and fila_prontos:
            em_execucao = fila_prontos.pop(0)
            tempo_quantum = 0
            # Marca o tempo de resposta (primeira vez que ganha CPU)
            if not em_execucao.resposta_definida:
                em_execucao.tempo_resposta = cont - em_execucao.tempo_chegada
                em_execucao.resposta_definida = True
            if em_execucao.tempo_pico == 0:
                processos_concluidos.append(em_execucao)
                em_execucao = None

        # 4. Executa por uma unidade de tempo (cont a cont+1)
        cont += 1

        if em_execucao:
            em_execucao.tempo_pico -= 1
            em_execucao.tempo_retorno += 1
            tempo_quantum += 1
            for p in fila_prontos:
                p.tempo_espera += 1
                p.tempo_retorno += 1

        # 5. Verifica término ou preempção para a PRÓXIMA iteração
        if em_execucao and em_execucao.tempo_pico <= 0:
            processos_concluidos.append(em_execucao)
            em_execucao = None
            tempo_quantum = 0
        elif em_execucao and tempo_quantum == quantum:
            preempted = em_execucao
            em_execucao = None
            tempo_quantum = 0

    # Calcula as médias
    tempo_retorno = sum(p.tempo_retorno for p in processos_concluidos) / len(
        processos_concluidos
    )
    tempo_resposta = sum(p.tempo_resposta for p in processos_concluidos) / len(
        processos_concluidos
    )
    tempo_espera = sum(p.tempo_espera for p in processos_concluidos) / len(
        processos_concluidos
    )

    return f"RR {tempo_retorno:.1f} {tempo_resposta:.1f} {tempo_espera:.1f}".replace(
        ".", ","
    )


def main():

    # Aceita um arquivo informado na linha de comando; sem argumento, lê stdin.
    if len(sys.argv) > 1:
        processos_originais = instancia_processos(sys.argv[1])
    else:
        valores = sys.stdin.read().split()
        processos_originais = [
            Processo(int(valores[i]), int(valores[i + 1]))
            for i in range(0, len(valores) - 1, 2)
        ]

    if not processos_originais:
        return

    # Cria cópias frescas para cada algoritmo
    def criar_processos(lista):
        return [Processo(p.tempo_chegada, p.tempo_pico) for p in lista]

    # Printa as estatísticas segundo cada algoritmo
    print(first_come_first_served(processos=criar_processos(processos_originais)))
    print(shortest_job_first(processos=criar_processos(processos_originais)))
    print(round_robin(processos=criar_processos(processos_originais)))


if __name__ == "__main__":
    main()
