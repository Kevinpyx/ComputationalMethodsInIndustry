"""
hw3.py
Name(s): Seiju Hirose and Kevin Peng
Date: March 9, 2024
"""

import math
import random as rdm
import Organism as Org
import numpy as np
import matplotlib.pyplot as plt

"""
crossover operation for genetic algorithm
"""
def crossover(parent1, parent2):
    # numCoeffs = len(parent1.bits)//64
    # k = rdm.randint(0, numCoeffs)
    # child1 = Org.Organism(numCoeffs, np.concatenate((parent1.bits[0:64*k], parent2.bits[64*k:])))
    # child2 = Org.Organism(numCoeffs, np.concatenate((parent2.bits[0:64*k], parent1.bits[64*k:])))

    lenBits = len(parent1.bits)
    numCoeffs = lenBits//64
    k = rdm.randint(0, lenBits)
    child1 = Org.Organism(numCoeffs, np.concatenate((parent1.bits[0:k], parent2.bits[k:])))
    child2 = Org.Organism(numCoeffs, np.concatenate((parent2.bits[:k], parent1.bits[k:])))

    return child1, child2

"""
mutation operation for genetic algorithm
"""
def mutation(genome, mutRate):
    for bit in genome:
        r = rdm.random()
        if r<mutRate:
            bit = 1-bit
    return genome

"""
selection operation for choosing a parent for mating from the population
"""
def selection(pop):
    threshold = rdm.random()
    length = len(pop)
    i = 0
    while pop[i].accFit < threshold and i < length:
        i += 1
    return pop[i] if i < length else pop[-1]

"""
calcFit will calculate the fitness of an organism
"""
def calcFit(org, xVals, yVals):
    # Create a variable to store the running sum error.
    error = 0

    # Loop over each x value.
    for ind in range(len(xVals)):
        # Create a variable to store the running sum of the y value.
        y = 0
        
        # Compute the corresponding y value of the fit by looping
        # over the coefficients of the polynomial.
        for n in range(len(org.floats)):
            # Add the term c_n*x^n, where c_n are the coefficients.
            try:
                y += org.floats[n] * (xVals[ind])**n
            except OverflowError:
                y += math.inf

        # Compute the squared error of the y values, and add to the running
        # sum of the error.
        try:
            error += (y - yVals[ind])**2
        except OverflowError:
            error += math.inf

    # Now compute the sqrt(error), average it over the data points,
    # and return the reciprocal as the fitness.
    if error == 0:
        return math.inf
    else:
        fitness = len(xVals)/math.sqrt(error)
        if not math.isnan(fitness):
            return fitness
        else:
            return 0

"""
accPop will calculate the fitness and accFit of the population
"""
def accPop(pop, xVals, yVals):

    # calculate fitness for every org and the sum of fitness
    fitnessSum = 0
    for org in pop:
        org.fitness = calcFit(org, xVals, yVals)
        fitnessSum += org.fitness

    # sort the population by fitness in descending order (https://stackoverflow.com/questions/403421/how-do-i-sort-a-list-of-objects-based-on-an-attribute-of-the-objects)
    pop.sort(key=lambda x: x.fitness, reverse=True)

    # calculate normalized fitness
    for org in pop:
        org.normFit = org.fitness/fitnessSum

    # calculate accFit
    accFit = 0
    for org in pop:
        accFit += org.normFit
        org.accFit = accFit
    
    return pop

"""
initPop will initialize a population of a given size and number of coefficients
"""
def initPop(size, numCoeffs):
    # Get size-4 random organisms in a list.
    pop = [Org.Organism(numCoeffs) for x in range(size-4)]

    # Create the all 0s and all 1s organisms and append them to the pop.
    pop.append(Org.Organism(numCoeffs, [0]*(64*numCoeffs)))
    pop.append(Org.Organism(numCoeffs, [1]*(64*numCoeffs)))

    # Create an organism corresponding to having every coefficient as 1.
    bit1 = [0]*2 + [1]*10 + [0]*52
    org = []
    for c in range(numCoeffs):
        org = org + bit1
    pop.append(Org.Organism(numCoeffs, org))

    # Create an organism corresponding to having every coefficient as -1.
    bit1 = [1,0] + [1]*10 + [0]*52
    org = []
    for c in range(numCoeffs):
        org = org + bit1
    pop.append(Org.Organism(numCoeffs, org))

    # Return the population.
    return pop

