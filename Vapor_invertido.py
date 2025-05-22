#!/usr/bin/env python
# coding: utf-8

from imports import *

# buscar flote para que todas las armas tengan su flote lo mas bajo posible


def input_output_contrato( grado_sup_col, grado_sup_filler, cant_col: int, cant_filler: int):
    out_col = grado_sup_col.cant_armas()
    out_filler = grado_sup_filler.cant_armas()

    out_posibles = out_col * cant_col + out_filler * cant_filler
    prob_cada_coleccion = [(out_col * cant_col) / out_posibles, (out_filler * cant_filler) / out_posibles]
    return prob_cada_coleccion


def flote_prom_minimo_menor_gasto(grado):
    avrg_min = 1
    for arma in grado.obtener_armas():
        flt_min = arma.obtener_rango()[0]
        flt_max = arma.obtener_rango()[1]

        if flt_min == 0:
            avrg_temp = 0.06999 / flt_max
            if avrg_temp < avrg_min:
                avrg_min = avrg_temp
            continue

        gasto = flote_a_gasto(flt_min)
        rango = flt_max - flt_min

        match gasto:
            case 0:
                avrg_temp = (0.06999 - flt_min) / rango
            case 1:
                avrg_temp = (0.14999 - flt_min) / rango
            case 2:
                avrg_temp = (0.37999 - flt_min) / rango
            case 3:
                avrg_temp = (0.44999 - flt_min) / rango
            case 4:
                avrg_temp = (0.9999 - flt_min) / rango
        if avrg_temp < avrg_min:
            avrg_min = avrg_temp
    return avrg_min


# ESTE CODIGO ESTA DESORDENADO

def may_men(lista_contratos):

    #ordeno primera vez
    if len(lista_contratos) == 2:
        
        if lista_contratos[0].get_esperanza_perc() < lista_contratos[1].get_esperanza_perc():
            temp = lista_contratos[0]
            lista_contratos[0] = lista_contratos[1]
            lista_contratos[1] = temp
        return lista_contratos
    
    # ahora para cuando agrego contratos
    if len(lista_contratos) == 3:
        i = 0
        while i < 2:
            if lista_contratos[i].get_esperanza_perc() < lista_contratos[2].get_esperanza_perc():
                if i == 0:
                    lista_contratos.insert(0, lista_contratos[2])
                if i == 1:
                    lista_contratos.insert(1, lista_contratos[2])
                i += 1
            i += 1

        if len(lista_contratos) > 3:
            lista_contratos.pop()
        
        lista_contratos.pop()
        return lista_contratos

def muy_molesta(arma, grado):
    precios = arma.obtener_precios()
    if precios[grado] == 0 and grado == 4:
        return True
    if precios[grado] == 0 and precios[grado + 1] == 0:
        return True
    return False

def contratos_skin(lista_todo, skin_col): #Se puede usar poniendo un arma que queremos usar de relleno en skin_col
    # para ciertas skins de un e coleccion, encuentra el contrato que mejor funciona
    skin_col_sup = buscar(skin_col.obtener_coleccion(), grado_superior(skin_col.obtener_grado()))
    mejor_esp = -100
    contratos = []
    grado = skin_col.obtener_grado()
    i = 0
    y = 1
    for col in lista_todo:
        nomb = skin_col.obtener_nombre()
        if nomb == "AWP Duality":
            print("")

        grad = col.obtener_grados()
        pos = G_grado_a_int(grado)

        #para zafar de colecciones q no funcionan o no sirven
        if pos == 0 or grad[pos-1] == 0 or grad[pos] == 0:
            continue
        

        skin_rell = buscar(col.obtener_nombre(), grado).arma_mas_barata()

        if muy_molesta(skin_rell, pos):
            continue
        if demasiado_cara(skin_rell):
            continue

        skin_rell_sup = buscar_grado_sup(skin_rell)

        armas_contrato = [skin_col, skin_rell, skin_col_sup, skin_rell_sup]
        contrato = mejor_contrato( armas_contrato )  # devuelve la manera mas barata de conseguir lo deseado

        if contrato == 0:
            continue

        ev_percentaje = contrato.get_esperanza_perc() 
        if ev_percentaje > 1.15 :
            i += 1
            # guardamos los mejores 2
            if i < 3:
                contratos.append(contrato)
                if i == 2:
                    may_men(contratos)
                continue
            contratos.append(contrato)
            temp = contratos
            contratos = may_men(temp)
            mejor_esp = 100


    if mejor_esp == -100:
        nombre_arma = skin_col.obtener_nombre()
        print("no hay contrato para: ", nombre_arma)
        return 0

    return contratos


def parche_gastos(lista_gasto, cant_c, cant_f): # se usa par ordenar los gastos de las armas
    parche = [] 
    i = 0
    col = 0
    fill = 0
    
    while i < 10:
        if col < cant_c:
            parche.append(lista_gasto[0])
            col += 1
            i += 1
            continue
        if fill < cant_f:
            parche.append(lista_gasto[1])
            fill += 1
            i += 1
            continue

    return parche

def mejor_contrato(armas_contrato):  # esta funcion creara una instancia de contrato
    skin_col = armas_contrato[0]
    skin_rell = armas_contrato[1]
    skin_col_sup = armas_contrato[2]
    skin_rell_sup = armas_contrato[3]
    esperanza = -100
    i = 1
    while i < 10: # arma_col, arma_fill, cant_sup, cant_fill
        salida_contrato = input_output_contrato(skin_col_sup, skin_rell_sup, 10 - i, i)
        gasto_barato_2 = lowest_cost(skin_col, skin_rell, 10 - i, i)  # Devuelve una lista de los gastos
        gasto_barato = parche_gastos(gasto_barato_2.x, 10 - i, i)
        costo = costo_con(skin_col, skin_rell, 10 - i, i, gasto_barato)
        ingreso = ingreso_con( salida_contrato, skin_col_sup, skin_rell_sup, 10 - i, i, gasto_barato)
        esperanza_i = ingreso - costo

        if esperanza_i > esperanza:
            esperanza = esperanza_i
            skins = []
            x = 0

            while x < 10:
                if x < 10 - i:
                    skins.append(skin_col)
                    x += 1
                    continue
                skins.append(skin_rell)
                x += 1
            
            contrato = Contrato(skins, gasto_barato, esperanza_i, ingreso, costo)
        i += 1

    if esperanza == -100:
        return 0
    return contrato


