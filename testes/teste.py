import threading
import time

# Função que será chamada pela thread
def minha_funcao1():
    print("Esta é a função 1 sendo executada pela thread")
    time.sleep(2)
    minha_funcao2()
    print("A função 1 terminou sua execução")
    # Após terminar, chama a função 2

# Outra função do código
def minha_funcao2():
    print("Esta é a função 2 chamada pela função 1")

# Criando e iniciando a thread
minha_thread = threading.Thread(target=minha_funcao1)
minha_thread.start()

# O restante do código continua sendo executado enquanto a thread roda em paralelo
print("Aqui está o restante do código")

# Espera a thread terminar para continuar
minha_thread.join()

print("O programa terminou completamente")
