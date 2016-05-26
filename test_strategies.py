import random
import unittest

from employee import Employee
from strategies import CommonSenseHypothesis, PeterHypothesis, BestStrategy, WorstStrategy, RandomStrategy


class TestHypothesis(unittest.TestCase):
    def test_common_sense_new_competence(self):
        emp = employee(competence=6.0)
        self.called = False

        def mock_uniform(a, b):
            self.called = True
            return 0.3

        save_uniform = random.uniform
        try:
            random.uniform = mock_uniform
            CommonSenseHypothesis().compute_new_competence(emp)
        finally:
            random.uniform = save_uniform

        self.assertTrue(self.called, msg='random.uniform() was not called')
        self.assertEquals(6.3, emp.competence)

    def test_peter_new_competence(self):
        emp = employee(competence=6.0)

        self.called = False

        def mock_init_competence():
            self.called = True

        save_init_competence = emp.init_competence
        try:
            emp.init_competence = mock_init_competence
            PeterHypothesis().compute_new_competence(emp)
        finally:
            emp.init_competence = save_init_competence

        self.assertTrue(self.called, msg='Employee.init_competence() was not called')


class TestStrategy(unittest.TestCase):
    def test_best_strategy(self):
        employees = [employee(3.2), employee(7.3), employee(9.8), employee(6.9)]
        self.assertEquals(9.8, BestStrategy().choose_from(employees).competence)

    def test_worst_strategy(self):
        employees = [employee(3.2), employee(7.3), employee(9.8), employee(6.9)]
        self.assertEquals(3.2, WorstStrategy().choose_from(employees).competence)

    def test_random_strategy(self):
        self.choice_from = []

        def mock_choice(seq):
            self.choice_from = seq
            return seq[-1]

        save_choice = random.choice
        try:
            random.choice = mock_choice
            employees = [employee(3.2), employee(7.3), employee(9.8), employee(6.9)]
            chosen = RandomStrategy().choose_from(employees)
        finally:
            random.choice = save_choice

        self.assertEquals([3.2, 7.3, 9.8, 6.9], [emp.competence for emp in self.choice_from])
        self.assertEquals(6.9, chosen.competence)

def employee(competence):
    emp = Employee()
    emp.competence = competence
    return emp

if __name__ == '__main__':
    unittest.main()
