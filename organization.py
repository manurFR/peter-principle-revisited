from employee import Employee


class Organization:
    def __init__(self, hypothesis, strategy, min_competence=4.0, max_age=60):
        self.layers = {}
        self.hypothesis = hypothesis
        self.strategy = strategy
        self.min_competence = min_competence
        self.max_age = max_age

    def add_layer(self, number, size, efficiency_weight):
        self.layers[number] = Layer(size, efficiency_weight)

    def populate(self):
        for layer in self.layers.values():
            layer.hire()

    def step(self):
        for level in sorted(self.layers.keys()):
            self.layers[level].prune(self.min_competence, self.max_age)
            if self.layers.get(level+1):
                self.promote(origin=self.layers[level+1], destination=self.layers[level])
            else:
                self.layers[level].hire()
            self.layers[level].grow_up()

    def promote(self, origin, destination):
        for index, employee in enumerate(destination.employees):
            if employee is None:
                promoted = self.strategy.choose_from(origin.employees)
                origin.employees[origin.employees.index(promoted)] = None
                self.hypothesis.compute_new_competence(promoted)
                destination.employees[index] = promoted

    def workforce(self):
        return sum(layer.size for layer in self.layers.values())

    def maximum_efficiency(self):
        return sum(10 * layer.size * layer.efficiency_weight for layer in self.layers.values()) / self.workforce()

    def global_efficiency(self):
        return 100 * (sum(layer.weighted_efficiency() for layer in self.layers.values()) /
                      (self.maximum_efficiency() * self.workforce()))


class Layer:
    def __init__(self, size, efficiency_weight):
        self.size = size
        self.efficiency_weight = efficiency_weight
        self.employees = [None] * size

    def prune(self, min_competence, max_age):
        for index, employee in enumerate(self.employees):
            if employee is not None and (employee.competence < min_competence or employee.age > max_age):
                self.employees[index] = None

    def hire(self):
        for index, employee in enumerate(self.employees):
            if employee is None:
                self.employees[index] = Employee()

    def grow_up(self):
        for index, employee in enumerate(self.employees):
            if employee is not None:
                self.employees[index].age += 1

    def weighted_efficiency(self):
        return self.efficiency_weight * sum(employee.competence for employee in self.employees if employee is not None)

    def __repr__(self):
        return 'size={0}, efficiency_weight={1}, employees={2}'.format(self.size, self.efficiency_weight, self.employees)
