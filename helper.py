import random
from PIL import Image
from PIL import ImageDraw
from copy import deepcopy

MUTATION_CHANCE = 0.01
ADD_GENE_CHANCE = 0.3
REM_GENE_CHANCE = 0.2
CROSSOVER_CHANCE = 0.5

class Point:
    # A 2d point
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
class Color:
    # A color
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b


class Gene:
    # gene
    def __init__(self, size):
        self.size = size
        self.diameter = random.randint(2, 10)
        self.pos = Point(random.randint(0, size[0]), random.randint(0, size[1]))
        self.color = Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.params = ["diameter", "pos", "color"]

    def mutate(self):
        mutation_type = random.choice(self.params) # randomly selects a mutation type from the available parameters (diameter, pos, color).
        if mutation_type == 'diameter':
            self.diameter = random.randint(2, 10)
        elif mutation_type == 'pos':
            x = random.randint(0, self.size[0])
            y = random.randint(0, self.size[1])
            self.pos = Point(x,y)
        elif mutation_type == "color":
            self.color = Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


class Chromosome:
    def __init__(self, size, num):
        self.size = size
        self.genes = [Gene(size) for _ in range(num)]

    def mutate(self):
        # performs mutation on the chromosome's genes.
        if len(self.genes) < 200: #If the number of genes is 200 or more, a random sample of genes is selected for mutation based on MUTATION_CHANCE.
            for g in self.genes:
                if MUTATION_CHANCE > random.random():
                    g.mutate()

        else:
            for g in random.sample(self.genes, int(len(self.genes) * MUTATION_CHANCE)):
                g.mutate()

        if ADD_GENE_CHANCE > random.random(): # If ADD_GENE_CHANCE is greater than a random value, a new gene is appended to the genes list.
            self.genes.append(Gene(self.size))
        if len(self.genes) > 0 and REM_GENE_CHANCE > random.random(): # If there are genes in the chromosome and REM_GENE_CHANCE is greater than a random value, a random gene is removed from the genes list.
            self.genes.remove(random.choice(self.genes))
    
    def crossover(self, other):
        # Perform uniform crossover between self and other
        # Create a new Chromosome as the child
        child = Chromosome(self.size, 0)

        # For each gene in the chromosome, if a random value is less than CROSSOVER_CHANCE, a deepcopy of the corresponding gene from self is added to the child chromosome.
        # Otherwise, a deepcopy of the corresponding gene from other is added to the child chromosome.
        for i in range(len(self.genes)):            
            if random.random() < CROSSOVER_CHANCE:
                child.genes.append(deepcopy(self.genes[i]))
            else:
                child.genes.append(deepcopy(other.genes[i]))

        return child

    def drawImage(self):
        # creates a new image with the specified size and white background
        image = Image.new('RGB', self.size, (255, 255, 255))
        canvas = ImageDraw.Draw(image)

        for g in self.genes:
            color = (g.color.r, g.color.g, g.color.b)
            canvas.ellipse([g.pos.x-g.diameter, g.pos.y-g.diameter, g.pos.x+g.diameter, g.pos.y+g.diameter], outline = color, fill = color)
        return image

