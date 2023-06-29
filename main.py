from functions import *

INIT_GENS=32
POPULATION_SIZE=50


if __name__ == "__main__":

    target = GetImage('spiderman.png')

    generation = 1
    parent = Chromosome(target.size, INIT_GENS)
    score = Fitness(parent.drawImage(), target)
    while True:
        GetSave(parent , generation, score)
        generation += 1
        children = []
        scores = []
        winners = []
        children.append(parent)
        scores.append(score)

        if len(winners) >= 2:
            children = Crossover([x[0] for x in winners], POPULATION_SIZE - 1)

            

        try:
            results = Mutate(parent, POPULATION_SIZE - 1, target)
        except KeyboardInterrupt:
            print("bye")
            exit()
        
        newScores, newChildren = zip(*results)

        children.extend(newChildren)
        scores.extend(newScores)

        winners = sorted(zip(children, scores), key=lambda x:x[1])
        parent, score = winners[0]