import _PyPacwar
import argparse
import numpy
import random

def convert_gene_str2list(gene: str) -> list[int]:
    """takes a string representing a gene and converts it to its list equivalent

    :param str gene: a string representing a gene
    :return list[int]: the list representation of the inputted gene
    """
    converted_gene =[]
    for nucleotide in gene:
        converted_gene.append(int(nucleotide))
    return converted_gene

def convert_gene_list2str(gene: list[int]) -> str:
    """ takes a list of integers representing a gene and 
        condenses it into a string of integers that can be ported 
        into the pacwar simulation

    :param str gene: a printed list of strings representing a gene
    :return str: the condensed string of integers representing a gene
    """
    return "".join([str(x) for x in gene])

# valid genes
GENES = [0,1,2,3]
# length of a gene
GENE_LENGTH = 50
# population size
POPULATION_SIZE = 200
# number of generations
NUM_GENERATIONS = 10
# seeded genes
SEEDED_POPULATION = [[1]*50, [3]*50]
# adding best genes to seeded population
SEEDED_POPULATION.append(convert_gene_str2list("10111111111111111111111111111111111111111211111311"))

class Gene():
    # mutation rate
    mutation_rate = .08
    def __init__(self, genome: list[int] = None):
        """Gene Class initializer

        :param list[int] genome: a list of strings representing a gene,
                                 must be of length GENE_LENGTH, defaults to None
        """
        if genome:
            assert(len(genome) == GENE_LENGTH)
            self.gene = genome
        else:
            self.gene = self.generate_genome()
        self.fitness = 0

    def generate_genome(self) -> list[int]:
        """generates a gene sequence

        :return list[int]: a list of each individual gene
        """
        gene = []
        for _ in range(GENE_LENGTH):
            r = random.randrange(4)
            gene.append(GENES[r])
        
        return gene
    
    def mutate(self):
        """mutates each gene with a 2% chance (has a chance to mutate into itself, so true mutation rate is 1.5%)
        """
        for i in range(GENE_LENGTH):
            if random.random() < self.mutation_rate:
                self.gene[i] = GENES[random.randint(0,3)]
    
    def decrease_mutation(self):
        self.mutation_rate *= 0.9

def mate(parent1: Gene, parent2: Gene) -> Gene:
    """generate offspring from parent1 and parent 2
       current crossover scheme is 50/50 at some break between genes U, V, W, X, Y, Z

    :param Gene parent1: the first parent to derive the genome from
    :param Gene parent2: the second parent to derive the genome from
    """

    # break points in gene -> 1-4; 5-20;                   (4bit)
    #                         21-23; 24-26; 27-38; 39-50   (3bit)   
    breakpoints = [4,20,23,26,38] 
    flip_point = breakpoints[random.randint(0,4)]
    flip_order = random.randint(0,1)

    new_genome = [-1] * 50
    new_genome[0:flip_point] = parent1.gene[0:flip_point] if flip_order == 0 else parent2.gene[0:flip_point]
    new_genome[flip_point:] = parent2.gene[flip_point:] if flip_order == 0 else parent1.gene[flip_point:]

    # old cross over scheme flipping each gene
    
    # new_genome[0:4] = parent1.gene[0:4] if random.random() < .5 else parent2.gene[0:4]
    # new_genome[4:20] = parent1.gene[4:20] if random.random() < .5 else parent2.gene[4:20]
    # new_genome[20:23] = parent1.gene[20:23] if random.random() < .5 else parent2.gene[20:23]
    # new_genome[23:26] = parent1.gene[23:26] if random.random() < .5 else parent2.gene[23:26]
    # new_genome[26:38] = parent1.gene[26:38] if random.random() < .5 else parent2.gene[26:38]
    # new_genome[38:50] = parent1.gene[38:50] if random.random() < .5 else parent2.gene[38:50]         
    return Gene(new_genome)

def generate_genes(num_genes: int, preset_genes: list[list[int]] = []) -> list[Gene]:
    """generates a list of gene sequences

    :param int num_genes: the number of genes to be generated
    :param list[list[int]] preset_genes: a list of integer lists representing genes to seed the population with
    :return list[gene]: a list of seeded and randomly generated genes
    """
    gene_list = []
    # convert the seeded gene list into actual Gene objects
    for i in range(len(preset_genes)):
        gene = Gene(preset_genes[i])
        gene_list.append(gene)
    # generate the rest of the desired number of genes randomly
    for _ in range(num_genes - len(preset_genes)):
        gene = Gene()
        gene_list.append(gene)
    
    return gene_list

# simulates round robin competition between genes in list
# returns percentage of wins for each placement
def round_robin(genes: list[Gene]):
    """makes a round robin competition between every genome in genes

    :param list[Gene] genes: list of genomes to test
    :return None:
    """
    for i in range(len(genes) - 1):
        for j in range(i+1, len(genes)):
            (rounds, c1, c2) = _PyPacwar.battle(genes[i].gene, genes[j].gene)
            score = score_simulation(rounds, c1, c2)
            if score > 0:
                genes[i].fitness += score
                genes[j].fitness += 1 - score
            else:
                genes[i].fitness += 1 + score
                genes[j].fitness += -1 * score
    for gene in genes:
        gene.fitness /= (len(genes) - 1)
    return

def single_vs_population_fitness(gene: Gene, population: list[Gene]):
    gene.fitness = 0
    for i in range(len(population)):
        (rounds, c1, c2) = _PyPacwar.battle(gene.gene, population[i].gene)
        score = score_simulation(rounds, c1, c2)
        if score > 0:
            gene.fitness += score
        else:
            gene.fitness += 1 + score
    gene.fitness /= len(population)
    return gene.fitness


