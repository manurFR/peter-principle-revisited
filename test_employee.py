import unittest

from employee import Employee


class TestEmployee(unittest.TestCase):
    def test_modify_competence(self):
        emp = Employee()
        emp.competence = 8.2

        emp.modify_competence(increment=0.3)
        self.assertEqual(8.5, emp.competence)

    def test_modify_competence_limit_high(self):
        emp = Employee()
        emp.competence = 9.9

        emp.modify_competence(increment=0.3)
        self.assertEqual(10.0, emp.competence)

    def test_modify_competence_limit_low(self):
        emp = Employee()
        emp.competence = 0.2

        emp.modify_competence(increment=-0.5)
        self.assertEqual(0.0, emp.competence)


if __name__ == '__main__':
    unittest.main()
