from scipy.linalg import lu
import numpy as np

def crear_sistema_ecuaciones(n):
    """
    Crea un sistema de ecuaciones para un tablero de Lights Out de tamaño n x n.
    Retorna una matriz de coeficientes y un vector de términos constantes.
    """
    # Total de luces en el tablero
    total_luces = n * n
    # Inicializar la matriz de coeficientes y el vector de términos constantes
    matriz_coeficientes = np.zeros((total_luces, total_luces), dtype=int)
    vector_constantes = np.zeros(total_luces, dtype=int)

    # Función para agregar coeficientes a la matriz
    def agregar_coeficientes(fila, columna):
        index = fila * n + columna
        matriz_coeficientes[index, index] = 1  # Luz en la posición actual
        if fila > 0:  # Arriba
            matriz_coeficientes[index, index - n] = 1
        if fila < n - 1:  # Abajo
            matriz_coeficientes[index, index + n] = 1
        if columna > 0:  # Izquierda
            matriz_coeficientes[index, index - 1] = 1
        if columna < n - 1:  # Derecha
            matriz_coeficientes[index, index + 1] = 1

    # Llenar la matriz de coeficientes
    for fila in range(n):
        for columna in range(n):
            agregar_coeficientes(fila, columna)

    return matriz_coeficientes, vector_constantes

def resolver_lights_out(estado_inicial):
    """
    Resuelve el juego Lights Out para un estado inicial dado.
    estado_inicial: Matriz n x n representando el estado inicial del juego.
    Retorna un vector de solución.
    """
    n = len(estado_inicial)
    matriz_coeficientes, vector_constantes = crear_sistema_ecuaciones(n)

    # Actualizar el vector de términos constantes según el estado inicial
    for i in range(n**2):
        fila, columna = divmod(i, n)
        vector_constantes[i] = estado_inicial[fila][columna]

    # Resolver el sistema de ecuaciones
    # Como estamos trabajando con aritmética modular (suma binaria), usamos eliminación de Gauss
    for i in range(n**2):
        # Normalizar la fila actual
        if matriz_coeficientes[i, i] == 0:
            for j in range(i + 1, n**2):
                if matriz_coeficientes[j, i] == 1:
                    matriz_coeficientes[[i, j]] = matriz_coeficientes[[j, i]]  # Intercambiar filas
                    vector_constantes[i], vector_constantes[j] = vector_constantes[j], vector_constantes[i]
                    break

        # Eliminación de Gauss
        for j in range(i + 1, n**2):
            if matriz_coeficientes[j, i] == 1:
                matriz_coeficientes[j] = (matriz_coeficientes[j] + matriz_coeficientes[i]) % 2
                vector_constantes[j] = (vector_constantes[j] + vector_constantes[i]) % 2

    # Solución mediante sustitución hacia atrás
    solucion = np.zeros(n**2, dtype=int)
    for i in range(n**2 - 1, -1, -1):
        solucion[i] = (vector_constantes[i] - np.dot(matriz_coeficientes[i, i+1:], solucion[i+1:])) % 2

    return solucion

# Prueba de la función con el estado inicial proporcionado anteriormente
estado_inicial = [[1, 0, 1], [1, 1, 1], [0, 1, 1]]
solucion = resolver_lights_out(estado_inicial)
print(solucion)
