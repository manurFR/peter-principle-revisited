import unittest

from employee import Employee
from organization import Layer, Organization
from strategies import BestStrategy


def emp(age, competence):
    employee = Employee()
    employee.age = age
    employee.competence = competence
    return employee


class MockHypothesis:
    def __init__(self):
        self.called = False

    def compute_new_competence(self, employee):
        self.called = True


class TestOrganization(unittest.TestCase):
    def test_promote(self):
        hypothesis = MockHypothesis()
        orga = Organization(hypothesis=hypothesis, strategy=BestStrategy())
        orga.add_layer(1, size=1, efficiency_weight=1.0)
        orga.add_layer(2, size=3, efficiency_weight=1.0)

        best_employee = emp(38, 7.5)
        worst_employee = emp(25, 3.0)
        average_employee = emp(49, 6.3)

        # layer 1 has a vacancy
        orga.layers[2].employees = [worst_employee, best_employee, average_employee]

        orga.promote(origin=orga.layers[2], destination=orga.layers[1])

        self.assertEquals([best_employee],                          orga.layers[1].employees)
        self.assertEquals([worst_employee, None, average_employee], orga.layers[2].employees)
        self.assertTrue(hypothesis.called)
        self.assertEquals(7.5, orga.layers[1].employees[0].competence)

    def test_workforce(self):
        orga = Organization(hypothesis=None, strategy=None)
        orga.add_layer(1, size=2, efficiency_weight=1.0)
        orga.add_layer(2, size=3, efficiency_weight=1.0)
        orga.add_layer(3, size=5, efficiency_weight=1.0)

        self.assertEquals(10, orga.workforce())

    def test_maximum_efficiency(self):
        orga = Organization(hypothesis=None, strategy=None)
        orga.add_layer(1, size=2, efficiency_weight=1.0)
        orga.add_layer(2, size=3, efficiency_weight=0.6)
        orga.add_layer(3, size=5, efficiency_weight=0.2)

        self.assertEquals((2*10*1.0 + 3*10*0.6 + 5*10*0.2) / 10, orga.maximum_efficiency())

    def test_global_efficiency(self):
        orga = Organization(hypothesis=None, strategy=None)
        orga.add_layer(1, size=2, efficiency_weight=1.0)
        orga.add_layer(2, size=3, efficiency_weight=0.6)
        orga.add_layer(3, size=5, efficiency_weight=0.2)

        orga.layers[1].employees = [emp(25, 8.0), emp(25, 9.0)]
        orga.layers[2].employees = [emp(25, 7.0), emp(25, 2.0), emp(25, 7.0)]
        orga.layers[3].employees = [emp(25, 6.0), emp(25, 5.5), emp(25, 10.0), None, emp(25, 7.0)]

        self.assertEquals(100 * ((8.0 + 9.0) * 1.0 + (7.0 + 2.0 + 7.0) * 0.6 + (6.0 + 5.5 + 10.0 + 7.0) * 0.2) /
                                 (orga.workforce() * orga.maximum_efficiency()),
                          orga.global_efficiency())


class TestLayer(unittest.TestCase):
    emp25_7 = emp(25, 7.0)
    emp58_8 = emp(58, 8.5)
    emp32_3 = emp(32, 3.1)
    emp44_9 = emp(44, 9.9)
    emp63_2 = emp(63, 2.8)

    def test_prune(self):
        layer = Layer(5, 0)
        layer.employees = [self.emp25_7, self.emp58_8, self.emp32_3, self.emp44_9, self.emp63_2]

        layer.prune(min_competence=4.0, max_age=55)

        self.assertEquals([self.emp25_7, None, None, self.emp44_9, None], layer.employees)

    def test_hire(self):
        layer = Layer(5, 0)
        layer.employees = [self.emp25_7, None, self.emp58_8, None, self.emp63_2]

        layer.hire()

        self.assertIsNotNone(layer.employees[1])
        self.assertIsNotNone(layer.employees[3])

if __name__ == '__main__':
    unittest.main()
