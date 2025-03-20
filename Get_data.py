import requests
from bs4 import BeautifulSoup
from Class_Coleccion import *

def C_nombre_coleccion(Soup_coleccion):
    n = Soup_coleccion.find("div", class_="inline-middle collapsed-top-margin")
    if n is None:
        return "NO"
    name = n.find("h1")
    return name.text


def C_armas_de_coleccion(Soup_coleccion):
    armas = Soup_coleccion.find_all(
        "div", class_="col-lg-4 col-md-6 col-widen text-center"
    )
    return armas


def C_nombre_arma(elemento):
    nombre = elemento.find(
        "img", class_="img-responsive center-block margin-top-sm margin-bot-sm"
    )
    return nombre.attrs["alt"]


def C_grado_arma(elemento):
    # elemento es un elemento del resultado de C_armas_de_coleccion()
    a = elemento.find("a", class_="nounderline")
    if a == None:
        return "cuchi"
    b = a.find("p", class_="nomargin")
    grado = (b.text.strip()).split(" ")
    return grado[0]


def C_link_arma(elemento):
    # elemento es un elemento del resultado de C_armas_de_coleccion()
    div_price = elemento.find("div", class_="price")
    if div_price:
        primer_enlace = div_price.find("a")
        if primer_enlace:
            href_value = primer_enlace["href"]
            return href_value
        else:
            return False
    else:
        return False


def C_es_caja(Soup_coleccion):
    nombre = C_nombre_coleccion(Soup_coleccion)
    palabras = nombre.split(" ")
    for palabra in palabras:
        if palabra == "Case":
            return True
    return False


# Ahora para la pagina de cada arma:

# Con esto consegimos toda la info que nos importa de la pag


def A_precios(Soup_arma):
    # Devuelve una lista con todos los precios
    div_prices = Soup_arma.find( "div", {"role": "tabpanel", "class": "tab-pane active", "id": "prices"} )
    p_grad = div_prices.find_all("div", class_="btn-group-sm btn-group-justified")

    precios_lista = []

    # Iterar a través de los elementos del ResultSet p_grad
    for elemento in p_grad:
        precios_lista.append(elemento)

    return precios_lista


def A_precio_es_stat(elemento):
    # elemento es un elemento de la lista que nos da A_precios
    if elemento.find("span", class_="pull-left price-details-st") == None:
        return False
    else:
        return True


def A_precio_es_souv(elemento):
    # elemento es un elemento de la lista que nos da A_precios
    if elemento.find("span", class_="pull-left price-details-souv") == None:
        return False
    else:
        return True


def A_precio(elemento):
    # elemento es un elemento de la lista que nos da A_precios
    span_pull_right = elemento.find("span", class_="pull-right")
    if span_pull_right:
        contenido_span = (
            span_pull_right.text.strip()
        )  # Obtenemos el contenido del elemento y eliminamos espacios en blanco
        valor_numerico_str = contenido_span.split(" ")[1]

        # Eliminamos la coma (,) y convertimos el valor a un número float
        valor_numerico_str = valor_numerico_str.split(".")
        valor_numerico_str = "".join(valor_numerico_str).replace(",", ".")
        if valor_numerico_str == "Possible" or valor_numerico_str == "Recent":
            return 0
        valor_numerico_float = float(valor_numerico_str)
        return valor_numerico_float
    else:
        return 0


def A_calidad(elemento):
    # elemento es un elemento de la lista que nos da A_precios
    span_pull_left = elemento.find_all("span", class_="pull-left")
    if len(span_pull_left) > 1:
        return span_pull_left[1].text
    else:
        return span_pull_left[0].text


def A_calidad_a_int(calidad):
    match calidad:
        case "Factory New":
            return 0
        case "Minimal Wear":
            return 1
        case "Field-Tested":
            return 2
        case "Well-Worn":
            return 3
        case "Battle-Scarred":
            return 4


def A_rango(soup_html_arma):
    miin = soup_html_arma.find("div", class_="marker-wrapper wear-min-value")
    miin = miin.find("div", title='Minimum Wear ("Best")').text.strip()
    maax = soup_html_arma.find("div", class_="marker-wrapper wear-max-value")
    maax = maax.find("div", title='Maximum Wear ("Worst")').text.strip()
    return [float(miin), float(maax)]


def asignar_precios_y_rango(link_html_arma, arma):
    global __cambio__
    # hago soup
    response = requests.get(link_html_arma)
    response = response.content
    Soup_html_arma = BeautifulSoup(response, "html.parser")

    # asignacion rango
    rango = A_rango(Soup_html_arma)
    arma.set_rango_flote(rango)

    # asignacion precios
    precios_calidades = A_precios(Soup_html_arma)
    for elemento in precios_calidades:
        # esto es una cagada
        if A_precio_es_souv(elemento):
            continue

        stat = A_precio_es_stat(elemento)
        valor_arg = A_precio(elemento)
        valor_usd = valor_arg/__cambio__
        calidad = A_calidad_a_int(A_calidad(elemento))

        arma.agregar_precio(stat, valor_usd, calidad)

