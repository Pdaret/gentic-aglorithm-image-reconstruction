from functions import *

if __name__ == "__main__":
    target = getImage('amugus.png')
    run(target,initial_gens=32, generation_per_image=150, pop_per_generation=50)