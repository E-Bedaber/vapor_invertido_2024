import pickle

def buscar(nombre, tipo):  # case sensitive.
    # nombre es el nombre del arma o coleccion
    # tipo es 0 si buscas arma, 1 si buscas coleccion
    # si buscas el grado de una coleccion, nombre es el nombre de la coleccion, y tipo es el str del grado
    # EJ: "Zeus x27 | Olympus" escribir como "Zeus x27 Olympus"

    with open("colecciones.pkl", "rb") as file:
        all = pickle.load(file)

    match tipo:
        case 0:
            for col in all:
                grados = col.obtener_grados()
                for grado in grados:
                    if grado == 0:
                        continue
                    armas = grado.obtener_armas()
                    for arma in armas:
                        if arma.obtener_nombre() == nombre:
                            return arma 
                        

        case 1:
            for col in all:
                if col.obtener_nombre() == nombre:
                    return col
                
    for col in all:
            if col.obtener_nombre() == nombre:
                grados = col.obtener_grados()
                for grado in grados:
                    if grado != 0:
                        if grado.obtener_grado() == tipo:
                            return grado

                
    print("Escribiste mal")
    print("Fijate de estar poniendo bien las mayusculas y siguiendo las reglas de busqueda")


def grado_superior(grado:str):

    match grado:
        case "Classified":
            return "Covert"
        case "Restricted":
            return "Classified"
        case "Mil-Spec":
            return "Restricted"
        case "Industrial":
            return "Mil-Spec"
        case "Consumer":
            return "Industrial"
        
    print("estan pasando mal el grado")

def buscar_grado_sup(arma):
    coleccion = arma.obtener_coleccion()
    grado = arma.obtener_grado()
    grado_sup = grado_superior(grado)

    return buscar(coleccion, grado_sup)