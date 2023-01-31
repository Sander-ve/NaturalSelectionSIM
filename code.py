import pdb

import random
import matplotlib.pyplot as plt
import numpy as np
import simpy

# Initialize constants
POPULATION_SIZE = 100
MUTATION_PROBABILITY = 0.2
MUTATION_AMOUNT = 1.0
SPEED_START = 5.0
SIZE_START = 5.0
SENSE_START = 10.0
LIFESPAN = 20
ENERGY = 500
GENERATION = 0
MAX_GENERATIONS = 100

COST = 50
EFFICIENCY = 0.3


current_size=[]
current_speed=[]
current_sense=[]
saved_size =[]
saved_speed =[]
saved_sense=[]
saved_population = []


# Create a population of organisms

class Organism:
    def __init__(self, env, speed, size, sense, energy, cost, efficiency):
        self.env = env
        self.speed = speed
        self.size = size
        self.sense = sense
        self.birth_time = self.env.now
        self.death_time = self.birth_time + LIFESPAN
        self.energy = energy
        self.death = False
        
        # cost = 0
        # cost += 0.5*((self.size) * self.speed ** 2)
        # cost += self.sense
        
        self.energy_cost = cost
        # self.efficiency = ((self.speed + self.sense) / self.size) / 100
        self.efficiency = efficiency
        
            
    def gathering(self):
        while True:
            self.energy -= self.energy_cost
            print(self.energy, "Used a bit of energy")
            if random.random() <= self.efficiency:
                # Found food and adds energy
                self.energy += 300
                return
            return

    def live(self):
        if GENERATION >= MAX_GENERATIONS:
            return
        # print("Energy cost =", self.energy_cost)
        # print("Energy Checkpoint 1 = ", self.energy)
        # print("I reached here (live)")
        while True:
            if self.energy <= 0:
                self.death = True
                return 
            #Turns gathering = true which activates the chance to find food + ages 1 time step
            Organism.gathering(self) == True
            # print("Energy Checkpoint 2 = ", self.energy)
            # print("Organism is dead: ", self.death)
            if self.death_time == env.now:
                return
            yield self.env.timeout(1)
            return
            # env.step()
  
    def set_values(self, env, offspring_speed, offspring_size, offspring_sense, offspring_cost, offspring_efficiency):
        # print("this is in set values\n", offspring_speed, offspring_size, offspring_sense)
        self.env = env
        self.speed = offspring_speed
        self.size = offspring_size
        self.sense = offspring_sense
        self.death = False
        self.energy_cost = offspring_cost
        self.efficiency = offspring_efficiency

    #Reproduce function, the parent reproduces at the end of their lifespan and gives off their traits + a random mutation rate
    #onto their descendants             
    def reproduce(self):
        # print("I reached here (reproduce)")
        # print(f"Before: {self.speed} {self.size} {self.sense}")
        if self.death == True:
            print("Organism died and shouldnt reproduce")
            return
        
        current_size.append(self.size)
        current_speed.append(self.speed)
        current_sense.append(self.sense)
        MUTATION_CHANCE = random.random() # Random value between 0 - 1
        offspring_speed = 0
        offspring_sense = 0
        offspring_size = 0
        if MUTATION_CHANCE < MUTATION_PROBABILITY: #0.2 aka 20% chance of being below 0.2
            print("ORGANISM MUTATED")
            offspring_speed = self.speed + random.uniform(-MUTATION_AMOUNT, MUTATION_AMOUNT)
            offspring_size = self.size + random.uniform(-MUTATION_AMOUNT, MUTATION_AMOUNT)
            offspring_sense = self.sense + random.uniform(-MUTATION_AMOUNT, MUTATION_AMOUNT)
            # print("New values are", offspring_speed, offspring_size, offspring_sense)
        else: 
            offspring_speed = self.speed
            offspring_size = self.size
            offspring_sense = self.sense
        
        offspring_cost = 0
        offspring_cost += 0.5*((offspring_size) * offspring_speed ** 2)
        offspring_cost += offspring_sense

        self.efficiency = ((offspring_speed + offspring_sense) / offspring_size) / 100
        offspring_efficiency = self.efficiency

        self.set_values(env, offspring_speed, offspring_size, offspring_sense, offspring_cost, offspring_efficiency)
        # return the organism class in case the helper method does not function
# Initialize the environment and create a starting population
env = simpy.Environment()

# population = [Organism(env, SPEED_START, SIZE_START, SENSE_START, ENERGY, COST, EFFICIENCY) for _ in range(POPULATION_SIZE)]
population = []
for i in range(POPULATION_SIZE):
    population.append(Organism(env, SPEED_START, SIZE_START, SENSE_START, ENERGY, COST, EFFICIENCY))
# print("this is the population list", population)
# print(type(population[0])) #hopefully not a NoneType ( so a Organism  )

def simulate():
    global GENERATION
    global population
    if GENERATION >= MAX_GENERATIONS or population == 0:
        return
    # Reproduce at the end of each organism's lifespan
    # print("I reached here (simulate)")
    global saved_population
    # new_organisms = [organism.reproduce() for organism in population]
    new_organisms = []
    for organism in population:
        # organism = organism.reproduce()
        Organism.reproduce(organism)
        if(organism.death == False):
            new_organisms.append(organism)
    
    population = new_organisms
    GENERATION += 1
    print("Finished generation", GENERATION)
    if current_size:
        saved_size.append(np.average(current_size))
    if current_speed:
        saved_speed.append(np.average(current_speed))
    if current_sense:
        saved_sense.append(np.average(current_sense))
    saved_population.append(len(population))

    current_size.clear()
    current_speed.clear()
    current_sense.clear()
    yield env.timeout(LIFESPAN)
       
# Run the simulation
def run():
    print("Executing run()")
    for i in range(MAX_GENERATIONS):
        while i > 0:
            for organism in population:
                env.process(organism.live())
            env.process(simulate())
            i -= 1
    env.run(until=100)       
 
    
# Plot the distribution of traits at the end of the simulation
def speed_plot():
    x = np.array(saved_speed)
    plt.title("Speed")
    plt.plot(x)
    plt.show()

def size_plot():
    x = np.array(saved_size)
    plt.title("Size")
    plt.plot(x)
    plt.show()

def sense_plot():
    x = np.array(saved_sense)
    plt.title("Sense")
    plt.plot(x)
    plt.show()

def pop_plot():
    x = saved_population
    plt.title("Population")
    plt.plot(x)
    plt.show()

run()
#Show the plots
speed_plot()
size_plot()
sense_plot()
pop_plot()

