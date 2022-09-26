import operator

def hay_incompatible(prenda, lavado_actual, incompatibles):
    for k in lavado_actual:
        # Si la prenda del lavado actual esta en la lista de incompatibles de la prenda comparacion y viceversa, hay incompatibilidad
        if k in incompatibles[prenda] or prenda in incompatibles[k]:
            return True
    return False

def crear_lavado(tiempos_lavado, lista_incompatibles):
    lavados = {}

    i=1
    while(len(tiempos_lavado) != 0):
        lavados[i] = [tiempos_lavado[0]]
        tiempos_lavado.pop(0)
    
        for prenda in tiempos_lavado:
            if not hay_incompatible(prenda, lavados[i], lista_incompatibles):
                lavados[i].append(prenda)
                tiempos_lavado.remove(prenda)

        i += 1

    return lavados

def escribir_solucion(archivo, lavados):
    lineas = []

    for key, value in lavados.items():
        for i in value:
            lineas.append(i + " " + str(key) + "\n")
    archivo.writelines((lineas))

def ordenar_tiempos_lavado(tiempos):
    tiempos_ordenados = sorted(tiempos.items(), key = operator.itemgetter(1), reverse=True)
    prendas_ord_segun_tiempo = []
    for t in tiempos_ordenados:
        prendas_ord_segun_tiempo.append(t[0])
    return prendas_ord_segun_tiempo

def eliminar_repetidos(dict):
    for elem in dict:
        dict[elem] = list(dict.fromkeys(dict[elem]))

infoEnunciado = open('segundo_problema.txt', 'r')
solucion = open('solucion.txt', 'w')

# Declaro las variables que voy a necesitar, uso Sets que contienen listas adentro
cant_prendas = 0
incompatibles = {}
t_lavado = {}

for linea in infoEnunciado.readlines():
    linea = linea[:-1].split(' ')

    if linea[0] == 'c':
        continue

    elif linea[0] == 'p':
        cant_prendas = linea[2]

    elif linea[0] == 'e':
        # Veo si el primer incompatible ya fue registrado
        if linea[1] in incompatibles:
            # Como ya esta, en la lista de esa prenda agrego la nueva prenda con la que es incompatible
            incompatibles[linea[1]].append(linea[2])
        else:
            # Si no esta, en la ubic de la primer prenda creo una lista que contenga a su nueva prenda incompatible
            incompatibles[linea[1]] = [linea[2]]

        # Repito la misma logica pero con el segundo incompatible de la lista
        if linea[2] in incompatibles:
            incompatibles[linea[2]].append(linea[1])

        else:
            incompatibles[linea[2]] = [linea[1]]

    # Guardo el tiempo de lavado correspondiente a cada prenda
    elif linea[0] == 'n':
        t_lavado[linea[1]] = int(linea[2])

#Elimino los elementos repetidos en la lista de incompatibles de cada prenda
eliminar_repetidos(incompatibles)

#Ordeno los tiempos de lavado
t_lavado_ordenado = ordenar_tiempos_lavado(t_lavado)

# Armo los lavados
lavados_final = crear_lavado(t_lavado_ordenado, incompatibles)
eliminar_repetidos(lavados_final)

# Escribo los lavados en el doc solucion
escribir_solucion(solucion, lavados_final)


infoEnunciado.close()
solucion.close()