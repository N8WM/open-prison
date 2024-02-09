import random
from deap import base, creator, tools, algorithms
from pdilem import Move
from typing import List

# NOTE: Simple Implementation w/deap, more elaborate implementation here
# SOURCE: https://github.com/JoelMorrisey/Prisoners-dilemma/blob/main/main.py

# Step 1: Define Fitness
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# Step 2: Individual Representation
# For simplicity, an individual could be a fixed-length list of moves, representing a strategy
def create_individual() -> List[Move]:
    return [random.choice([Move.COOPERATE, Move.DEFECT]) for _ in range(10)]  # Example length

# Step 3: Evaluation Function
def evaluate(individual):
    # Here, you should implement the logic to evaluate an individual's performance in the game.
    # This could involve simulating games against a fixed strategy or a variety of strategies.
    # Return a tuple with a single element (the fitness score,)
    return (random.uniform(0, 10),)  # Placeholder

# Step 4: Setup Genetic Algorithm Components
toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=2)

# Step 5: Run the Evolutionary Process
def run_evolution(ngen=40, population=None, cxpb=0.5, mutpb=0.2):
    """
    Run the evolutionary algorithm.
    
    :param ngen: Number of generations
    :param population: Initial population (None if starting a new population)
    :param cxpb: Crossover probability
    :param mutpb: Mutation probability
    :return: The evolved population
    """
    if population is None:
        population = toolbox.population(n=100)

    # Evaluate the initial population if not already done
    if not population[0].fitness.valid:
        fitnesses = list(map(toolbox.evaluate, population))
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit

    for gen in range(ngen):
        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cxpb:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < mutpb:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the new individuals
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        population[:] = offspring

    return population

def main():
    evolved_population = run_evolution(ngen=40)
    further_evolved_population = run_evolution(ngen=40, population=evolved_population)
    sample_fitnesses = [ind.fitness.values[0] for ind in further_evolved_population[:5]]
    print("Sample fitnesses from further evolution:\n", sample_fitnesses)


if __name__ == "__main__":
    main()
