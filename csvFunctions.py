import csv
import GeneticAlgorithm as ga
import pandas as pd
import argparse
import random
import _PyPacwar

# Random genes

def load_gene_pool(filename:str) -> list[ga.Gene]:
    """reads a csv file that is assumed to have a list of genes under header 'gene'.
    Order the gene by their discovered fitness and return the list

    :param str filename: name of the csv file to read
    :return list[ga.Gene]: a list of genes held in the CSV file
    """
    gene_pool = []
    with open(filename, newline='', mode='r') as file:
        csvFile = csv.DictReader(file)
        for rows in csvFile:
            gene_pool.append((ga.Gene(ga.convert_gene_str2list(rows['gene'])), rows['discoveredPoolFitness']))
        gene_pool.sort(reverse=True, key=lambda gene: gene[1])
        # print(gene_pool)
    return [gene[0] for gene in gene_pool]

def experiment(num_generations: int, population_size: int, seeded_population: list[list[int]], elitism_percent: int = .2):
    """run a genetic algorithm experiment and update the result csv

    :param int num_generations: number of generations in the algorithm (how many rounds)
    :param int population_size: number of genes in each generation
    :param list[list[int]] seeded_population: a list of list representations of genes to seed the intial population
    :param int elitism_percent: what percent of the population that you carry over to the next generation, defaults to .2
    """
    # load the current results and add to seeded population
    discovered_gene_pool = load_gene_pool("results.csv")
    # TODO: grab only the elite discovered genes (once 200 or more genes generated, slice discovered)
    seeded_population.extend([gene.gene for gene in discovered_gene_pool])
    num_elite = elitism_percent * population_size
    # create the initial population
    old_population = ga.generate_genes(population_size, seeded_population)
    for i in range(num_generations):
        # clear old fitness scores
        for gene in old_population:
            gene.fitness = 0
        ga.round_robin(old_population)
        # sort in order of fitness, greatest to least
        old_population.sort(key=lambda gene: gene.fitness, reverse=True)
        print(f"Best Gene in round {i}:\nGene: {old_population[0].gene}\nAverage Fitness: {old_population[0].fitness}")
        # take the elite population
        new_population = old_population[:int(num_elite)] # just up to the elite
        # populate the rest of the population with the elite's children (should eventually weight the parent selection)
        while len(new_population) < population_size:
            p1 = new_population[random.randint(0,num_elite - 1)]
            p2 = new_population[random.randint(0,num_elite - 1)]
            child = ga.mate(p1, p2)
            child.mutate()
            new_population.append(child)
        old_population = new_population
    
    gene_dict_list = []
    # calculate all metrics and record into csv file
    for gene in old_population[:10]:
        gene_dict = {}
        gene_dict["gene"] = ga.convert_gene_list2str(gene.gene)
        # gene_dict["experimentalFitness"] = gene.fitness
        gene_dict["discoveredPoolFitness"] = ga.single_vs_population_fitness(gene, discovered_gene_pool)
        gene_dict["allThrees"] = ga.score_simulation(*_PyPacwar.battle(gene.gene, [3] * 50))
        gene_dict["allOnes"] = ga.score_simulation(*_PyPacwar.battle(gene.gene, [1] * 50))
        gene_dict_list.append(gene_dict)

    with open('results.csv', 'a') as csvfile:
        # creating a csv dict writer object
        fields = ['gene', "discoveredPoolFitness", "allThrees", "allOnes"]
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        # writing headers (field names)
        # writer.writeheader()

        # writing data rows
        writer.writerows(gene_dict_list)

def update_discovered_fitness(filename: str):
    df = pd.read_csv(filename)
    discovered_gene_pool = load_gene_pool("results.csv")
    # recalculate the fitness based on discovered gene pool
    # print(df.loc[:, ['gene', 'discoveredPoolFitness']])
    new_fitness = []
    for gene_code in df.loc[:, 'gene']:
        gene = ga.Gene(ga.convert_gene_str2list(gene_code))
        ga.single_vs_population_fitness(gene, discovered_gene_pool)
        new_fitness.append(gene.fitness)
        # print(gene)
    # newFitness = pd.Series([1, 1, 1, 1])
    df['discoveredPoolFitness'] = new_fitness
    # print(df.loc[:, ['gene', 'discoveredPoolFitness']])
    df.to_csv(filename, index=False)
    
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--update", action="store_true")
    parser.add_argument("-r", "--runs", action="store", default=1)
    args = parser.parse_args()
    if(args.update):
        update_discovered_fitness("result.csv")
    else:
        for _ in range(int(args.runs)):
            experiment(num_generations=ga.NUM_GENERATIONS, population_size=ga.POPULATION_SIZE, seeded_population=ga.SEEDED_POPULATION, elitism_percent=0.2)




################# Used to generate our constant gene pool###################

# constant_gene_pool = ga.generate_genes(500) # not seeded
# gene_dict_list = []
# for gene in constant_gene_pool:
#     gene_dict = {}
#     gene_dict["gene"] = ga.convert_gene_list2str(gene.gene)
#     gene_dict_list.append(gene_dict)

# with open('randomGenePool.csv', 'w') as csvfile:
#     # creating a csv dict writer object
#     writer = csv.DictWriter(csvfile, fieldnames=["gene"])

#     # writing headers (field names)
#     writer.writeheader()

#     # writing data rows
#     writer.writerows(gene_dict_list)