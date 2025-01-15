import threading
import time
import random
import matplotlib.pyplot as plt
import os
import csv
import pandas as pd

# Verifica e cria os diretórios "graficos" e "dataset" se não existirem
if not os.path.exists("graficos"):
    os.makedirs("graficos")
if not os.path.exists("dataset"):
    os.makedirs("dataset")

# Implementação da classe utilizando Semáforos para resolver o problema dos Filósofos Comensais
class PhilosophersSemaphores:
    def __init__(self, num_philosophers=5):
        self.num_philosophers = num_philosophers
        # Cria um semáforo para cada garfo
        self.forks = [threading.Semaphore(1) for _ in range(num_philosophers)]

    def dine(self, philosopher_id):
        # Define os garfos esquerdo e direito para cada filósofo
        left_fork = philosopher_id
        right_fork = (philosopher_id + 1) % self.num_philosophers

        for _ in range(5):  # Cada filósofo realiza o ciclo 5 vezes
            print(f"(Semaphores) Filósofo {philosopher_id} está pensando.")
            time.sleep(random.uniform(0.05, 0.2))  # Simula o tempo de pensar
            # Pega os garfos (semáforos)
            self.forks[left_fork].acquire()
            self.forks[right_fork].acquire()
            print(f"(Semaphores) Filósofo {philosopher_id} está comendo.")
            time.sleep(random.uniform(0.05, 0.2))  # Simula o tempo de comer
            # Libera os garfos (semáforos)
            self.forks[left_fork].release()
            self.forks[right_fork].release()

# Implementação da classe utilizando Monitores
class PhilosophersMonitors:
    def __init__(self, num_philosophers=5):
        self.num_philosophers = num_philosophers
        # Estado dos garfos: True se ocupado, False se livre
        self.forks = [False for _ in range(num_philosophers)]
        self.condition = threading.Condition()  # Condição para controle de acesso

    def dine(self, philosopher_id):
        left_fork = philosopher_id
        right_fork = (philosopher_id + 1) % self.num_philosophers

        for _ in range(5):
            print(f"(Monitors) Filósofo {philosopher_id} está pensando.")
            time.sleep(random.uniform(0.05, 0.2))
            with self.condition:
                # Aguarda até que os dois garfos estejam disponíveis
                while self.forks[left_fork] or self.forks[right_fork]:
                    self.condition.wait()
                # Reserva os garfos
                self.forks[left_fork] = True
                self.forks[right_fork] = True
            print(f"(Monitors) Filósofo {philosopher_id} está comendo.")
            time.sleep(random.uniform(0.05, 0.2))
            with self.condition:
                # Libera os garfos e notifica outros threads
                self.forks[left_fork] = False
                self.forks[right_fork] = False
                self.condition.notify_all()

# Implementação da classe utilizando Locks/Mutexes
class PhilosophersLocks:
    def __init__(self, num_philosophers=5):
        self.num_philosophers = num_philosophers
        # Cria um lock para cada garfo
        self.forks = [threading.Lock() for _ in range(num_philosophers)]

    def dine(self, philosopher_id):
        left_fork = philosopher_id
        right_fork = (philosopher_id + 1) % self.num_philosophers

        for _ in range(5):
            print(f"(Locks/Mutexes) Filósofo {philosopher_id} está pensando.")
            time.sleep(random.uniform(0.05, 0.2))
            # Garante exclusão mútua nos dois garfos
            with self.forks[left_fork]:
                with self.forks[right_fork]:
                    print(f"(Locks/Mutexes) Filósofo {philosopher_id} está comendo.")
                    time.sleep(random.uniform(0.05, 0.2))

# Função para executar os testes com threads
def run_philosophers_test(philosopher_class, num_philosophers=5):
    philosophers = philosopher_class(num_philosophers)
    threads = []

    # Cria uma thread para cada filósofo
    for i in range(num_philosophers):
        t = threading.Thread(target=philosophers.dine, args=(i,))
        threads.append(t)
        t.start()

    # Aguarda todas as threads terminarem
    for t in threads:
        t.join()

# Função para medir o tempo de execução de cada implementação
def measure_time(philosopher_class, label):
    print(f"Iniciando teste: {label}")
    start_time = time.time()  # Marca o início do teste
    run_philosophers_test(philosopher_class)
    end_time = time.time()  # Marca o fim do teste
    execution_time = end_time - start_time
    print(f"{label} concluído. Tempo total: {execution_time:.2f}s\n")
    return execution_time

# Pergunta ao usuário o número de repetições para os testes
repeat_count = int(input("Quantas vezes esses testes serão repetidos? "))

# Cria um arquivo CSV para salvar os resultados dos testes
dataset_path = "dataset/dataset.csv"
with open(dataset_path, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Execução", "Semáforos", "Monitores", "Locks/Mutexes"])

    # Realiza as repetições solicitadas
    for i in range(1, repeat_count + 1):
        print(f"Iniciando execução {i} de {repeat_count}...")
        tempos = {
            "Semáforos": measure_time(PhilosophersSemaphores, "Semáforos"),
            "Monitores": measure_time(PhilosophersMonitors, "Monitores"),
            "Locks/Mutexes": measure_time(PhilosophersLocks, "Locks/Mutexes"),
        }
        writer.writerow([i, tempos["Semáforos"], tempos["Monitores"], tempos["Locks/Mutexes"]])

# Leitura do dataset e geração do gráfico comparativo
data = pd.read_csv(dataset_path)
avg_times = data.mean().iloc[1:]

# Criação do gráfico de barras para comparar tempos médios
plt.bar(avg_times.index, avg_times.values, color=['blue', 'green', 'orange'])
plt.ylim(0, max(avg_times.values) * 1.2)
for i, value in enumerate(avg_times.values):
    plt.text(i, value + 0.05, f"{value:.2f}s", ha='center', va='bottom')
plt.xlabel('Mecanismo de Exclusão Mútua')
plt.ylabel('Tempo Médio de Execução (s)')
plt.title('Comparação Média de Tempos de Execução - Filósofos Comensais')
plt.savefig("graficos/comparison_average.png")
