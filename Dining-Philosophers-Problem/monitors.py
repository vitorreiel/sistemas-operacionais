import threading
import time
import random

# Classe que representa o problema dos Filósofos Comensais com Monitores
class PhilosophersMonitors:
    def __init__(self, num_philosophers=5):
        self.num_philosophers = num_philosophers
        self.forks = [False for _ in range(num_philosophers)]  # False indica que o garfo está disponível
        self.condition = threading.Condition()  # Condição para sincronizar o uso dos garfos

    def dine(self, philosopher_id):
        left_fork = philosopher_id  # Garfo à esquerda
        right_fork = (philosopher_id + 1) % self.num_philosophers  # Garfo à direita

        for _ in range(5):
            print(f"(Monitors) Filósofo {philosopher_id} está pensando.")
            time.sleep(random.uniform(0.05, 0.2))  # Simula o tempo pensando

            with self.condition:
                while self.forks[left_fork] or self.forks[right_fork]:
                    self.condition.wait()  # Espera até que os garfos estejam disponíveis
                self.forks[left_fork] = True  # Pega o garfo à esquerda
                self.forks[right_fork] = True  # Pega o garfo à direita

            print(f"(Monitors) Filósofo {philosopher_id} está comendo.")
            time.sleep(random.uniform(0.05, 0.2))  # Simula o tempo comendo

            with self.condition:
                self.forks[left_fork] = False  # Devolve o garfo à esquerda
                self.forks[right_fork] = False  # Devolve o garfo à direita
                self.condition.notify_all()  # Notifica que os garfos estão disponíveis

            print(f"Filósofo {philosopher_id} terminou de comer e está devolvendo os garfos.")


# Função principal para rodar o teste
def run_philosophers_test(philosopher_class, num_philosophers=5):
    # Cria uma instância da classe dos filósofos
    philosophers = philosopher_class(num_philosophers)

    # Cria e inicia uma thread para cada filósofo
    threads = []
    for i in range(num_philosophers):
        t = threading.Thread(target=philosophers.dine, args=(i,))
        threads.append(t)
        t.start()

    # Aguarda todas as threads finalizarem
    for t in threads:
        t.join()

    print("Encerrando a simulação dos filósofos comensais. Todos os filósofos comeram 5 vezes.")


# Executa o teste com a implementação de monitores
if __name__ == "__main__":
    start_time = time.time()
    run_philosophers_test(PhilosophersMonitors)
    end_time = time.time()
    print(f"Tempo total de execução: {end_time - start_time:.2f}s")
