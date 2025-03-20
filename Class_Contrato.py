

class Contrato:
    def __init__(self, list_armas, list_flotes, esperanza, income, cost):
        self.components = list_armas
        self.floats = list_flotes
        self.cost = cost
        self.income = income
        self.esperanza = esperanza # income neta en pesos
        self.esperazna_perc = 0  # income neta en porcentaje
        self.output
        self.prob_gan

    def get_comp(self):
        return self.components
    
    def get_floats(self):
        return self.floats

    def get_cost(self):
        return self.cost

    def get_income(self):
        return self.income

    def get_esperanza(self):
        return self.esperanza

    def get_esperanza_perc(self):
        return  self.income / self.cost
    
    def get_armas(self):
        return self.components
    
    def get_flotes(self):
        return self.floats

    def output(self): #es chiche para mas adelante
        return

    def get_output(self): #es chiche para mas adelante
        return self.output

    def prob_gan(self): #es chiche para mas adelante
        return

    def get_prob_ganar(self): #es chiche para mas adelante
        return self.prob_gan

    def actualizar(self):
        # actualizamos los valores de las armas y luego los valoores del contrato
        return
    
    