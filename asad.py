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
    def position_update(self,ll, higherBound):
       for i in range(0,self.dimensions):
           self.current_position[i]=self.current_position[i] + self.velocity[i]

           # checking lower bound
           if self.current_position[i] < ll:
               self.current_position[i]=ll

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
# ll given by user default -10
# ul given by user default 10
# total iteration given by user default 20
# population_size given by user default 10
class PSO():
    def __init__(self, costfunc, positions, ll, ul, population_size, total_iteration):
    
        dimensions = len(positions)
        global_best_cost = -1
        global_best_position = []
        # build house of particles
        house_of_particle = []
        for i in range (0, population_size):
            house_of_particle.append(particle(positions))

        i = 0
        while i < total_iteration:
            for j in range (0, population_size):
                house_of_particle[j].run_cost_function(costfunc)
                if (house_of_particle[j].cost) < global_best_cost or global_best_cost == -1:
                    global_best_cost = float(house_of_particle[j].cost)
                    global_best_position = list(house_of_particle[j].current_position)
                    
            for k in range (0, population_size):
                house_of_particle[k].velocity_update(global_best_position)
                house_of_particle[k].position_update(ll, ul)
            print ("iteration i = " , i , "   " , global_best_position)
            print ("iteration i = " , i , "   " , global_best_cost)
            i+=1

        print (global_best_position)
        print (global_best_cost)

#take input from user

print (sys.argv)

positions = list(map(int, sys.argv[1].split(',')))
ll = int(sys.argv[2])
ul = int(sys.argv[3])
birds = int(sys.argv[4])
total_iterations = int(sys.argv[5])
choose_function = int(sys.argv[6])
print choose_function
if choose_function == 1:
    print "Sphere function", positions, ll, ul, birds, total_iterations
    PSO(sphereFunction, positions, ll, ul, birds, total_iterations)
if choose_function == 2:
    print "Ackley function", positions, ll, ul, birds, total_iterations
    PSO(ackleyFunction, positions, ll, ul, birds, total_iterations)
if choose_function == 3:
    print "Squares Function", positions, ll, ul, birds, total_iterations
    PSO(squaresFunction, positions, ll, ul, birds, total_iterations)
#positions=[10, 12]
#ll = -10
#ul = 10
#birds = 30
#total_iterations = 15
#PSO(sphereFunction, positions, ll, ul, birds, total_iterations)
#PSO(ackleyFunction, positions, ll, ul, birds, total_iterations)
#PSO(squaresFunction, positions, ll, ul, birds, total_iterations)
