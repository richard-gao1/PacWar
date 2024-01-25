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
    
# Example Python module in C for Pacwar
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
