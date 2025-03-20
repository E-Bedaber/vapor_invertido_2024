from Price_est import weapon_to_par

class Arma:
    def __init__(self, nombre, grado: str, coleccion: str):
        self.nombre = nombre
        self.grado = grado
        self.coleccion = coleccion
        self.rango_flote = [0, 1]
        self.parameters = [0, 0, 0, 0]
        # deberia agregar si tiene stat o no, simplificaria codigo creo
        self.precios = [0, 0, 0, 0, 0]
        self.precios_S = [0, 0, 0, 0, 0]

    def set_par(self):
        par = weapon_to_par(self)
        par_o = self.parameters
        par_o[0] =  par[0]
        par_o[1] = par[1]
        par_o[2] = par[2]
        par_o[3] = par[3]
        return 

    def get_par(self):
        return self.parameters

    def agregar_precio(self, stat, precio, calidad):
        if stat:
            self.precios_S[calidad] = precio
        else:
            self.precios[calidad] = precio
            

    def obtener_precios(self):
        return self.precios

    def obtener_precios_S(self):
        return self.precios_S

    def obtener_grado(self):
        return self.grado

    def obtener_coleccion(self):
        return self.coleccion

    def obtener_nombre(self):
        return self.nombre

    def obtener_rango(self):
        return self.rango_flote

    def set_rango_flote(self, rango):
        self.rango_flote = rango

    def set_stat(self, existe):
        self.stat = existe

    def gasto(self):
        return self.rango_flote

    def p_max(self):
        precios = self.obtener_precios()
        for precio in precios:
            if precio != 0:
                return precio
        return 0

    def p_S_max(self):
        return max(self.precios_S)