def score_simulation(rounds, c1, c2) -> float:
    """scores the results of a PyPacwar battle

    :param _type_ rounds: number of rounds in the simulate
    :param _type_ c1: ending population of the c1 genome
    :param _type_ c2: ending population of the c2 genome
    :return float: return scoring (proportional to 1) based on the PacWar specifications, 
                   it will be negative if c2 wins examples: 10-10 --> .5, 7-13 --> -13/20, 20-0 --> 1
    """
    score = 0 # higher score is better
    # checks if c1 or c2 wins
    c1_wins = 1 if c1 >= c2 else -1

    # checking if the simulation ended in a population completely winning
    if (rounds < 500):
        if (rounds >= 300):
            score = 17/20
        elif(rounds >= 200):
            score = 18/20
        elif(rounds >= 100):
            score = 19/20
        else:
            score = 1
    elif(c1 == 0 or c2 == 0): # covers the case of a population being wiped out on the 500th round
        score = 17/20
    else: # if there is remaining populations in both c1 and c2
        ratio = 1        
        if (c1_wins == 1):
            ratio = c1 / c2
        else:
            ratio = c2 / c1
        if ratio >= 10:
            score = 13/20
        elif ratio >= 3:
            score = 12/20
        elif ratio >= 1.5:
            score = 11/20
        else:
            score = .5

    score *= c1_wins
    return score
    
# Example Python module in C for Pacwar
# https://www.geeksforgeeks.org/genetic-algorithms/
def main():
    elitism_percent = .2
    num_elite = elitism_percent * POPULATION_SIZE
    # seed the initial population with all 1 and all 3 genes
    test = Gene([1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 3, 1, 1])
    
    yesterday = Gene(convert_gene_str2list("10111111111111111111111111111111111111111211111311"))
    (rounds, c1, c2) = _PyPacwar.battle(test.gene, [1] * 50)
    print("for all 1's: ", "rounds; ", rounds, "c1", c1, "c2", c2)
    (rounds, c1, c2) = _PyPacwar.battle(test.gene, [3] * 50)
    print("for all 3's: ", "rounds; ", rounds, "c1", c1, "c2", c2)
    (rounds, c1, c2) = _PyPacwar.battle(test.gene, yesterday.gene)
    print("for the one yestrday", "rounds; ", rounds, "c1", c1, "c2", c2)
    # (rounds, c1, c2) = _PyPacwar.battle(yesterday.gene, )


    

    old_population = generate_genes(POPULATION_SIZE, SEEDED_POPULATION)
    for i in range(NUM_GENERATIONS):
        # clear old fitness scores
        
        for gene in old_population:
            gene.fitness = 0
        round_robin(old_population)
        # sort in order of fitness, greatest to least
        old_population.sort(key=lambda gene: gene.fitness, reverse=True)
        print(f"Best Gene in round {i}:\nGene: {old_population[0].gene}\nAverage Fitness: {old_population[0].fitness}")
        # take the elite population
        new_population = old_population[:int(num_elite)] # just up to the elite
        # populate the rest of the population with the elite's children (should eventually weight the parent selection)
        while len(new_population) < POPULATION_SIZE:
            p1 = new_population[random.randint(0,num_elite - 1)]
            p2 = new_population[random.randint(0,num_elite - 1)]
            child = mate(p1, p2)
            child.mutate()
            child.decrease_mutation()
            new_population.append(child)
        old_population = new_population
        
    
    # show top 3 genes after generations
    for i in range(3):
        print(f"{i + 1}th Best Gene after Experiment:\nGene: {old_population[i].gene}\nAverage Fitness: {old_population[i].fitness}")

def test():
    # check generate_genes
    genes = generate_genes(4)
    # print(genes)
    assert(len(genes) == 4)
    assert([len(genome.gene) for genome in genes] == [50] * 4)

    # check score_simulation
    assert(score_simulation(10, 0, 100) == -1)
    assert(score_simulation(101, 0, 100) == -19/20)
    assert(score_simulation(201, 10, 0) == 18/20)
    assert(score_simulation(301, 10, 0) == 17/20)
    assert(score_simulation(500, 0, 100) == -17/20)

    assert(score_simulation(500, 10, 100) == -13/20)
    assert(score_simulation(500, 33, 100) == -12/20)
    assert(score_simulation(500, 1.5, 1) == 11/20)
    assert(score_simulation(500, 100, 100) == 10/20)

    # check round robin
    round_robin(genes)
    # print(results)
    assert(sum([gene.fitness for gene in genes]) == 1)

    # check mating pattern
    parent1 = Gene([0]*50)
    parent2 = Gene([1]*50)
    offspring = mate(parent1, parent2)
    print("Crossover of all 1's and all 0's\n" + offspring.gene)



def condense(gene: str) -> str:
    """ takes a printed list of strings representing a gene and 
        condenses it into a sequence of integers that can be ported 
        into the pacwar simulation

    :param str gene: a printed list of strings representing a gene
    :return str: the condensed string of integers representing a gene
    """
    clean_gene = ""
    for char in gene:
        if char.isdigit():
            clean_gene += char
    return clean_gene

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", action="store_true")
    parser.add_argument("-c", "--condense", action="store")
    args = parser.parse_args()
    # run command with -t to run test, run without to run main
    if (args.test):
        test()
    elif (args.condense):
        condensed = condense(args.condense)
        print(condensed)
        # print(convert_gene_str2list(condensed))
    else:
        main()
