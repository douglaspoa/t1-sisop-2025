# 📘 Implementação de um Escalonador de Processos

## 1️⃣ Introdução

Este documento apresenta a implementação de um **escalonador de processos** baseado em prioridades, conforme descrito no **Trabalho 1 (T1)** da disciplina de Sistemas Operacionais. O código foi desenvolvido em **Python** e segue as diretrizes discutidas no enunciado do trabalho.

A implementação considera:
- **Estados do processo**: Ready, Running, Blocked e Exit.
- **Escalonamento baseado em créditos**.
- **Controle de entrada e saída (E/S)**.
- **Redistribuição de créditos** quando necessário.
- **Habilitação opcional de logs para depuração**.

Abaixo, detalhamos a estrutura do código e explicamos, trecho por trecho, como ele resolve os problemas propostos no **T1**.

---

## 2️⃣ Estrutura e Explicação do Código

### 📝 Definição da Classe Processo

```python
class Processo:
    def __init__(self, nome, surto_cpu, tempo_io, tempo_total_cpu, ordem, prioridade):
        self.nome = nome
        self.surto_cpu = surto_cpu  # Tempo de CPU antes de uma operação de E/S
        self.tempo_io = tempo_io  # Tempo que fica bloqueado por E/S
        self.tempo_total_cpu = tempo_total_cpu  # Tempo total necessário na CPU
        self.ordem = ordem  # Critério de desempate
        self.prioridade = prioridade  # Define a prioridade do processo
        self.creditos = prioridade  # Inicialmente, os créditos são iguais à prioridade
        self.estado = "Ready"  # Estado inicial
        self.tempo_restante = tempo_total_cpu  # Tempo restante de CPU
        self.tempo_bloqueado = 0  # Tempo de espera na fila de bloqueados
        self.tempo_proximo_io = surto_cpu  # Quando ocorre a próxima E/S
```

📌 **Explicação:**
- A classe `Processo` define a estrutura de um processo no sistema, armazenando informações essenciais para o escalonamento.
- O **tempo de surto de CPU** (`surto_cpu`) indica o tempo de uso da CPU antes de um processo necessitar de entrada/saída (E/S).
- O **tempo de E/S** (`tempo_io`) representa o período em que o processo ficará bloqueado aguardando a operação de entrada e saída.
- O **tempo total de CPU** (`tempo_total_cpu`) é o tempo necessário para o processo concluir sua execução.
- A **ordem** (`ordem`) é utilizada para resolver empates entre processos de mesma prioridade.
- A **prioridade** (`prioridade`) determina a importância do processo no escalonamento e influencia a distribuição de créditos.

---

### 🔄 Inserção dos Processos na Fila de Prontos

```python
def escalonador(processos):
    tempo_atual = 0
    fila_prontos = []  # Fila de processos prontos
    fila_bloqueados = []  # Processos esperando E/S

    for p in processos:
        heapq.heappush(fila_prontos, p)  # Insere processos na fila ordenada por prioridade
```

📌 **Explicação:**
- A lista `fila_prontos` representa a **fila de processos prontos** para execução.
- A **função `heapq.heappush(fila_prontos, p)`** insere os processos na fila de prontos utilizando um **heap** (min-heap por padrão).
- A classe `Processo` implementa um **método `__lt__`** para modificar o comportamento do heap:

```python
    def __lt__(self, outro):
        if self.creditos == outro.creditos:
            return self.ordem < outro.ordem  # Critério de desempate
        return self.creditos > outro.creditos  # O maior crédito tem prioridade
```

- Dessa forma, o **processo com maior número de créditos sempre será selecionado primeiro**.
- Caso dois processos tenham a mesma quantidade de créditos, a **ordem de chegada** (`ordem`) é usada como critério de desempate.

---

### ⏳ Gerenciamento de E/S e Bloqueio

```python
    while fila_prontos or fila_bloqueados:
        for p in list(fila_bloqueados):
            p.tempo_bloqueado -= 1
            if p.tempo_bloqueado <= 0:
                heapq.heappush(fila_prontos, p)
                fila_bloqueados.remove(p)
```

📌 **Explicação:**
- Este trecho de código simula a **execução dos processos e a transição de estados**.
- A cada ciclo de execução, o escalonador percorre a fila de bloqueados (`fila_bloqueados`).
- Se um processo está bloqueado, seu **tempo de bloqueio (`tempo_bloqueado`) é reduzido**.
- Quando o tempo de bloqueio atinge **zero**, o processo volta para a fila de prontos (`fila_prontos`).
- Esse mecanismo garante que processos **não executem enquanto aguardam operações de E/S**, conforme exigido no **Trabalho 1 (T1)**.

---

### 🔄 Redistribuição de Créditos

```python
        if fila_prontos and all(p.creditos == 0 for p in fila_prontos):
            for p in fila_prontos:
                p.creditos = (p.creditos // 2) + p.prioridade
```

📌 **Explicação:**
- Quando **todos os processos da fila de prontos ficam sem créditos**, o escalonador redistribui os créditos de acordo com a fórmula descrita no **T1**:

  **cred = cred/2 + prioridade**

- Essa redistribuição evita que **processos de baixa prioridade fiquem indefinidamente sem execução** (**problema de starvation**).

---

## 3️⃣ Execução do Programa

✅ **Modo normal (sem logs)**
```bash
python main.py
```

✅ **Modo depuração (com logs detalhados)**
```bash
python main.py logs
```

📌 **Explicação:**
- Se o argumento `logs` for passado, a execução exibirá **detalhes do escalonamento**.
- Isso facilita a **depuração do código** e a análise da lógica de escalonamento.

---

## 4️⃣ Conclusão

Este projeto implementa um **simulador de escalonamento de processos** utilizando **Python** e seguindo as diretrizes do **Trabalho 1 (T1)**. O código resolve os seguintes problemas:

✔ **Seleciona processos com base em prioridade e créditos**.✔ **Gerencia operações de E/S e bloqueio corretamente**.✔ **Redistribui créditos para evitar starvation**.✔ **Utiliza logs opcionais para facilitar a depuração**.

Com isso, conseguimos aplicar os conceitos teóricos na prática, garantindo um **escalonador funcional e eficiente**. 🚀
