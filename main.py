from functions import *

INIT_GENS=32
POPULATION_SIZE=50


if __name__ == "__main__":

    target = GetImage('spiderman.png')

    # Population
    # Parent Selection
    generation = 1
    parent = Chromosome(target.size, INIT_GENS)

    # Fitness
    score = Fitness(parent.drawImage(), target)

    while True:
        GetSave(parent , generation, score)
        generation += 1
        children = []
        scores = []
        winners = []
        children.append(parent)
        scores.append(score)

        # Crossover
        if len(winners) >= 2: # If there are at least 2 winners (chromosomes with good fitness scores) in the winners list, a crossover operation is performed.
            children = Crossover([x[0] for x in winners], POPULATION_SIZE - 1)

        # Mutation
        try:
            results = Mutate(parent, POPULATION_SIZE - 1, target) # called to mutate the parent chromosome and generate additional child chromosomes (POPULATION_SIZE - 1 in total).
        except KeyboardInterrupt:
            print("bye")
            exit()
        
        newScores, newChildren = zip(*results) # The results of the mutation operation (results) are unpacked into newScores and newChildren lists using zip(*results).

        children.extend(newChildren)
        scores.extend(newScores)

        winners = sorted(zip(children, scores), key=lambda x:x[1])
        parent, score = winners[0]

        # is termination criterion satisfied ?
        if score == 0 :
            break

    print("Excellent.... \nthe image in generation {} is an exact match to the target image".format(generation))