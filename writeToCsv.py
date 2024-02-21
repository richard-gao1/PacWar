import csv
import GeneticAlgorithm as ga

# Random genes


if __name__ == "__main__":
    constant_gene_pool = ga.generate_genes(500) # not seeded
    gene_dict_list = []
    for gene in constant_gene_pool:
        gene_dict = {}
        gene_dict["gene"] = ga.convert_gene_list2str(gene.gene)
        gene_dict_list.append(gene_dict)

    with open('randomGenePool.csv', 'w') as csvfile:
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames=["gene"])
    
        # writing headers (field names)
        writer.writeheader()
    
        # writing data rows
        writer.writerows(gene_dict_list)