import _PyPacwar
import argparse
import numpy
import random

GENES = [0,1,2,3]

# intially generates num_genes randomly
def generate_genes(num_genes: int) -> list:
    generated = []
    for _ in range(num_genes):
        gene  = ['3','3','0','0']

        for _ in range(46):
            r = random.randrange(4)
            gene.append(str(GENES[r]))
        
        generated.append(gene)
    
    return generated

# simulates round robin competition between genes in list
# returns percentage of wins for each placement
def round_robin(genes: list[int]) -> list[float]:
    results = [0] * len(genes)
    for i in range(len(genes) - 1):
        for j in range(i+1, len(genes)):
            (rounds, c1, c2) = _PyPacwar.battle(genes[i], genes[j])
            score = score_simulation(rounds, c1, c2)

            results[i] = results[i] + score if score > 0 else results[i] + (1 + score)
            results[j] = results[j] + (1 - score) if score > 0 else results[j] +(-1 * score)
            # if score > 0:
            #     results[i] += score
            #     results[j] += 1 - score
            # else:
            #     results[i] += 1 + score
            #     results[j] += -1 * score
    num_rounds = (len(genes) - 1) * len(genes) / 2
    results = [n/num_rounds for n in results]
    return results

# scores both populations in a simulation proportional to 1, if c2 is the winner, the score will be negative
# 10-10 --> .5, 7-13 --> -13/20, 20-0 --> 1
def score_simulation(rounds, c1, c2) -> float:
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
    ones = [1] * 50
    threes = [3] * 50

    best_genes = [] # each elem is a tuple of the gene in list form and str form
    for _ in range(5):
        best_genes.append(find_optimal_gene())
    # temp = [3,3,0,0]
    # temp2 = [3] * (50-4)
    # temp.extend(temp2)
    # best_genes.append((temp,33003333333333333333333333333333333333333333333333))
    # print('\n'.join([str(item[1]) for item in best_genes]))

    for gene_list, gene_str in best_genes:
        print("testing gene: ", gene_str)

        print("versus all ones ...")
        (rounds, c1, c2) = _PyPacwar.battle(gene_list, ones)
        print("Number of rounds:", rounds)
        print("test remaining:", c1, "Ones PAC-mites remaining:", c2)
        print()

        print("versus all threes ...")
        (rounds, c1, c2) = _PyPacwar.battle(gene_list, threes)
        print("Number of rounds:", rounds)
        print("test remaining:", c1, "Threes PAC-mites remaining:", c2)

def find_optimal_gene():
    num_genes = 100
    gene_list = generate_genes(num_genes) # list of all 50 genes
    # print(gene_list)
    temp = ['3','3','0','0']
    temp2 = ['3'] * (50-4)
    temp.extend(temp2)
    # gene_list.append("33003333333333333333333333333333333333333333333333")
    gene_list.append(temp)

    results = round_robin(gene_list)
    # print(results)
    max_result = max(results)
    # print("best score: ", max_result)
    best_gene = "".join(gene_list[results.index(max_result)])
    # print("best gene: ", gene_list[results.index(max_result)])
    # print("best_gene: ", best_gene)
    return (gene_list[results.index(max_result)], best_gene)


def test():
    # check generate_genes
    genes = generate_genes(4)
    assert(len(genes) == 4)
    assert([len(gene) for gene in genes] == [50] * 4)

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
    results = round_robin(genes)
    # print(results)
    assert(sum(results) == 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", action="store_true")
    args = parser.parse_args()
    # run command with -t to run test, run without to run main
    if (args.test):
        test()
        print("done with test")
    else:
        main()