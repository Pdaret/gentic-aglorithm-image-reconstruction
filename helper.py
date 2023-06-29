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
            # mutation_size = max(1, int(round(random.gauss(15, 4))))/100
            mutation_type = random.choice(self.params)
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
        if len(self.genes) < 200:
            for g in self.genes:
                if MUTATION_CHANCE > random.random():
                    g.mutate()

        else:
            for g in random.sample(self.genes, int(len(self.genes) * MUTATION_CHANCE)):
                g.mutate()

        if ADD_GENE_CHANCE > random.random():
            self.genes.append(Gene(self.size))
        if len(self.genes) > 0 and REM_GENE_CHANCE > random.random():
            self.genes.remove(random.choice(self.genes))
    
    def crossover(self, other):
        # Perform uniform crossover between self and other
        # Create a new Chromosome as the child
        child = Chromosome(self.size, 0)

        for i in range(len(self.genes)):
            if random.random() < CROSSOVER_CHANCE:
                child.genes.append(deepcopy(self.genes[i]))
            else:
                child.genes.append(deepcopy(other.genes[i]))

        return child

    def drawImage(self):
        image = Image.new('RGB', self.size, (255, 255, 255))
        canvas = ImageDraw.Draw(image)

        for g in self.genes:
            color = (g.color.r, g.color.g, g.color.b)
            canvas.ellipse([g.pos.x-g.diameter, g.pos.y-g.diameter, g.pos.x+g.diameter, g.pos.y+g.diameter], outline = color, fill = color)
        return image

