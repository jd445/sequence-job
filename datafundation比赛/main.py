import pandas
from gensim.models import *


def k_mergenerator(WaiTingKmer, k,name):
    result = open("{}.txt".format(name), mode="w")
    for i in WaiTingKmer:
        line = []
        for j in range(len(i)-k+1):
            line.append(i[j:j+k])
            result.write(i[j:j+k])
            result.write(" ")
        result.write("\n")
if __name__ == '__main__':

    '''import the rna_dataset'''
    rna_data = {}
    rna = []
    mirna = pandas.read_csv("mirna_seq.csv",header=1)
    mirna = mirna.values.tolist()
    for i in mirna:
        i = str(i).replace("'","").replace("\\n","").replace("[","").replace("]","")
        rna_data.update({i.split(",")[0]:i.split(",")[1]})
        rna.append(i.split(",")[1])

    '''import the gene_dataset'''
    gene_data = {}
    dna = []
    gene = pandas.read_csv("gene_seq.csv",header=1)
    gene = gene.values.tolist()
    for i in gene:
        i = str(i).replace("'","").replace("\\n","").replace("[","").replace("]","")
        gene_data.update({i.split(",")[0]:i.split(",")[1]})
        dna.append(i.split(",")[1])

    '''generate the txt file for rna and dna'''
    k_mergenerator(rna,3,"rna")
    k_mergenerator(dna,3,"dna")

    '''transfer rna and dna to vector'''
    genes = word2vec.Text8Corpus("dna.txt")
    gene_model = word2vec.Word2Vec(genes, sg=1, min_count=1, vector_size=100)
    print(gene_model)
    gene_model.wv.save_word2vec_format("dna_vec", binary=False)

    rna = word2vec.Text8Corpus("rna.txt")
    rna_model = word2vec.Word2Vec(genes, sg=1, min_count=1, vector_size=100)
    print(rna_model)
    rna_model.wv.save_word2vec_format("rna_vec", binary=False)
    '''import trandata'''
    