"""
nextGeneration will create the next generation
"""
def nextGeneration(pop, numCoeffs, mutRate, eliteNum):
    newPop = []

    # mate
    for i in range((len(pop)-eliteNum)//2):
        # selection
        parent1 = selection(pop)
        parent2 = selection(pop)
        # crossover
        child1, child2 = crossover(parent1, parent2)
        # mutation
        child1.bits = mutation(child1.bits, mutRate)
        child2.bits = mutation(child2.bits, mutRate)
        # append
        newPop.extend([child1, child2])

    # append the elites
    newPop.extend(pop[:eliteNum])

    return newPop

"""
containsClone: checks whether newOrg has a clone in lst.
"""
def containsClone(lst, newOrg):
    for org in lst: 
        if org.isClone(newOrg):
            return True
    return False

"""
updateBestN: takes in the list of bestN number of best organisms and newPop to get the new Best organisms
"""
def updateBest(best, newPop):
    tail = best[-1]
    i = 0
    while(i < len(newPop) and newPop[i].fitness > tail.fitness):
        if containsClone(best, newPop[i]):
            pass # do nothing
        else: 
            best[-1] = newPop[i] # replace the tail
            best.sort(key=lambda x: x.fitness, reverse=True) # sort best

        # update indices
        i += 1
        tail = best[-1]

    return best

"""
GA will perform the genetic algorithm for k+1 generations (counting
the initial generation).

INPUTS
k:         the number of generations
size:      the size of the population
numCoeffs: the number of coefficients in our polynomials
mutRate:   the mutation rate
xVals:     the x values for the fitting
yVals:     the y values for the fitting
eliteNum:  the number of elite individuals to keep per generation
bestN:     the number of best individuals to track over time

OUTPUTS
best: the bestN number of best organisms seen over the course of the GA
fit:  the highest observed fitness value for each iteration
"""
def GA(k, size, numCoeffs, mutRate, xVals, yVals, eliteNum, bestN):
    # initilization
    pop = initPop(size, numCoeffs)
    # get values from the first generation
    pop = accPop(pop, xVals, yVals)
    best = pop[:bestN]
    fit = [pop[0].fitness]

    for i in range(k):
        pop = nextGeneration(pop, numCoeffs, mutRate, eliteNum)
        pop = accPop(pop, xVals, yVals)

        # save the values
        fit.append(pop[0].fitness)
        best = updateBest(best, pop)
        
    return (best,fit)

"""
runScenario will run a given scenario, plot the highest fitness value for each
generation, and return a list of the bestN number of top individuals observed.

INPUTS
scenario: a string to use for naming output files.
--- the remaining inputs are those for the call to GA ---

OUTPUTS
best: the bestN number of best organisms seen over the course of the GA
--- Plots are saved as: 'fit' + scenario + '.png' ---
"""
def runScenario(scenario, k, size, numCoeffs, mutRate, \
                xVals, yVals, eliteNum, bestN):

    # Perform the GA.
    (best,fit) = GA(k, size, numCoeffs, mutRate, xVals, yVals, eliteNum, bestN)

    # Plot the fitness per generation.
    gens = range(k+1)
    plt.figure()
    fig, ax = plt.subplots()
    ax.plot(gens, fit)
    plt.title('Best Fitness per Generation')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.savefig('fit'+scenario+'.png', bbox_inches='tight')
    plt.close('all')

    # Return the best organisms.
    return best

"""
main function
"""
if __name__ == '__main__':

    # Flags to suppress any given scenario. Simply set to False and that
    # scenario will be skipped. Set to True to enable a scenario.
    scenA = False
    scenB = False
    scenC = False
    scenD = True

    if not (scenA or scenB or scenC or scenD):
        print("All scenarios disabled. Set a flag to True to run a scenario.")
    
################################################################################
    ### Scenario A: Fitting to a constant function, y = 1. ###
################################################################################

    if scenA:
        # Create the x values ranging from 0 to 10 with a step of 0.1.
        xVals = [0.1*n for n in range(101)]

        # Create the y values for y = 1 corresponding to the x values.
        yVals = [1. for n in range(len(xVals))]

        # Set the other parameters for the GA.
        sc = 'A'      # Set the scenario title.
        k = 100       # 100 generations for our GA.
        size = 1000   # Population of 1000.
        numCoeffs = 4 # Cubic polynomial.
        mutRate = 0.1 # 10% mutation rate.
        eliteNum = 50 # Keep the top 5% of the population.
        bestN = 5     # track the top 5 seen so far.

        # Run the scenario.
        best = runScenario(sc, k, size, numCoeffs, mutRate, xVals, yVals, \
                           eliteNum, bestN)

        # Print the best individuals.
        print()
        print('Best individuals of Scenario '+ sc +':')
        for org in best:
            print(org)
            print()

    # Observation: 
    # We tried numCoeffs = 1 because we know the answer. However, the final fitness is usually worse than numCoeffs = 4. 

################################################################################
    ### Scenario B: Fitting to a constant function, y = 5. ###
################################################################################
    
    if scenB:
        # Create the x values ranging from 0 to 10 with a step of 0.1.
        xVals = [0.1*n for n in range(101)]

        # Create the y values for y = 1 corresponding to the x values.
        yVals = [5. for n in range(len(xVals))]

        # Set the other parameters for the GA.
        sc = 'B'      # Set the scenario title.
        k = 250       # 250 generations for our GA.
        size = 1000   # Population of 1000.
        numCoeffs = 4 # Cubic polynomial.
        mutRate = 0.1 # 10% mutation rate.
        eliteNum = 50 # Keep the top 5% of the population.
        bestN = 5     # track the top 5 seen so far.

        # Run the scenario.
        best = runScenario(sc, k, size, numCoeffs, mutRate, xVals, yVals, \
                           eliteNum, bestN)

        # Print the best individuals.
        print()
        print('Best individuals of Scenario '+ sc +':')
        for org in best:
            print(org)
            print()

################################################################################
    ### Scenario C: Fitting to a quadratic function, y = x^2 - 1. ###
################################################################################
    
    if scenC:
        # Create the x values ranging from 0 to 10 with a step of 0.1.
        xVals = [0.1*n for n in range(101)]

        # Create the y values for y = x^2 - 1 corresponding to the x values.
        yVals = [x**2-1. for x in xVals]

        # Set the other parameters for the GA.
        sc = 'C'      # Set the scenario title.
        k = 250       # 250 generations for our GA.
        size = 1000   # Population of 1000.
        numCoeffs = 4 # Cubic polynomial.
        mutRate = 0.1 # 10% mutation rate.
        eliteNum = 50 # Keep the top 5% of the population.
        bestN = 5     # track the top 5 seen so far.

        # Run the scenario.
        best = runScenario(sc, k, size, numCoeffs, mutRate, xVals, yVals, \
                           eliteNum, bestN)

        # Print the best individuals.
        print()
        print('Best individuals of Scenario '+ sc +':')
        for org in best:
            print(org)
            print()

################################################################################
    ### Scenario D: Fitting to a quadratic function, y = cos(x). ###
################################################################################
    
    if scenD:
        # Create the x values ranging from -5 to 5 with a step of 0.1.
        xVals = [0.1*n-5 for n in range(101)]

        # Create the y values for y = cos(x) corresponding to the x values.
        yVals = [math.cos(x) for x in xVals]

        # Set the other parameters for the GA.
        sc = 'D'      # Set the scenario title.
        k = 250       # 250 generations for our GA.
        size = 1000   # Population of 1000.
        numCoeffs = 5 # Quartic polynomial with 4 zeros!
        mutRate = 0.1 # 10% mutation rate.
        eliteNum = 50 # Keep the top 5% of the population.
        bestN = 5     # track the top 5 seen so far.

        # Run the scenario.
        best = runScenario(sc, k, size, numCoeffs, mutRate, xVals, yVals, \
                           eliteNum, bestN)

        # Print the best individuals.
        print()
        print('Best individuals of Scenario '+ sc +':')
        for org in best:
            print(org)
            print()

# Observations: 
# We noticed that our algorithm works worse and worse when we get to scenario B, C, and D. It might
# be because there are more coefficients farther away from our starting population (which contains
# four specially created organisms). 