import os
import numpy as np
from PIL import Image
from copy import deepcopy
from helper import *

MAX_SIZE = 500
IMAGE_GENERATION=500

def GetImage(path):
    # loads and prepares an image from the specified path.
    try:
        target = Image.open(path)
        target.convert("RGB")
        height , width = target.size
        if height > MAX_SIZE:
            target.resize((MAX_SIZE , width))
        elif width > MAX_SIZE:
            target.resize((height , MAX_SIZE))
        else:
            return target
    except IOError:
        print("Oops!!!! try again....")
        exit()


def foo(img1 , img2):
    # calculates the squared sum of the difference between two images.
    i1 = np.array(img1, dtype=np.int16)
    i2 = np.array(img2, dtype=np.int16)
    diff = np.abs(np.square(i1 - i2))
    root_diff = np.sqrt(diff)
    sq_sum = np.sum(root_diff)
    return sq_sum, i1.size 

def Fitness(img1, img2):
    # calculates the fitness score between two images.
    dif, size = foo(img1 , img2 )
    return (dif/255.0*100)/size

def Crossover(parents, number):
    # performs crossover between a list of parent chromosomes.
    results = []
    for _ in range(number):
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)
        child = parent1.crossover(parent2)
        results.append(child)
    return results


def Mutate(parent, number,target):
    # performs mutation on a parent chromosome.
    results = []
    for _ in range(number):
        chromosomes = deepcopy(parent)
        chromosomes.mutate()
        i1 = chromosomes.drawImage()
        i2 = target
        fitness_score = Fitness(i1, i2)
        results.append((fitness_score, chromosomes))
    return results

def GetSave(parent, generation, score):
    # handles saving the generated images.
    if not os.path.exists("results"):
        os.mkdir("results")

    print("Generation {}-{}".format(generation, score))
    if generation % IMAGE_GENERATION == 0 or generation == 100:
        parent.drawImage().save(os.path.join("results", "{}.png".format(generation)))