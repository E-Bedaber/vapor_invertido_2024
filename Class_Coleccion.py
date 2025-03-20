from Class_Grado import *


class Coleccion:
    def __init__(self, nombre, stat):
        self.nombre = nombre
        self.stat = stat
        self.grados = [0, 0, 0, 0, 0, 0]
        self.rango_grados = [0, 0]

    def obtener_nombre(self):
        return self.nombre

    def obtener_stat(self):
        return self.stat

    def obtener_grados(self):
        return self.grados

    def agregar_grado(self, grado, nivel):
        self.grados[nivel] = grado

    def obtener_rango_grados(self):
        inf = 0
        for i in range(6):
            if inf == 0 and (self.grados[i] != 0):
                inf = 1
                self.rango_grados[0] = i
            if inf == 1 and (self.grados[i] == 0):
                self.rango_grados[1] = i - 1
                return self.rango_grados
        self.rango_grados[1] = 5
        return self.rango_grados

    def skins_trade(self):  # Devuelve doble arreglar
        grado_arma = []
        for y in range(
            self.obtener_rango_grados()[0], self.obtener_rango_grados()[1] - 1):
            precio_promedio = self.grados[y].precio_prom()
            arma_mas_barata = self.grados[y + 1].arma_mas_barata()

            if precio_promedio > 8 * arma_mas_barata.p_max():
                grado_arma.append((self.grados[y + 1], arma_mas_barata))
        return grado_arma
