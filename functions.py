import os
import numpy as np
from PIL import Image
from copy import deepcopy
from helper import *

MAX_SIZE = 500

def getImage(path):
    try:
        target = Image.open(path)
        target.convert("RGB")
        height , width = target.size
        if height > 500:
            target.resize((MAX_SIZE , width))
        elif width > 500:
            target.resize((height , MAX_SIZE))
        else:
            return target
    except IOError:
        print("Oops!!!! try again....")
        exit()


def foo(img1 , img2):
    i1 = np.array(img1, dtype=np.int16)
    i2 = np.array(img2, dtype=np.int16)
    diff = np.abs(np.square(i1 - i2))
    root_diff = np.sqrt(diff)
    sq_sum = np.sum(root_diff)
    return sq_sum, i1.size 

def fitness(img1, img2):
    dif, size = foo(img1 , img2 )
    return (dif/255.0*100)/size

def run(target, initial_gens, generation_per_image, pop_per_generation):
    if not os.path.exists("results"):
        os.mkdir("results")
    generation = 1
    parent = Organism(target.size, initial_gens)
    score = fitness(parent.drawImage(), target)
    while True:
        print("Generation {}-{}".format(generation, score))
        if generation % generation_per_image == 0:
            parent.drawImage().save(os.path.join("results", "{}.png".format(generation)))
        generation += 1
        children = []
        scores = []
        winners = []
        children.append(parent)
        scores.append(score)


        if len(winners) >= 2:
            children = groupCrossover([x[0] for x in winners], pop_per_generation - 1)

        try:
             results = groupMutate(parent, pop_per_generation - 1, target)
        except KeyboardInterrupt:
             print("bye")
             return
        
        newScores, newChildren = zip(*results)

        children.extend(newChildren)
        scores.extend(newScores)

        winners = sorted(zip(children, scores), key=lambda x:x[1])
        parent, score = winners[0]


def groupCrossover(parents, number):
    results = []
    for _ in range(number):
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)
        child = parent1.crossover(parent2)
        results.append(child)
    return results


def groupMutate(parent, number,target):
    results = []
    for _ in range(number):
        chromosomes = deepcopy(parent)
        chromosomes.mutate()
        i1 = chromosomes.drawImage()
        i2 = target
        fitness_score = fitness(i1, i2)
        results.append((fitness_score, chromosomes))
    return results
