import numpy
import ga
import matplotlib.pyplot as plt
import sys

def eda_fixed(laplace, title):
    # Number of the weights we are looking to optimize.
    num_weights = 5

    #Genetic algorithm parameters:
    #    solution per population
    #    Mating pool size
    sol_per_pop = 4
    num_parents_mating = 2

    # optimization target 
    # for this example target is a chromosome with max amount of 1 in each allele
    target = numpy.ones((num_weights))

    # Defining the population size.
    # The population will have sol_per_pop chromosome where each chromosome has num_weights genes.
    pop_size = (sol_per_pop,num_weights) 

    # Creating the initial population
    # for the random example
    new_population = numpy.array([[1,1,0,0,1],[1,1,1,0,1],[0,1,0,1,1],[1,1,0,0,0]])
 ##   print("Starting Population \n",new_population)

    # Number of Generations that need to be calculated
    # each generation selects their parents (#num_parents_mating), calculates a new probability for each allele and generates new children
    num_generations = 6

    return_value = simulation(num_generations, target, new_population, num_parents_mating, pop_size, laplace=laplace, title=title)
    return_value[0] = new_population
    return return_value

def eda_random(num_weight, solutions, num_parents, generations, laplace, bit, title):
    # for testing fix random seed
    # maybe useful for fixed example
    #numpy.random.seed(123)

    # Number of the weights we are looking to optimize.
    num_weights = num_weight

    #Genetic algorithm parameters:
    #    solution per population
    #    Mating pool size
    sol_per_pop = solutions
    num_parents_mating = num_parents

    # optimization target 
    # for this example target is a chromosome with max amount of 1 in each allele
    target = numpy.ones((num_weights))

    # Defining the population size.
    # The population will have sol_per_pop chromosome where each chromosome has num_weights genes.
    pop_size = (sol_per_pop,num_weights) 


    # Creating the initial population
    # for the random example
    # bit = 0 -> random values between 0 and 1
    # bit = 1 -> random values 0 or 1
    if bit == 1:
        new_population = numpy.random.randint(low=0, high=2.0, size=pop_size)
    elif bit == 0:
        new_population = numpy.random.uniform(low=0.0, high=1, size=pop_size)
    else:
        sys.exit("Your selection is not supported, exiting program")
##    print(new_population)

    # Number of Generations that need to be calculated
    # each generation selects their parents (#num_parents_mating), calculates a new probability for each allele and generates new children
    num_generations = generations

    return_value = simulation(num_generations, target, new_population, num_parents_mating, pop_size, laplace, title=title)
    return_value[0] = new_population
    return return_value

def simulation(num_generations, target, population, num_parents_mating, pop_size, laplace, title):
    plot_fitness = numpy.zeros(num_generations)
    return_gen_values = []
    new_population = population
    for generation in range(num_generations):
##        print("\n Generation: ", generation)
        # Measuring the fitness of each chromosome in the population.
        fitness = ga.calculate_pop_fitness(target, new_population)
##        print("Best Fitness this Generation: ", numpy.amax(fitness))

        # Selecting the best parents in the population for mating.
        parents = ga.select_mating_pool(new_population, fitness, num_parents_mating)

        # Generating next generation using crossover.
        new_population = ga.probabilistic(parents, offspring_size=(pop_size), laplace=laplace)

        nsize = int(numpy.size(parents) / pop_size[1])
         ##    print("parents: ", parents)
        if laplace == 0:
            probability_model = ga.probabilistic_model(nsize, parents)
        elif laplace == 1:
            probability_model = ga.probabilistic_model_laplace(nsize,parents)
        else:
            sys.exit("Your selection is not supported, exiting program")
        
        plot_fitness[generation] += numpy.amax(fitness)
        return_gen_values.append([generation, parents, probability_model, numpy.amax(fitness)])

    # Output the best possible Fitness 
    # ∑ target    
##    print("\nTarget Fitness: ", numpy.sum(target))

    # Getting the best solution after iterating finishing all generations.
    # At first, the fitness is calculated for each solution in the final generation.
    fitness = ga.calculate_pop_fitness(target, new_population)
    # Then return the index of that solution corresponding to the best fitness.
    # If more than one solution fits that criteria all found solutions will be presented
    best_match_idx = numpy.where(fitness == numpy.amax(fitness))
##    print("Best solution(s): \n", new_population[best_match_idx, :])

    # quick and clean plot
    # title is defined by the option chosen at the start
    # ylabel reflects the Fitness values
    # xlabel reflects Generation
    # Plot thus shows the fitness for each generation
    #plt.plot(plot_fitness)
    #plt.title(title)
    #plt.ylabel("Fitness")
    #plt.xlabel("Generation")
    #plt.show()


    return_value = []
    return_value.append(new_population)
    return_value.append(return_gen_values)
    return_value.append(numpy.sum(target))
    return_value.append(new_population[best_match_idx, :])
    return_value.append(plot_fitness)
    # calculation for the best fitness in the final population
    return_value.append(numpy.amax(plot_fitness))
##  print("Best solution fitness : ", fitness[best_match_idx].max())

    return return_value
 

