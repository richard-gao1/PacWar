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
            r = random.randrange(3)
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
    # checking if the simulation ended in a population completely winning
    if (rounds < 500):
        # checks if c1 or c2 wins
        c1_wins = 1 if c1 > c2 else -1
        if (rounds >= 300):
            score = 17/20
        elif(rounds >= 200):
            score = 18/20
        elif(rounds >= 100):
            score = 19/20
        else:
            score = 1
        score *= c1_wins
    else: 
        


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


if __name__ == "__main__":
    main()
