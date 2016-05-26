import copy
import statistics

from organization import Organization
from strategies import PeterHypothesis, BestStrategy

NB_REALIZATIONS = 50
NB_STEPS = 100

#  {level: (nb_positions, efficiency_weight)
TOPOLOGY = {1: (1, 1.0),
            2: (5, 0.9),
            3: (11, 0.8),
            4: (21, 0.6),
            5: (41, 0.4),
            6: (81, 0.2)}

MIN_COMPETENCE = 4.0
MAX_AGE = 60


def averaged_global_efficiency(configurations):
    return statistics.mean(organization.global_efficiency() for organization in configurations)

if __name__ == '__main__':
    print('The Peter Principle Revisited: A Computational Study')
    print('  Pluchino, A., Rapisarda, A., Garolafo, C. (2009)')
    print('  Universita di Catania, Italy')
    print('  arXiv:0907.0455 [physics.soc-ph]')
    print('=' * 55)
    print()

    organization_template = Organization(hypothesis=PeterHypothesis(), strategy=BestStrategy(),
                                         min_competence=MIN_COMPETENCE, max_age=MAX_AGE)
    for level, characteristics in TOPOLOGY.items():
        organization_template.add_layer(number=level, size=characteristics[0], efficiency_weight=characteristics[1])

    realizations_template = [copy.deepcopy(organization_template) for _ in range(NB_REALIZATIONS)]
    for organization in realizations_template:
        organization.populate()

    history = [averaged_global_efficiency(realizations_template)]

    print('Global effiency:')
    print('Initial     : {0:5.2f}'.format(history[0]))

    for step in range(NB_STEPS):
        for organization in realizations_template:
            organization.step()

        history.append(averaged_global_efficiency(realizations_template))

        print('Step {0:>6} : {1:5.2f}'.format(step+1, history[-1]))