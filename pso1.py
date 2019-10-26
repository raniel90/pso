import random
import math
import numpy as np
import matplotlib.pyplot as plt

w = 1
c1 = 2.05
c2 = 2.05
r1 = 0.25
r2 = 0.25
n_iterations = 10
n_particles = 3
speed_limit = 3
target_position = np.array([5,5])

class Particle():
    def __init__(self, position):
        self.position = position
        self.pbest_position = self.position
        self.pbest_value = float('inf')
        self.velocity = np.array([0, 0])

    def __str__(self):
        print("I am at ", self.position, " meu pbest is ", self.pbest_position)
    
    def move(self):
        self.position = self.position + self.velocity

class Space():
    def __init__(self, target_position, n_particles, particles_vector):
        self.target_position = target_position
        self.target_value = 0 # self.fitness(Particle(target_position))
        self.n_particles = n_particles
        self.particles = particles_vector
        self.gbest_value = float('inf')
        self.gbest_position = np.array([random.random()*50, random.random()*50])

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
        f = self.sphere(particle.position - target_position)
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


    def move_particles(self, w, c1, c2, r1, r2, speed_limit):
        for particle in self.particles:
            new_velocity = (w*particle.velocity) + \
                           (c1*r1) * (particle.pbest_position - particle.position) + \
                           (r2*c2) * (self.gbest_position - particle.position)

            # redutor de velocidade
            mod_v = math.sqrt((new_velocity[0]**2 + new_velocity[0]**2))
            if(mod_v > speed_limit):
                new_velocity /= (mod_v / speed_limit)

            particle.velocity = new_velocity
            particle.move()

def get_particles():
    p1 = Particle(np.array([5,5]))
    p1.pbest_position = np.array([5,5])
    p1.velocity = np.array([2,2])

    p2 = Particle(np.array([8,3]))
    p2.pbest_position = np.array([7,3])
    p2.velocity = np.array([3,3])

    p3 = Particle(np.array([6,7]))
    p3.pbest_position = np.array([5,6])
    p3.velocity = np.array([4,4])

    return [p1, p2, p3]

def get_search_space(particles_vector):
    # init space
    search_space = Space(target_position, n_particles, particles_vector)
    search_space.print_particles()

    return search_space

def main():
    iteration = 0
    bests_fitness = []

    particles_vector = get_particles()
    search_space = get_search_space(particles_vector)
    
    while(iteration < n_iterations):
        bests_fitness.append(search_space.gbest_value)
        search_space.update_pbest_gbest()

        search_space.move_particles(w, c1, c2, r1, r2, speed_limit)

        if(iteration == 0):
            i=1
            for p in particles_vector:
                print('Particula P'+str(i), p.position)
                i+=1

        iteration += 1

    print("The best result is: ", search_space.gbest_position, "gbest %.2f"% search_space.gbest_value, " in n_iterations: ", iteration, "target ", search_space.target_position)
    #print(bests_fitness)
    plt.plot(bests_fitness)
    plt.show()

main()