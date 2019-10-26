import random
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

points = []
W = 0.8
Wmax = 0.9
Wmin = 0.4
c1 = 2.05
c2 = 2.05
r1 = 0.25
r2 = 0.25
n_iterations = 10000
target_error = 1e-10
n_particles = 30
dimensions = 30
particles_vector = []

class Particle():
    def __init__(self, position):
        self.position = position
        self.pbest_position = self.position
        self.pbest_value = float('inf')
        self.velocity = np.zeros(len(position))

    def __str__(self):
        print("I am at ", self.position, " meu pbest is ", self.pbest_position)
    
    def move(self):
        self.position = self.position + self.velocity

class Space():

    def __init__(self, target_position, target_error, n_particles, particles_vector):
        self.target_position = target_position
        self.target_value = 0 # self.fitness(Particle(target_position))
        self.target_error = target_error
        self.n_particles = n_particles
        self.particles = particles_vector
        self.gbest_value = self.fitness(particles_vector[0])
        self.gbest_position = particles_vector[0].position

    def print_particles(self):
        for particle in self.particles:
            particle.__str__()

    def sphere(self, dimensions):
        total = 0
        for i in range(len(dimensions)):
            total += dimensions[i] ** 2
        return total

    def rastrigin(self, dimensions):
        total = 0
        for i in range(len(dimensions)):
            total += (dimensions[i] ** 2 - 10 * np.cos(2 * np.pi * dimensions[i])) + 10
        return total

    def fitness(self, particle):
        f = self.sphere(particle.position-target_position)
        # f = self.rastrigin(particle.position - target_position)
        return f

    def update_pbest_gbest(self):
        for particle in self.particles:
            fitness_cadidate = self.fitness(particle)
            #set pbest
            if(particle.pbest_value > fitness_cadidate):
                particle.pbest_value = fitness_cadidate
                particle.pbest_position = particle.position
            #set Gbest
            if (self.gbest_value > fitness_cadidate):
                self.gbest_value = fitness_cadidate
                self.gbest_position = particle.position


    def move_particles(self, W, c1, c2, r1, r2):
        for particle in self.particles:
            new_velocity = (W*particle.velocity) + \
                           (c1*r1) * (particle.pbest_position - particle.position) + \
                           (r2*c2) * (self.gbest_position - particle.position)
            particle.velocity = new_velocity
            particle.move()
        

target_position = np.zeros(dimensions)
for d in range(dimensions):
    target_position[d] = (random.random() * 50)

for _ in range(n_particles):
    p = np.zeros(dimensions)
    for d in range(dimensions):
        p[d] = (random.random()*50)
    particles_vector.append(Particle(p))

def main():
    iteration = 0
    bests_fitness = []

    search_space = Space(target_position, target_error, n_particles, particles_vector)

    while(iteration < n_iterations):

        bests_fitness.append(search_space.gbest_value)
        search_space.update_pbest_gbest()

        search_space.move_particles(W, c1, c2, r1, r2)

        if(abs(search_space.gbest_value - search_space.target_value) <= search_space.target_error):
            break
        iteration += 1

    print("The best solution is: ", search_space.gbest_position, "gbest %.4f"% search_space.gbest_value, " in n_iterations: ", iteration, "target ", search_space.target_position)
    plt.plot(bests_fitness)
    plt.show()

main()