def usd_arg():
    url = "https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=ARS"
    response = requests.get(url)
    response = response.content
    Soup = BeautifulSoup(response, "html.parser")

    p_tag = Soup.find('p', class_="sc-295edd9f-1 jqMUXt")

    main_value = p_tag.contents[0].strip()
    faded_value = p_tag.find('span', class_='faded-digits').get_text(strip=True)

    full_value = main_value + faded_value
    float_value = float(full_value)
    return float_value


def guardar_armas_en_lista(Soup_coleccion):

    nombre_coleccion = C_nombre_coleccion(Soup_coleccion)
    armas_en_pag_coleccion = C_armas_de_coleccion(Soup_coleccion)
    lista_armas_raw = []
    grados = [
        "Covert",
        "Classified",
        "Restricted",
        "Mil-Spec",
        "Industrial",
        "Consumer",
    ]

    for arma_en_pag_coleccion in armas_en_pag_coleccion:
        link_arma = C_link_arma(arma_en_pag_coleccion)
        grado_arma = C_grado_arma(arma_en_pag_coleccion)

        if grado_arma in grados:
            nombre_arma = C_nombre_arma(arma_en_pag_coleccion)
            arma_ = Arma(nombre_arma, grado_arma, nombre_coleccion)
            lista_armas_raw.append(arma_)
            asignar_precios_y_rango(
                link_arma, lista_armas_raw[len(lista_armas_raw) - 1]
            )

    return lista_armas_raw


def G_grado_a_int(grado):
    match grado:
        case "Covert":
            return 0
        case "Classified":
            return 1
        case "Restricted":
            return 2
        case "Mil-Spec":
            return 3
        case "Industrial":
            return 4
        case "Consumer":
            return 5


def G_grados_coleccion(lista_armas_raw):
    grados = set()
    for arma in lista_armas_raw:
        grados.add(arma.obtener_grado())
    grados_list = list(grados)
    grados_ordenados = [0, 0, 0, 0, 0, 0]
    for grado in grados_list:
        grados_ordenados[G_grado_a_int(grado)] = grado

    return grados_ordenados


def G_crear_grados(Soup_coleccion):
    stat = C_es_caja(Soup_coleccion)
    nombre_coleccion = C_nombre_coleccion(Soup_coleccion)
    if nombre_coleccion is None:
        return "NO"
    lista_armas_raw = guardar_armas_en_lista(Soup_coleccion)
    grados_ordenados = G_grados_coleccion(lista_armas_raw)
    grados_creados = []
    # creo todos los grados
    for grado in grados_ordenados:
        if grado == 0:
            continue
        grados_creados.append(Grado(grado, nombre_coleccion, stat))
    # los completo
    for grado_ in grados_creados:
        grado = grado_.obtener_grado()

        for arma in lista_armas_raw:
            precios = arma.obtener_precios()
            i = 0
            if arma.obtener_grado() == grado:
                grado_.agregar_arma(arma)
    return grados_creados


def C_crear_coleccion(lista_colecciones, lista_grados):
    # Usamos esta funcion en un ciclo, cada llamada a esta funcion crea una coleccion

    # lista_colecciones tendra todas las colecciones
    # lista_grados es obtenida de la funcion:  G_crear_grados()

    colec = lista_grados[0].obtener_coleccion()
    stat = lista_grados[0].obtener_stat()
    lista_colecciones.append(Coleccion(colec, stat))

    if len(lista_colecciones) == 0:
        pos = len(lista_colecciones)
    else:
        pos = len(lista_colecciones) - 1

    for grado in lista_grados:
        grado_str = grado.obtener_grado()  # nombre grado
        grado_int = G_grado_a_int(
            grado_str
        )  # valor en int grado, covert:0 , classified:1 ...
        # print(grado_str)
        lista_colecciones[pos].agregar_grado(grado, grado_int)
    return lista_colecciones


def links_todas_colecciones():
    # ESTE CODIGO SEGURO ESTE MAL SI AGREGAN UNA NUEVA COLECCION O CAJA
    
    url = "https://csgostash.com/setcurrency/USD"
    #url = "https://csgostash.com/"
    response = requests.get(url)
    response = response.content

    Soup = BeautifulSoup(response, "html.parser")

    colecciones = Soup.find_all("ul", class_="dropdown-menu navbar-dropdown-small")
    colecciones.pop()

    ccl = []
    for col in colecciones:
        links = col.find_all("a")
        for link in links:
            ccl.append(link["href"])
    return ccl


def lista_de_todas_las_colecciones_obj():
    global __cambio__
    __cambio__ = usd_arg()
    links = links_todas_colecciones()
    colecciones = []
    i = 1
    for link in links:
        
        # if i == 5:
        #     return colecciones

        print(i)
        response = requests.get(link)
        response = response.content
        sopa = BeautifulSoup(response, "html.parser")
        grados_col = G_crear_grados(sopa)
        if len(grados_col) == 0:
            print("zafamo")
            continue
        C_crear_coleccion(colecciones, grados_col)
        # colecciones.append(C_crear_coleccion(colecciones, grados_col))
        i += 1
    return colecciones