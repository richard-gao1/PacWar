import _PyPacwar
import numpy
import random

GENES = [0,1,2,3]

# intially generates num_genes randomly
def generate_genes(num_genes: int) -> list:
    generated = []
    for _ in range(num_genes):
        gene = ""

        for _ in range(50):
            r = random.randrange(4)
            gene += str(GENES[r])
        
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
            
            
    results = []

# scores a simulation - proportional to 100 - 10:10 --> .5, 20-0 --> 1
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

    num_genes = 50
    gene_list = generate_genes(num_genes)
    ones = [1] * 50
    threes = [3] * 50
    print("Example Python module in C for Pacwar")
    print("all ones versus all threes ...")
    (rounds, c1, c2) = _PyPacwar.battle(ones, threes)
    print("Number of rounds:", rounds)
    print("Ones PAC-mites remaining:", c1)
    print("Threes PAC-mites remaining:", c2)

def test():
    genes = generate_genes(4)
    print(genes)

    assert(score_simulation(10, 0, 100) == -1)
    assert(score_simulation(101, 0, 100) == -19/20)
    assert(score_simulation(201, 10, 0) == 18/20)
    assert(score_simulation(301, 10, 0) == 17/20)
    assert(score_simulation(500, 0, 100) == -17/20)

    assert(score_simulation(500, 10, 100) == -13/20)
    assert(score_simulation(500, 33, 100) == -12/20)
    assert(score_simulation(500, 1.5, 1) == 11/20)
    assert(score_simulation(500, 100, 100) == 10/20)


if __name__ == "__main__":
    # main()
    test()