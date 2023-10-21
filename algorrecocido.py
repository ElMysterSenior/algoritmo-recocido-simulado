import random
import math
import matplotlib.pyplot as plt

T = 1000
Tf = 0.01
Alpha = 0.94 #Factor de enfriamiento (explora mas soluciones)
tamaño_ciclo = 1000 #Ciclos de la metropolis
peso_maximo = 2.1
calorias_minimas = 2700


with open("lista_productos.txt", "r") as archivo:
    lineas = archivo.readlines()

valores = []
for linea in lineas:
    partes = linea.strip().split(',')
    nombre_producto = partes[0]
    valor1 = float(partes[1])
    valor2 = int(partes[2])
    array_valores = [nombre_producto, valor1, valor2]
    valores.append(array_valores)

def crear_solucion(num_lineas):
    return [random.randint(0, 1) for _ in range(num_lineas)]

def evaluar_solucion(solucion):
    peso_total, calorias_totales = 0, 0
    for i in range(len(solucion)):
        if solucion[i] == 1:
            peso_total += valores[i][1]
            calorias_totales += valores[i][2]
    if peso_total > peso_maximo or calorias_totales < calorias_minimas:
        return peso_total, 0
    return peso_total, calorias_totales

def mutar(solucion):
    indice_gen_a_mutar = random.randint(0, len(solucion) - 1)
    solucion_mutada = solucion.copy()
    solucion_mutada[indice_gen_a_mutar] = 1 - solucion_mutada[indice_gen_a_mutar]
    return solucion_mutada


energias = []
temperaturas = []
probabilidades = []

S = crear_solucion(len(valores))
ES = evaluar_solucion(S)[1]

Smejor = S
ESmejor = ES

while T > Tf:
    n = 1
    while n < tamaño_ciclo:
        Snew = mutar(S)
        ESnew = evaluar_solucion(Snew)[1]
        Dif = ESnew -ES
        
        # Almacenamos la energía y temperatura actuales
        energias.append(ES)
        temperaturas.append(T)
        
        if Dif > 0:
            S = Snew
            ES = ESnew
            if ES > ESmejor:
                Smejor = S
                ESmejor = ES
        else:
            if Dif / T > -700:  # Asegurarse de no desbordar
                probabilidad = math.exp(Dif / T)
            else:
                probabilidad = 0.0
            # Almacenamos la probabilidad de Boltzmann
            probabilidades.append(probabilidad)
            if probabilidad > random.random():
                #print(probabilidad)
                S = Snew
                ES = ESnew
        n += 1
    T = Alpha * T

peso_mejor, calorias_mejor = evaluar_solucion(Smejor)

if calorias_mejor==0:
    print("Ajusta los valores a tus restricciones o sigue intentando")
    print("No existe mochila que se ajuste a esos valores")
else:
    print("Mejor solución encontrada:")
    print("Mochila:", Smejor)
    print("Peso total:", peso_mejor)
    print("Calorías totales:", calorias_mejor)
    # Ahora, grafiquemos las métricas
    plt.figure(figsize=(12, 5))

    # Energía vs Iteraciones
    plt.subplot(1, 3, 1)
    plt.plot(energias)
    plt.title("Energía vs Iteraciones")
    plt.xlabel("Iteraciones")
    plt.ylabel("Energía (Calorías Totales)")

    # Temperatura vs Iteraciones
    plt.subplot(1, 3, 2)
    plt.plot(temperaturas)
    plt.title("Temperatura vs Iteraciones")
    plt.xlabel("Iteraciones")
    plt.ylabel("Temperatura")

    # Probabilidad de Boltzmann vs Iteraciones
    plt.subplot(1, 3, 3)
    plt.plot(probabilidades)
    plt.title("Probabilidad vs Iteraciones")
    plt.xlabel("Iteraciones")
    plt.ylabel("Probabilidad")

    plt.tight_layout()
    plt.show()
    #Graficae Energia, enfriamiento y probabilidad de bossman para ver correcto funcionamiento

