import _PyPacwar
import argparse
import numpy
import random

# valid genes
GENES = [0,1,2,3]
# length of a gene
GENE_LENGTH = 50
# population size
POPULATION_SIZE = 100

class Gene():
    mutation_rate = .2 # will decrease
    def __init__(self, genome: list[str] = None):
        """Gene Class initializer

        :param list[str] genome: a list of strings representing a gene,
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
            gene.append(str(GENES[r]))
        
        return gene
    
    def mutate(self):
        """mutates each gene with a 2% chance (has a chance to mutate into itself, so true mutation rate is 1.5%)
        """
        for i in range(GENE_LENGTH):
            if random.random() < Gene.mutation_rate:  # 10% chance
                self.gene[i] = str(GENES[random.randint(0,3)])

def mate(parent1: Gene, parent2: Gene) -> Gene:
    """generate offspring from parent1 and parent 2
       current crossover scheme is 50/50 for each gene U, V, W, X, Y, Z

    :param Gene parent1: the first parent to derive the genome from
    :param Gene parent2: the second parent to derive the genome from
    """

    # break points in gene -> 1-4; 5-20;                   (4bit)
    #                         21-23; 24-26; 27-38; 39-50   (3bit)    
    new_genome = [-1] * 50
    new_genome[0:4] = parent1.gene[0:4] if random.random() < .5 else parent2.gene[0:4]
    new_genome[4:20] = parent1.gene[4:20] if random.random() < .5 else parent2.gene[4:20]
    new_genome[20:23] = parent1.gene[20:23] if random.random() < .5 else parent2.gene[20:23]
    new_genome[23:26] = parent1.gene[23:26] if random.random() < .5 else parent2.gene[23:26]
    new_genome[26:38] = parent1.gene[26:38] if random.random() < .5 else parent2.gene[26:38]
    new_genome[38:50] = parent1.gene[38:50] if random.random() < .5 else parent2.gene[38:50]         
    return Gene(new_genome)

def generate_genes(num_genes) -> list[Gene]:
    """generates a list of gene sequences

    :return list[gene]: a list of randomly generated genes
    """
    gene_list = []
    for _ in range(num_genes - (4 + 1)):
        gene = Gene()
        gene_list.append(gene)

    def gen_specific_len_genome(num: int)->list[int]:
        gene = []
        # for _ in range(num):
        #     r = random.randrange(4)
        #     gene.append(str(GENES[r]))
        # print("Gene", gene)
        gene = ['3'] * num
        return gene
    
    # u(4), v(16), w(3), x(3), y(12), z(12)
    best_U = ['3','3','0','0']
    best_U.extend(gen_specific_len_genome(50-4))
    gene = Gene()
    gene.gene = best_U
    print("len U: ", len(gene.gene))
    gene_list.append(gene)
    print("best_U", best_U)

    best_X = gen_specific_len_genome(4+16+3)
    best_X.extend(['2','2','2'])
    best_X.extend(gen_specific_len_genome(12+12))
    gene = Gene()
    gene.gene = best_X
    gene_list.append(gene)
    print("len X: ", len(gene.gene))
    print("Best_X", best_X)

    best_W = gen_specific_len_genome(4+16)
    best_W.extend(['2','2','2'])
    best_W.extend(gen_specific_len_genome(3+12+12))
    gene = Gene()
    gene.gene = best_W
    print("len W: ", len(gene.gene))
    gene_list.append(gene)


    Z_gene = ['1','1','1','0','0','0','0','0','0','0','0','0']
    best_Z = gen_specific_len_genome(4+16+3+3+12)
    best_Z.extend(Z_gene)
    gene = Gene()
    gene.gene = best_Z
    gene_list.append(gene)
    print("len Z: ", len(gene.gene))
    print("".join(gene.gene), "YAS")

    # U+X also won

    # from_other_rounds = [['0', '0', '0', '0', '0', '1', '0', '1', '2', '1', '1', '0', '2', '2', '2', '2', '3', '3', '3', '2', '1', '1', '2', '1', '1', '1', '1', '1', '3', '3', '2', '1', '1', '2', '2', '3', '2', '3', '3', '1', '2', '1', '0', '2', '2', '3', '2', '3', '3', '3'],
    #                      ]

    # for g in from_other_rounds:
    #     gene = Gene()
    #     gene.gene = g
    #     gene_list.append(gene)

    
    # add all ones and all threes
    gene = Gene()
    threes = ['3'] * 25
    ones = []
    gene.gene = ['3'] * 25 
    # gene_list.append(gene)
    # gene = Gene()
    # gene.gene = ['1'] * 50
    # gene_list.append(gene)
    
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
    num_rounds = (len(genes) - 1) * len(genes) / 2
    for gene in genes:
        gene.fitness /= POPULATION_SIZE
    return

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

    if rounds == 500 and c1_wins == 1:  # so we win
        score += 100 # massively inflate score
    if rounds < 500 and c1_wins == 1:
        score += 1000
    if rounds == 500:
        score += 50 # pretty good

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
    test = Gene()
    test.gene = ['3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0']
    # Average Fitness: 0.9770000000000003
    threes = ['3'] * 50
    (rounds, c1, c2) = _PyPacwar.battle(test.gene, threes)
    print("TESTbattle: rounds: ", rounds, c1, "-", c2)

    generate_top_three_genes()

def generate_top_three_genes():
    elitism_percent = .2
    num_elite = elitism_percent * POPULATION_SIZE
    num_generations = 100

    old_population = generate_genes(POPULATION_SIZE)
    for i in range(num_generations):
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
            child.mutation_rate *= 0.6 # so decrease mutation rate every time
            new_population.append(child)
        old_population = new_population
        
    
    # show top 3 genes after generations
    threes = ['3'] * 50
    for i in range(3):
        print(f"{i}th Best Gene after Experiment:\nGene: {old_population[0].gene}\nAverage Fitness: {old_population[0].fitness}")
        (rounds, c1, c2) = _PyPacwar.battle(old_population[i].gene, threes)
        print("battle: rounds: ", rounds, c1, "-", c2)


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", action="store_true")
    args = parser.parse_args()
    # run command with -t to run test, run without to run main
    if (args.test):
        test()
    else:
        main()