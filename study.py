import itertools

from organization import Simulation, MIN_COMPETENCE, MAX_AGE
from strategies import PeterHypothesis, BestStrategy, CommonSenseHypothesis, WorstStrategy, RandomStrategy

NB_ORGANIZATIONS = 50
NB_STEPS = 100

#  {level: (nb_positions, efficiency_weight), ...}
TOPOLOGY = {1: (1, 1.0),
            2: (5, 0.9),
            3: (11, 0.8),
            4: (21, 0.6),
            5: (41, 0.4),
            6: (81, 0.2)}

if __name__ == '__main__':
    print('The Peter Principle Revisited: A Computational Study')
    print('  Pluchino, A., Rapisarda, A., Garolafo, C. (2009)')
    print('  Universita di Catania, Italy')
    print('  arXiv:0907.0455 [physics.soc-ph]')
    print('=' * 55)

    simulation = Simulation(NB_ORGANIZATIONS, TOPOLOGY, MIN_COMPETENCE, MAX_AGE)

    runs = itertools.product([PeterHypothesis(), CommonSenseHypothesis()],
                             [BestStrategy(), WorstStrategy(), RandomStrategy()])
    results = []
    for index, (hypothesis, strategy) in enumerate(runs):
        simulation.prepare(hypothesis, strategy)

        print('.', end="", flush=True)

        for step in range(NB_STEPS):
            simulation.step()

        results.append((hypothesis, strategy, simulation.history[-1] - simulation.history[0]))

    print()
    print()

    print('Efficiency evolution after {0} time units:'.format(NB_STEPS))

    for hypothesis, strategy, evolution in results:
        print('{0:>50}: {1:5.2f}'.format('{0} & {1}'.format(hypothesis, strategy), evolution))