import heapq
import sys

# Ativa logs apenas se "logs" for passado na linha de comando
LOGS_ATIVADOS = "logs" in sys.argv

def log(msg):
    """Exibe logs apenas se a opção estiver ativada."""
    if LOGS_ATIVADOS:
        print(msg)

class Processo:
    def __init__(self, nome, surto_cpu, tempo_io, tempo_total_cpu, ordem, prioridade):
        self.nome = nome
        self.surto_cpu = surto_cpu
        self.tempo_io = tempo_io
        self.tempo_total_cpu = tempo_total_cpu
        self.ordem = ordem
        self.prioridade = prioridade
        self.creditos = prioridade
        self.estado = "Ready"
        self.tempo_restante = tempo_total_cpu
        self.tempo_bloqueado = 0
        self.tempo_proximo_io = surto_cpu

    def __lt__(self, outro):
        if self.creditos == outro.creditos:
            return self.ordem < outro.ordem
        return self.creditos > outro.creditos

def escalonador(processos):
    tempo_atual = 0
    fila_prontos = []
    fila_bloqueados = []

    for p in processos:
        heapq.heappush(fila_prontos, p)

    log("\n=== Iniciando Escalonamento ===\n")

    while fila_prontos or fila_bloqueados:
        for p in list(fila_bloqueados):
            p.tempo_bloqueado -= 1
            if p.tempo_bloqueado <= 0:
                log(f"[{tempo_atual}ms] {p.nome} saiu da fila de bloqueados e voltou para prontos.")
                p.estado = "Ready"
                heapq.heappush(fila_prontos, p)
                fila_bloqueados.remove(p)

        if not fila_prontos:
            tempo_atual += 1
            continue

        processo_atual = heapq.heappop(fila_prontos)
        processo_atual.estado = "Running"
        log(f"[{tempo_atual}ms] Executando {processo_atual.nome} (Créditos: {processo_atual.creditos})")

        exec_time = min(1, processo_atual.tempo_restante)
        tempo_atual += exec_time
        processo_atual.tempo_restante -= exec_time
        processo_atual.creditos -= 1

        if processo_atual.tempo_restante > 0 and processo_atual.tempo_proximo_io is not None:
            processo_atual.tempo_proximo_io -= exec_time
            if processo_atual.tempo_proximo_io == 0:
                log(f"[{tempo_atual}ms] {processo_atual.nome} entrou na fila de bloqueados por {processo_atual.tempo_io}ms.")
                processo_atual.estado = "Blocked"
                processo_atual.tempo_bloqueado = processo_atual.tempo_io
                processo_atual.tempo_proximo_io = processo_atual.surto_cpu
                fila_bloqueados.append(processo_atual)
                continue

        if processo_atual.tempo_restante > 0:
            heapq.heappush(fila_prontos, processo_atual)
        else:
            log(f"[{tempo_atual}ms] {processo_atual.nome} finalizado.")

        if fila_prontos and all(p.creditos == 0 for p in fila_prontos):
            log(f"[{tempo_atual}ms] Redistribuindo créditos...")
            for p in fila_prontos:
                p.creditos = (p.creditos // 2) + p.prioridade

    log("\n=== Escalonamento Finalizado ===")

if __name__ == "__main__":
    processos = [
        Processo("A", 2, 5, 6, 1, 3),
        Processo("B", 3, 10, 6, 2, 3),
        Processo("C", None, None, 14, 3, 3),
        Processo("D", None, None, 10, 4, 3)
    ]

    escalonador(processos)  