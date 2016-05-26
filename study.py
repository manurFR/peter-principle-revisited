import argparse
import itertools

from organization import Simulation, MIN_COMPETENCE, MAX_AGE
from strategies import PeterHypothesis, BestStrategy, CommonSenseHypothesis, WorstStrategy, RandomStrategy, \
    BestWorstStrategy

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
    parser = argparse.ArgumentParser(description='The Peter Principle Revisited: A Computational Study')
    parser.add_argument('-s', '--study', action='store_true', help='Run the main comparison between the six combinations of parameters, as in the study')
    parser.add_argument('-bw', '--bestworst', action='store_true', help='Run the Best-Worst strategy for the two hypothesis, as in the study')
    args = parser.parse_args()

    if not any(v for v in vars(args).values()):
        args.study = True

    print('The Peter Principle Revisited: A Computational Study')
    print('  Pluchino, A., Rapisarda, A., Garolafo, C. (2009)')
    print('  Universita di Catania, Italy')
    print('  arXiv:0907.0455 [physics.soc-ph]')
    print('=' * 55)

    simulation = Simulation(NB_ORGANIZATIONS, TOPOLOGY, MIN_COMPETENCE, MAX_AGE)
    if args.study:
        runs = itertools.product([PeterHypothesis(), CommonSenseHypothesis()],
                                 [BestStrategy(), WorstStrategy(), RandomStrategy()])
        results = []
        for hypothesis, strategy in runs:
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

    if args.bestworst:
        results = []
        for hypothesis in [PeterHypothesis(), CommonSenseHypothesis()]:
            for p in range(11):
                simulation.prepare(hypothesis, BestWorstStrategy(p/10))

                print('.', end="", flush=True)

                for step in range(NB_STEPS):
                    simulation.step()

                results.append([hypothesis, p/10, simulation.history[-1]])
            print()
        print()
        print()

        print('Starting efficiency: {0:5.2f}'.format(simulation.history[0]))

        print('Final efficiencies:')
        for hypothesis, p, efficiency in results:
            print('{0:>25} for {1}%: {2:5.2f}'.format(repr(hypothesis), p, efficiency))