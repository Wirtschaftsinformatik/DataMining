import numpy
import sys

# -- some usefull outputs in the comments with ##

def calculate_pop_fitness(equation_inputs, pop):
    # Calculating the fitness value of each solution in the current population.
    # The fitness function caulcuates the sum of products between each input and its corresponding weight.
    fitness = numpy.sum(pop*equation_inputs, axis=1)
    return fitness

def select_mating_pool(pop, fitness, num_parents):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    parents = numpy.zeros((num_parents, pop.shape[1]))
    for parent_num in range(num_parents):
        max_fitness_idx = numpy.where(fitness == numpy.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_num, :] = pop[max_fitness_idx, :]
        fitness[max_fitness_idx] = 0
    return parents

def probabilistic_model(nsize, parents):
    # 1d ndarray in form (size) of parents filled with zeros
    probability_model = numpy.zeros_like(parents[0])

    # calculating the probability model
    # distribution for this problem: 1/n ∑ x ==> 1/#parents ∑ chromosome aller parents
    # probabilistic model return a 1d nd array with probabilitys ranging from 0 to 1 for each allele 
    for k in range(nsize):
        probability_model += parents[k]
    probability_model /= nsize
    print("probability_model: ", probability_model)
    return probability_model

def probabilistic_model_laplace(nsize, parents):
    # 1d ndarray in form (size) of parents filled with ones for laplace correction
    # other option would be to make a 1d ndarray filled with zeros and add a imaginary parent filled with ones
    probability_model = numpy.ones_like(parents[0])

    # calculating the probability model
    # distribution for this problem: 1/n+1 ∑ x ==> 1/#parents ∑ chromosome aller parents + 1 for the added laplace vector
    # probabilistic model return a 1d nd array with probabilitys ranging from 0 to 1 for each allele 
    for k in range(nsize):
        probability_model += parents[k]
    probability_model /= nsize+1
##    print("probability_model: ", probability_model)
    return probability_model

def probabilistic(parents, offspring_size, laplace):
    # calculating amount of parents
    nsize = int(numpy.size(parents) / offspring_size[1])
    # 2d ndarray (pop_size - parents x #chromosome) for the new population filled with zeros 
    new_population = numpy.zeros((offspring_size[0], offspring_size[1]))
    # 1d ndarray (#chromosome) for the childs that get calculated via the probabilistic_model 
    child = numpy.empty(offspring_size[1])
    # 1d ndarray in form (size) of parents filled with zeros
    probability_model = numpy.zeros_like(parents[0])
##    print("parents: ", parents)
    if laplace == 0:
        probability_model = probabilistic_model(nsize, parents)
    elif laplace == 1:
        probability_model = probabilistic_model_laplace(nsize,parents)
    else:
        sys.exit("Your selection is not supported, exiting program")

    # calculate new children based on the probabilistic model
    # for a new child chromosome each allele (0 or 1) will be randomly generated using the corresponding allele probability
    # after each allele loop exists a new child with replaces a zero value in the new_population
    for pop_size in range(offspring_size[0]):
        for allele in range(offspring_size[1]):
            probability_model[allele]
            probability = [1-probability_model[allele],probability_model[allele]]
##            print("probability : ",allele, probability)
            child[allele] = numpy.random.choice(2,1, p=probability)
        new_population[pop_size] += child
##       print("child:_", child)
##    print("new_population: ", new_population)
    return new_population
