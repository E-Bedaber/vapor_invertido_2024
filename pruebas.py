from Vapor_invertido import *
import pickle



# all_ = lista_de_todas_las_colecciones_obj()


# with open("colecciones.pkl", "wb") as file:
#     pickle.dump(all_, file)


with open("colecciones.pkl", "rb") as file:
    all = pickle.load(file)


conts = contratos_primigenios()

with open("contratos.pkl", "wb") as file:
    pickle.dump(conts, file)

with open("contratos.pkl", "rb") as file:
    contratitos = pickle.load(file)

for contrato in contratitos:
    armas = contrato.get_armas()
    flotes = contrato.get_flotes()
    print("")
    print("Este contrato tiene una esperanza percentil de: ", contrato.get_esperanza_perc())
    print("Ingreso", contrato.get_income(),"Costo: ", contrato.get_cost())
    i = 0
    print("Y compuesto por:")
    nomain = armas[i].obtener_nombre()

    while i < 10:
        nombre = armas[i].obtener_nombre()
        if nombre != nomain:
            print(i ," ", nomain," ", 10-i, nombre)
            i = 10
        i += 1

    if i == 10:
        print(nomain)
    y = 0
    while y < 10:
        print("Flotes: ", flotes[y])
        y += 1


# glock = buscar("Glock-18 High Beam", 0)

# c = contratos_skin(all, glock)

# p250 = buscar("P250 Splash", 0)
# precios = p250.obtener_precios()
# paramatros = p250.set_par()
# paramatros = p250.get_par()
# for precio in precios:
#     print(precio)

# for par in paramatros:
#     print (par)

# print(rat_price_est(p250, 0.061))


# acid = buscar("SSG 08 Acid Fade", 0)

# c = contratos_skin(all, acid)

# c1 = c[0] 

# armas = c1.get_armas()
# flotes = c1.get_flotes()
# print("")
# print("Este contrato tiene una esperanza percentil de: ", c1.get_esperanza_perc())
# print("Ingreso", c1.get_income(),"Costo: ", c1.get_cost())
# i = 0
# print("Y compuesto por:")
# nomain = armas[i].obtener_nombre()

# while i < 10:
#     nombre = armas[i].obtener_nombre()
#     if nombre != nomain:
#         print(i ," ", nomain," ", 10-i, nombre)
#         i = 10
#     i += 1

# if i == 10:
#     print(nomain)
# y = 0
# while y < 10:
#     print("Flotes: ", flotes[y])
#     y += 1



# c1 = c[1] 

# armas = c1.get_armas()
# flotes = c1.get_flotes()
# print("")
# print("Este contrato tiene una esperanza percentil de: ", c1.get_esperanza_perc())
# print("Ingreso", c1.get_income(),"Costo: ", c1.get_cost())
# i = 0
# print("Y compuesto por:")
# nomain = armas[i].obtener_nombre()

# while i < 10:
#     nombre = armas[i].obtener_nombre()
#     if nombre != nomain:
#         print(i ," ", nomain," ", 10-i, nombre)
#         i = 10
#     i += 1

# if i == 10:
#     print(nomain)
# y = 0
# while y < 10:
#     print("Flotes: ", flotes[y])
#     y += 1