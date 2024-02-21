import csv
import GeneticAlgorithm as ga

# Random genes

def load_constant_gene_pool() -> list[list[int]]:
    gene_pool = []
    with open("randomGenePool.csv", newline='', mode='r') as file:
        csvFile = csv.DictReader(file)
        for rows in csvFile:
            gene_pool.append(ga.convert_gene_str2list(rows['gene']))
    return gene_pool

if __name__ == "__main__":
    load_constant_gene_pool()




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