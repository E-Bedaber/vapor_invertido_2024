import numpy as np
from scipy.optimize import curve_fit
# from imports import Arma


def flote_a_gasto(flote):
    # devuelve la posicion en la lista de precios que corresponde al flote
    if 0 <= flote < 0.07:
        return 0
    if 0.07 <= flote < 0.15:
        return 1
    if 0.15 <= flote < 0.38:
        return 2
    if 0.38 <= flote < 0.45:
        return 3
    if 0.45 <= flote < 1:
        return 4


def porcentaje_de_flote(arma, flote):
    # Nos da un parametro que sirve para ver que tan cara va a ser el arma dependiendo del flote que se necesite

    # estas cosas que hago con los limites son para las armas que tienen rangos de desgaste que no son comunes,
    # pero tambien funciona para los comunes
    rango = arma.obtener_rango()
    gasto = flote_a_gasto(flote)
    if gasto == 0 or arma.obtener_precios()[gasto - 1] == 0:  # Puede estar mal esto (NO SE EN Q MIERDA PENSABA, NO ENCUENTRO LA LOGICA LOL)
        lim = 0.07
        limenor = 0
        if rango[1] < lim:
            lim = rango[1]
        if rango[0] > 0:
            limenor = rango[0]
        porc = (flote - limenor) / lim
        return 1 - porc

    flote_int = flote_a_gasto(flote)
    cero = 0
    match flote_int:
        case 1:
            lim = 0.08
            if rango[1] < lim:
                lim = rango[1]
            if rango[0] > 0:
                cero = rango[0] - 0.07
            porc = (flote - cero - 0.07) / lim

        case 2:
            lim = 0.23
            if rango[1] < lim:
                lim = rango[1]
            if rango[0] > 0.15:
                cero = rango[0] - 0.15
            porc = (flote - cero - 0.15) / lim

        case 3:
            lim = 0.07
            if rango[1] < lim:
                lim = rango[1]
            if rango[0] > 0:
                cero = rango[0] - 0.38
            porc = (flote - cero - 0.38) / lim

        case 4:
            lim = 0.65
            if rango[1] < lim:
                lim = rango[1]
            if rango[0] > 0:
                cero = rango[0] - 0.45
            porc = (flote - cero - 0.45) / lim

    return 1 - porc


def seg_lin_price_est(arma, flote):
    rango = arma.obtener_rango()
    if flote < rango[0] or flote > rango[1]:
        return False
    gasto = flote_a_gasto(flote)  # devuelve la posicion en la lista de precios que corresponde al flote

    # %z es que tan cerca esta el flote requerido de ser del siguiente flote
    porcentaje_z = porcentaje_de_flote(arma, flote)
    Pgasto = arma.obtener_precios()[gasto]

    if Pgasto == 0 and gasto != 4: #caso flote raro y poca liquidez
        Pgasto = arma.obtener_precios()[gasto + 1]*8
    # las armas que cumplen esto no suelen tener grandes diferencias entre precios
    min = arma.obtener_rango()[0]
    max = arma.obtener_rango()[1]
    if (max - min) < 0.09:
        precio = Pgasto + (Pgasto * 0.1) * porcentaje_z
        return precio

    # Las armas que cumplen esto su precio suele duplicar
    if gasto == 0 or arma.obtener_precios()[gasto - 1] == 0:
        precio = Pgasto + (Pgasto * 1.5 ) * porcentaje_z #estaba * por 1.5 pgasto
        return precio

    # Precio = Pgasto + (Pgasto_men - Pgasto). %z

    Pgasto_men_gasto = arma.obtener_precios()[gasto - 1]
    dif_precios = Pgasto_men_gasto - Pgasto

    if porcentaje_z >= 0.8:
        dif_precios = dif_precios * 1.5
        # para evitar que use flotes imposibles de encontrar

    precio = Pgasto + dif_precios * porcentaje_z

    return precio



def ajuste_recta(x_y):  # x_y es una lista o tupla de listas, primero va x y luego y
    # Calcula los coeficientes de la recta (pendiente y ordenada al origen) utilizando mínimos cuadrados
    pendiente, ordenada_al_origen = np.polyfit(x_y[0], x_y[1], 1)
    PO = [pendiente, ordenada_al_origen]
    return PO


def x_y(arma):
    # Crea una serie de puntos que estiman el valor de un arma
    x_list = []
    y_list = []

    rango_x = arma.obtener_rango()
    incremento = (rango_x[1] - rango_x[0]) / 10
    x = rango_x[0]
    while x <= rango_x[1]:
        x_list.append(x)
        y = seg_lin_price_est(arma, x)
        y_list.append(y)
        x = x + incremento
    return [x_list, y_list]


def ajuste_racional(xy): #xy is a tuple of lists
    def rational_func(x, a, b, c, d):
        return (a * x + b) / (c * x + d)
    
    x_data = xy[0]
    y_data = xy[1]

    # Adjust rational function to data
    params, params_covariance = curve_fit(rational_func, x_data, y_data, p0=[1, 1, 1, 1], maxfev=5000)

# #esto es chiche
#     # Imprimir los parámetros ajustados
#     print("Parámetros ajustados:")
#     print("a =", params[0])
#     print("b =", params[1])
#     print("c =", params[2])
#     print("d =", params[3])

#     # Crear una línea suave para la función ajustada
#     x_fit = np.linspace(min(x_data), max(x_data), 100)
#     y_fit = rational_func(x_fit, *params)

#     # Graficar los datos originales y la función ajustada
#     plt.scatter(x_data, y_data, label='Datos')
#     plt.plot(x_fit, y_fit, label='Función racional ajustada', color='red')

#     plt.title('Ajuste de función racional')
#     plt.xlabel('x')
#     plt.ylabel('y')
#     plt.legend()
#     plt.show()

#     #fin chiche

    return params


def rat_price_est(arma, flote):
    parameters = arma.get_par()
    a = parameters[0]
    b = parameters[1]

    if a + b == 0:
        arma.set_par()
        parameters = arma.get_par()
        a = parameters[0]
        b = parameters[1]
    
    c = parameters[2]
    d = parameters[3]


    return (a * flote + b)/(c * flote + d)

def weapon_to_par(arma):
    xy = x_y(arma)
    return ajuste_racional(xy)