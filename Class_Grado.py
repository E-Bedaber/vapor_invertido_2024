from Class_Arma import *

class Grado:
    def __init__(self, grado: str, coleccion, stat):
        self.grado = grado
        self.coleccion = coleccion
        self.stat = stat
        self.armas = []

    def obtener_coleccion(self):
        return self.coleccion

    def obtener_armas(self):
        return self.armas

    def agregar_arma(self, arma):
        self.armas.append(arma)
        for i in range(self.cant_armas()):
            if (self.armas[i]).p_max() < (self.armas[self.cant_armas() - 1]).p_max():
                temp = self.armas[i]
                self.armas[i] = arma
                self.armas[self.cant_armas() - 1] = temp

    def cant_armas(self):
        return len(self.armas)

    def arma_Pmax(self):
        return self.armas[0]

    def arma_PSmax(self):
        return [self.armas[0], self.armas[0]]

    def arma_mas_barata(self): # agregar tamaño del rango para calcular precio bajo ?
        i = 0
        mas_barat = self.armas[self.cant_armas() - 1]

        while i < self.cant_armas():
            arma_actual = self.armas[self.cant_armas() - i - 1]
            rango_arma_actual = arma_actual.obtener_rango()
            rango_min = rango_arma_actual[0]
            if rango_min == 0:
                return arma_actual
            i += 1
        if i == self.cant_armas():
            return mas_barat

    def obtener_stat(self):
        return self.stat

    def obtener_grado(self):
        return self.grado

    def arma_S_mas_barata(self):
        return min(
            [arma for arma in self.armas if arma.gasto() == 0 and arma.stat],
            key=lambda arma: arma.p_S_max(),
            default=None,
        )

    def precio_prom(self):
        precios = sum([arma.p_max() for arma in self.armas])
        if precios == 0:
            return 0
        return precios / self.cant_armas()

    def precio_prom_S(self):
        return sum([arma.p_S_max() for arma in self.armas if arma.stat]) / len(
            [arma for arma in self.armas if arma.stat]
        )

