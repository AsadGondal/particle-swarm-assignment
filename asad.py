from __future__ import division
import random
import math
import sys
#--- Sphere function -------
def sphereFunction (position):
    total = 0
    for i in range(len(position)):
        total += position[i]**2
    return total

#--- ACKLEY FUNCTION -------
def ackleyFunction (position):
    a = 20
    b = 0.2
    c = 2.0 * math.pi
    firstSum = 0.0
    secondSum = 0.0
    for i in range(len(position)):
        firstSum += position[i]**2.0
        secondSum += math.cos(c * position[i])
    n = float(len(position))
    return -a * math.exp(-b * math.sqrt(firstSum / n)) - math.exp(secondSum / n) + a + math.e

def squaresFunction (position):
    total = 0
    for i in range(len(position)):
        total += i * position[i]**2
    return total

class particle:
    def __init__(self, position):
        self.dimensions = len(position)
        self.velocity = []
        self.best_position = []
        self.best_cost = -1
        self.current_position = []
        self.cost = -1
        for i in range (0, self.dimensions):
            self.velocity.append(random.uniform(0, 0))
            self.current_position.append(position[i])
     
    # update particle velocity
    def velocity_update(self,global_best_position):
        intertia_coefficient = 0.5
        p_acceleration_coefficient = 2
        s_acceleration_coefficient = 2
        for i in range(0,self.dimensions):
            r1=random.uniform(0, 1)
            r2=random.uniform(0, 1)
            cognitive_component = p_acceleration_coefficient * r1 * (self.best_position[i]-self.current_position[i])
            social_component = s_acceleration_coefficient * r2 * (global_best_position[i]-self.current_position[i])
            self.velocity[i]=intertia_coefficient * self.velocity[i] + cognitive_component + social_component
            
    # update particle position
    def position_update(self,lowerBound, higherBound):
       for i in range(0,self.dimensions):
           self.current_position[i]=self.current_position[i] + self.velocity[i]

           # checking lower bound
           if self.current_position[i] < lowerBound:
               self.current_position[i]=lowerBound

           # checking upper bound
           if self.current_position[i] > higherBound:
               self.current_position[i]= higherBound
           
    # call cost/distance function
    def run_cost_function(self,costFunc):
       self.cost = costFunc(self.current_position)

       # check to see if the current position is an individual best
       if self.cost < self.best_cost or self.best_cost == -1:
           self.best_position = self.current_position
           self.best_cost = self.cost
           
# positions given by user in ',' separated form
# lowerBound given by user default -10
# upperBound given by user default 10
# maximum iteration given by user default 20
# population_size given by user default 10
class PSO():
    def __init__(self, costfunc, positions, lowerBound, upperBound, population_size, maximum_iteration):
    
        dimensions = len(positions)
        global_best_cost = -1
        global_best_position = []
        # build house of particles
        house_of_particle = []
        for i in range (0, population_size):
            house_of_particle.append(particle(positions))

        i = 0
        while i < maximum_iteration:
            for j in range (0, population_size):
                house_of_particle[j].run_cost_function(costfunc)
                if (house_of_particle[j].cost) < global_best_cost or global_best_cost == -1:
                    global_best_cost = float(house_of_particle[j].cost)
                    global_best_position = list(house_of_particle[j].current_position)
                    
            for k in range (0, population_size):
                house_of_particle[k].velocity_update(global_best_position)
                house_of_particle[k].position_update(lowerBound, upperBound)
            print ("iteration i = " , i , "   " , global_best_position)
            print ("iteration i = " , i , "   " , global_best_cost)
            i+=1

        print (global_best_position)
        print (global_best_cost)

#take input from user

print (sys.argv)

positions = list(map(int, sys.argv[1].split(',')))
lowerBound = int(sys.argv[2])
upperBound = int(sys.argv[3])
no_of_positions = int(sys.argv[4])
maximum_iterations = int(sys.argv[5])
choose_function = int(sys.argv[6])
print choose_function
if choose_function == 1:
    print "Sphere function", positions, lowerBound, higherBound, no_of_positions, maximum_iterations
    PSO(sphereFunction, positions, lowerBound, higherBound, no_of_positions, maximum_iterations)
if choose_function == 2:
    print "Ackley function", positions, lowerBound, higherBound, no_of_positions, maximum_iterations
    PSO(ackleyFunction, positions, lowerBound, higherBound, no_of_positions, maximum_iterations)
if choose_function == 3:
    print "Squares Function", positions, lowerBound, higherBound, no_of_positions, maximum_iterations
    PSO(squaresFunction, positions, lowerBound, higherBound, no_of_positions, maximum_iterations)
#positions=[10, 12]
#lowerBound = -10
#upperBound = 10
#no_of_positions = 30
#maximum_iterations = 15
#PSO(sphereFunction, positions, lowerBound, upperBound, no_of_positions, maximum_iterations)
#PSO(ackleyFunction, positions, lowerBound, upperBound, no_of_positions, maximum_iterations)
#PSO(squaresFunction, positions, lowerBound, upperBound, no_of_positions, maximum_iterations)
