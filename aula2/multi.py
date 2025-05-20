import multiprocessing
import time

def tarefa(numero:int) -> None:
    print(f"Inicio da Tarefa {numero}")
    time.sleep(3)
    print(f"Fim da tarefa{numero}")

def main() -> None:
    processos  = []
    for i in range(1,5):
        p= multiprocessing.Process(target=tarefa,args=(i,))
        processos.append(p)
        p.start()
    for p in processos:
        print()
        p.join()

if __name__ == "__main__":
    main()