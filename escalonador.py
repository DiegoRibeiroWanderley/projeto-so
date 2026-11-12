class Processo:

    # Atributos de cada processo
    def __init__(self, tempo_chegada: int, tempo_pico: int):
        self.tempo_chegada = tempo_chegada
        self.tempo_pico = tempo_pico
        self.tempo_retorno = 0
        self.tempo_resposta = 0
        self.tempo_espera = 0

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

    processos_copy = sorted(
        processos, key=lambda p: p.tempo_chegada
    )  # Cópia dos processos
    fila_fcfs = []  # Fila de processos
    em_execucao = []  # Processo em execução
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
        if fila_fcfs and not em_execucao:
            em_execucao.append(fila_fcfs[0])
            fila_fcfs.remove(fila_fcfs[0])

        # Contador incrementa em 1
        cont += 1

        # O processo em execução vai
        # Decrementar o tempo de pico necessário para conclusão
        # Incrementar o tempo retorno
        # E os outros processos na fila irão incrementar tempo de espera, resposta e retorno
        if em_execucao:
            em_execucao[0].tempo_pico -= 1
            em_execucao[0].tempo_retorno += 1
            for p in fila_fcfs:
                p.tempo_espera += 1
                p.tempo_resposta += 1
                p.tempo_retorno += 1
        # Como essa fila é FCFS tempo de espera == tempo de resposta

        # Se o processo em execução tiver seu tempo de pico faltando igual a 0
        # Então ele foi finalizado, logo sai do processo em execução e
        # Entra na lista de processos concluídos
        if em_execucao and em_execucao[0].tempo_pico == 0:
            processos_concluidos.append(em_execucao[0])
            em_execucao.pop()

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

    # Retorna as médias dos tempos
    return f"FCFS {tempo_retorno:.1f} {tempo_resposta:.1f} {tempo_espera:.1f}"


def main():

    # Lê os processos
    processos = instancia_processos("processos.txt")
    # Printa as estatísticas segundo o algoritmo FCFS
    print(first_come_first_served(processos=processos))


if __name__ == "__main__":
    main()
