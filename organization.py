import copy
import statistics

from employee import Employee

MIN_COMPETENCE = 4.0
MAX_AGE = 60


class Simulation:
    def __init__(self, nb_organizations, topology, min_competence=MIN_COMPETENCE, max_age=MAX_AGE):
        self.current_run = None
        self.history = None

        # topology format : {level: (nb_positions, efficiency_weight), ...}
        template = Organization(min_competence, max_age)
        for level, characteristics in topology.items():
            template.add_layer(number=level, size=characteristics[0], efficiency_weight=characteristics[1])

        self.starting_state = [copy.deepcopy(template) for _ in range(nb_organizations)]
        for organization in self.starting_state:
            organization.populate()

    def prepare(self, hypothesis, strategy):
        self.current_run = copy.deepcopy(self.starting_state)
        for organization in self.current_run:
            organization.set_strategies(hypothesis, strategy)
        self.history = [self.averaged_global_efficiency()]

    def step(self):
        for organization in self.current_run:
            organization.step()
        self.history.append(self.averaged_global_efficiency())

    def averaged_global_efficiency(self):
        return statistics.mean(organization.global_efficiency() for organization in self.current_run)


class Organization:
    def __init__(self, min_competence=4.0, max_age=60):
        self.layers = {}
        self.hypothesis = None
        self.strategy = None
        self.min_competence = min_competence
        self.max_age = max_age

    def add_layer(self, number, size, efficiency_weight):
        self.layers[number] = Layer(size, efficiency_weight)

    def populate(self):
        for layer in self.layers.values():
            layer.hire()

    def set_strategies(self, hypothesis, strategy):
        self.hypothesis = hypothesis
        self.strategy = strategy

    def step(self):
        for level in sorted(self.layers.keys()):
            self.layers[level].prune(self.min_competence, self.max_age)
            if self.layers.get(level+1):
                self.promote(origin=self.layers[level+1], destination=self.layers[level])
            else:
                self.layers[level].hire()
            self.layers[level].grow_up()

    def promote(self, origin, destination):
        assert self.hypothesis is not None and self.strategy is not None
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
