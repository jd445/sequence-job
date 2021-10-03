import pandas
from gensim.models import *
import numpy
def DNA_to_array(DNA, module):
    DNA_array = []
    sum = 0
    for i in DNA:
        for j in i:
            sum = sum + module.wv[j]
        DNA_array.append(sum)
    return numpy.array(DNA_array)
def k_mergenerator(WaiTingKmer, k ,name):
    result = open("{}.txt".format(name), mode="w")
    DNA = []
    for i in WaiTingKmer:
        line = []
        for j in range(len(i)-k+1):
            line.append(i[j:j+k])
            result.write(i[j:j+k])
            result.write(" ")
        DNA.append(line)
        result.write("\n")
    return DNA
if __name__ == '__main__':

    '''import the rna_dataset'''
    rna_data = {}
    rna = []
    mirna = pandas.read_csv("mirna_seq.csv",header=0)
    mirna = mirna.values.tolist()
    for i in mirna:
        i = str(i).replace("'","").replace("\\n","").replace("[","").replace("]","").replace(" ","").replace("\\r","")
        rna_data.update({i.split(",")[0].replace(" ",""):i.split(",")[1].replace(" ","")})
        rna.append(i.split(",")[1].replace(" ",""))

    '''import the gene_dataset'''
    gene_data = {}
    dna = []
    gene = pandas.read_csv("gene_seq.csv",header=0)
    gene = gene.values.tolist()
    for i in gene:
        i = str(i).replace("'","").replace("\\n","").replace("[","").replace("]","").replace(" ","").replace("\\r","")
        gene_data.update({i.split(",")[0].replace(" ",""):i.split(",")[1].replace(" ","")})
        dna.append(i.split(",")[1].replace(" ",""))

    '''generate the txt file for rna and dna'''
    rna_kmer = k_mergenerator(rna,3,"rna")
    dna_kmer = k_mergenerator(dna,3,"dna")

    '''transfer rna and dna to vector'''
    genes = word2vec.Text8Corpus("dna.txt")
    gene_model = word2vec.Word2Vec(genes, sg=1, min_count=1, vector_size=50)
    print(gene_model)
    gene_model.wv.save_word2vec_format("dna_vec", binary=False)

    rnas = word2vec.Text8Corpus("rna.txt")
    rna_model = word2vec.Word2Vec(rnas, sg=1, min_count=1, vector_size=50)
    print(rna_model)
    rna_model.wv.save_word2vec_format("rna_vec", binary=False)
    '''import trandata'''
    tran_dna_name = []
    tran_rna_name = []
    tran_label = []
    trandata = pandas.read_csv("Train.csv",header=1)
    trandata = trandata.values.tolist()
    for i in trandata:
        i = str(i).replace("'","").replace("\\n","").replace("[","").replace("]","")
        tran_dna_name.append(i.split(",")[0].replace(" ",""))
        tran_rna_name.append(i.split(",")[1].replace(" ",""))
        tran_label.append(i.split(",")[2].replace(" ",""))
    tran_dna = []
    tran_rna = []
    for i in tran_dna_name:
        tran_dna.append(gene_data[i])
    for i in tran_rna_name:
        tran_rna.append(rna_data[i])
    file = open('label.txt','w')
    for i in tran_label:
        file.write(str(i))
        file.write("\n")
    file.close()
    tran_label = numpy.array(tran_label)

    '''generate vector for sequence'''
    tran_dna_kmer = k_mergenerator(tran_dna,3,"kkjj")
    tran_rna_kmer = k_mergenerator(tran_rna,3,"kkjj")
    DNAarray = DNA_to_array(tran_dna_kmer, gene_model)
    RNAarray = DNA_to_array(tran_rna_kmer, rna_model)
    print(RNAarray.shape,DNAarray.shape)
    Big_array = numpy.hstack((RNAarray,DNAarray))
    # 70 准确率，但是偏心
    # Big_array = RNAarray + DNAarray

    '''save as txt'''
    numpy.savetxt("DNAarray.txt",DNAarray)
    numpy.savetxt("RNAarray.txt",RNAarray)
    numpy.savetxt("Big_array.txt",Big_array)
    '''tran, using svm'''
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(Big_array,tran_label,test_size=0.3)
    from sklearn.svm import SVC
    svmclass = SVC(kernel="rbf")
    print(len(X_train),len(y_train))
    svmclass.fit(X_train,y_train)
    res = svmclass.predict(X_test)
    import sklearn.metrics as sm
    bg = sm.classification_report(y_test, res)
    SB = sm.confusion_matrix(y_test,res)
    print(SB)
    # for i in range(len(y_test)):
    #     print(y_test[i],res[i])
    print('分类报告：', bg, sep='\n')




