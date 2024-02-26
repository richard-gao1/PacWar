import csv
import GeneticAlgorithm as ga
import random
import _PyPacwar

# Random genes

def load_constant_gene_pool() -> list[ga.Gene]:
    gene_pool = []
    with open("randomGenePool.csv", newline='', mode='r') as file:
        csvFile = csv.DictReader(file)
        for rows in csvFile:
            gene_pool.append(ga.Gene(ga.convert_gene_str2list(rows['gene'])))
    return gene_pool

def experiment(num_generations: int, population_size: int, seeded_population: list[list[int]], elitism_percent: int = .2):
    constant_gene_pool = load_constant_gene_pool()
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
        gene_dict["constantPoolFitness"] = ga.single_vs_population_fitness(gene, constant_gene_pool)
        gene_dict["allThrees"] = ga.score_simulation(*_PyPacwar.battle(gene.gene, [3] * 50))
        gene_dict["allOnes"] = ga.score_simulation(*_PyPacwar.battle(gene.gene, [1] * 50))
        gene_dict_list.append(gene_dict)

    with open('results.csv', 'a') as csvfile:
        # creating a csv dict writer object
        fields = ['gene', "constantPoolFitness", "allThrees", "allOnes"]
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        # writing headers (field names)
        # writer.writeheader()

        # writing data rows
        writer.writerows(gene_dict_list)

if __name__ == "__main__":
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