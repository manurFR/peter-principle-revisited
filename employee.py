from random import normalvariate


class Employee:
    def __init__(self):
        self.age = round(normalvariate(25, 5))
        self.competence = 0.0
        self.init_competence()

    def init_competence(self):
        self.competence = normalvariate(7.0, 2.0)

    def modify_competence(self, increment):
        self.competence += increment
        self.competence = min(self.competence, 10.0)
        self.competence = max(self.competence, 0.0)
