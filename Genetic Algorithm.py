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
            if random.random() < .02:
                self.gene[i] = GENES[random.randint(0,3)]

def mate(parent1: Gene, parent2: Gene) -> Gene:
    """generate offspring from parent1 and parent 2

    :param Gene parent1: the first parent to derive the genome from
    :param Gene parent2: the second parent to derive the genome from
    """

    # break points in gene -> 1-4; 5-20;                   (4bit)
    #                         21-23; 24-26; 27-38; 39-50   (3bit)             


def generate_genes(num_genes) -> list[Gene]:
        """generates a list of gene sequences

        :return list[gene]: a list of randomly generated genes
        """
        gene_list = []
        for _ in range(num_genes):
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
    num_rounds = (len(genes) - 1) * len(genes) / 2
    for gene in genes:
        gene.fitness /= num_rounds
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
    gene_list = generate_genes(POPULATION_SIZE)
    ones = [1] * 50
    threes = [3] * 50
    print("Example Python module in C for Pacwar")
    print("all ones versus all threes ...")
    (rounds, c1, c2) = _PyPacwar.battle(ones, threes)
    print("Number of rounds:", rounds)
    print("Ones PAC-mites remaining:", c1)
    print("Threes PAC-mites remaining:", c2)

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", action="store_true")
    args = parser.parse_args()
    # run command with -t to run test, run without to run main
    if (args.test):
        test()
    else:
        main()