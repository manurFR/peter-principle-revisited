import random


# Hypothesis #########################################################################

class CommonSenseHypothesis:
    def compute_new_competence(self, employee):
        employee.modify_competence(random.uniform(-1.0, 1.0))


class PeterHypothesis:
    def compute_new_competence(self, employee):
        employee.init_competence()


# Strategies #########################################################################

def choose_by_competence(employees, competence):
    return random.choice([emp for emp in employees if emp is not None and emp.competence == competence])


class BestStrategy:
    def choose_from(self, employees):
        best_competence = max(emp.competence for emp in employees if emp is not None)
        return choose_by_competence(employees, best_competence)


class WorstStrategy:
    def choose_from(self, employees):
        worst_competence = min(emp.competence for emp in employees if emp is not None)
        return choose_by_competence(employees, worst_competence)


class RandomStrategy:
    def choose_from(self, employees):
        return random.choice([emp for emp in employees if emp is not None])
