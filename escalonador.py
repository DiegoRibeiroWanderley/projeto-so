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

    # Cria a fila de processos FCFS
    fila_fcfs = sorted(processos, key=lambda p: p.tempo_chegada)
    # Cria uma lista para os processos concluídos
    processos_resu = []
    # Contador para controlar o tempo de chegada dos processos
    cont = 0

    # Enquanto tiver elementos na fila executa
    while fila_fcfs:

        # Se o tempo de chegada for menor que o contador, ele vira o contador atual
        cont = fila_fcfs[0].tempo_chegada if cont < fila_fcfs[0].tempo_chegada else cont
        # Tempo de resposta e espera = contador - tempo de chegada
        # São iguais por conta do funcionamento da fila no FCFS
        fila_fcfs[0].tempo_resposta = cont - fila_fcfs[0].tempo_chegada
        fila_fcfs[0].tempo_espera = cont - fila_fcfs[0].tempo_chegada
        # Acrescenta ao contador o tempo de pico (processo foi executado)
        cont += fila_fcfs[0].tempo_pico
        # Tempo de retorno = contador (após a execução) - tempo de chegada
        fila_fcfs[0].tempo_retorno = cont - fila_fcfs[0].tempo_chegada

        # Põe o processo na fila de processos concluídos e retira-o da fila
        processos_resu.append(fila_fcfs[0])
        fila_fcfs.remove(fila_fcfs[0])

    # Calcula o tempo médio dos tempos de retorno, resposta e espera
    tempo_retorno = sum(p.tempo_retorno for p in processos_resu) / len(processos_resu)
    tempo_resposta = sum(p.tempo_resposta for p in processos_resu) / len(processos_resu)
    tempo_espera = sum(p.tempo_espera for p in processos_resu) / len(processos_resu)

    # Retorna as médias dos tempos
    return f"FCFS {tempo_retorno:.1f} {tempo_resposta:.1f} {tempo_espera:.1f}"


def main():

    # Lê os processos
    processos = instancia_processos("processos.txt")
    # Printa as estatísticas segundo o algoritmo FCFS
    print(first_come_first_served(processos=processos))


if __name__ == "__main__":
    main()