def prom(lista):
    sum = 0
    for x in lista:
        sum = sum + x

    return sum/10

def ingreso_con(output_prob, col_sup, col_filler, cant_sup, cant_filler, lista_flotes):  # comprobar
    # Voy a hacerla para q tome el valor de fn, asi no dependo tanto de la suerte de un flote un poco menor

    promedio = prom(lista_flotes)
    armas_col = col_sup.obtener_armas()
    armas_filler = col_filler.obtener_armas()
    col_prob = output_prob[0] / len(armas_col)
    filler_prob = output_prob[1] / len(armas_filler)
    ingreso = 0
    for arma in armas_col:
        grados = arma.obtener_rango()
        flote = promedio * (grados[1] - grados[0]) + grados[0]
        precio = flote_a_gasto(flote)
        ingreso = ingreso + arma.obtener_precios()[precio] * col_prob
        #ingreso = ingreso + arma.p_max() * col_prob

    for arma in armas_filler:
        grados = arma.obtener_rango()
        flote = promedio * (grados[1] - grados[0]) + grados[0]
        precio = flote_a_gasto(flote)
        ingreso = ingreso + arma.obtener_precios()[precio] * filler_prob
        #ingreso = ingreso + arma.p_max() * filler_prob
    return ingreso


def costo_con(arma_col, arma_fill, cant_col, cant_filler, flotes):  # comprobar
    # no estaba recorriendo armas_sup ni fill
    fill = 0
    col = 0
    costo = 0
    for flote in flotes:
        if col < cant_col:
            costo = costo + rat_price_est(arma_col, flote)
            col = col + 1
            continue
        if fill < cant_filler:
            costo = costo + rat_price_est(arma_fill, flote)
            fill = fill + 1
    return costo


def lowest_cost(arma_col, arma_fill, cant_sup, cant_fill):
    sup_col = buscar_grado_sup(arma_col)
    flote_buscado = flote_prom_minimo_menor_gasto(sup_col)

    xy_col= x_y(arma_col)
    xy_fill = x_y(arma_fill)

    parameters_col = ajuste_racional(xy_col)
    parameters_fill = ajuste_racional(xy_fill)

    # Definir las funciones f1, f2
    def f1(x):
        a = parameters_col[0]
        b = parameters_col[1]
        c = parameters_col[2]
        d = parameters_col[3]
        return (x * a + b)/(c * x + d)

    def f2(x):
        af = parameters_fill[0]
        bf = parameters_fill[1]
        cf = parameters_fill[2]
        df = parameters_fill[3]
        return (x * af + bf)/(cf * x + df)

    # Función objetivo
    def objective(x):
        return cant_sup * f1(x[0]) + cant_fill * f2(x[1])

    # Definimos los límites para x1 y x2
    lrc = arma_col.obtener_rango() #Limite Rangos Coleccion
    lrf = arma_fill.obtener_rango() #Limite Rangos Filler
    bound = [(lrc[0], lrc[1]), (lrf[0], lrf[1])]

    # Restricciónes
    def constraint1(x):
        return objective(x) - 0

    def constraint2(x):
        y = flote_buscado  # define el valor de y
        
        return 10 * y - (cant_sup * x0[0] + cant_fill * x0[1])
    
    constr = [{'type': 'ineq', 'fun': constraint1},
                {'type': 'eq', 'fun': constraint2}]

    # Inicializacion
    x0 = np.array([flote_buscado, flote_buscado])  # punto inicial #el 0.5 capaz cambiar por flote_buscado

    # Resolución del problema
    result = minimize(objective, x0, bounds = bound, constraints = constr) # Usa minimos cuadrados para minimizar

    # Mostramos el resultado
    # print("Resultado de la optimización:")
    # print("x1:", result.x[0])
    # print("x2:", result.x[1])
    # print("Costo mínimo:", result.fun)
    return result

def demasiado_cara(arma):
    precios = arma.obtener_precios()
    for precio in precios:
        if precio != 0:
            return False
        
    return True

def contratos_primigenios():
    with open("colecciones.pkl", "rb") as file:
        all = pickle.load(file)

    cont= []
    i = 1
    for col in all:
        nom = col.obtener_nombre()
        trades = col.skins_trade()
        if trades == 0:
            continue

        for trade in trades:
            arma = trade[1]
            # Si es demasiado cara los contratos se hacen mal, porque el precio es 0
            if demasiado_cara(arma):
                continue

            contra = contratos_skin(all, arma)
            if contra == 0:
                print("Progreso: ",round((i / 43)* 100),"%")
                i += 1
                continue

            for contra2 in contra:
                cont = inst_sort(contra2, cont)

            print("Progreso: ",(i / 43)* 100,"%")
            i += 1
    return cont
            

def inst_sort(contrato, lista):
    
    if len(lista) == 0:
        lista.append(contrato)
        return lista

    perc_esp = contrato.get_esperanza_perc()
    i = 0
    while i < len(lista):
        if perc_esp > lista[i].get_esperanza_perc():
            lista.insert(i, contrato)
            return lista
        i += 1
    
    lista.append(contrato)
    return lista
