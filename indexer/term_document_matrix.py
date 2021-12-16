from . tokenizer import Tokenizer
from dataclasses import dataclass
from scipy.sparse import spmatrix
from . document_collection import DocumentCollection
from math import log10, sqrt
import os
from collections import Counter



@dataclass
class TermDocumentMatrix:
    tokenizer: Tokenizer
    documentCollection: DocumentCollection
    matrix: spmatrix

    ##############
    # Construction
    ##############

    def __init__(self, tokenizer, documentCollection):
        self.tokenizer = tokenizer
        self.documentCollection = documentCollection
        self.computeMatrix()


    def computeMatrix(self, query, document):
        alluniquewordsDocs = Counter()
        alluniquewordsQuery = Counter()
        queryWordsSplitted = query.split()
        dfForWordInDocs = Counter()
        dfForWordInQuery = Counter()
        numberofwordsindoc = 0
        squareddoclength = 0
        squaredquerylength = 0

        # Compute Document Materix
        allwantedfiles = open(document, "r")

        for word in allwantedfiles:
            numberofwordsindoc += 1
            word = word.lower()
            if word in alluniquewordsDocs:
                alluniquewordsDocs[str(word)] += 1
            else:
                alluniquewordsDocs[str(word)] = 1

        for word in queryWordsSplitted:
            word = word.lower()
            if word in alluniquewordsDocs:
                alluniquewordsQuery[str(word)] += 1
            else:
                alluniquewordsQuery[str(word)] = 1

        for word in alluniquewordsDocs:
            dfForWordInDocs[str(word)] = log10(numberofwordsindoc / alluniquewordsDocs[str(word)])

        for word in alluniquewordsQuery:
            dfForWordInQuery[str(word)] = log10(numberofwordsindoc / alluniquewordsQuery[str(word)])

        for value in dfForWordInDocs:
            squareddoclength += dfForWordInDocs[str(value)] ** 2

        for value in dfForWordInQuery:
            squaredquerylength += dfForWordInQuery[str(value)] ** 2

        print(sqrt(squareddoclength), sqrt(squaredquerylength))

        return [alluniquewordsDocs, alluniquewordsQuery, dfForWordInDocs, dfForWordInQuery, numberofwordsindoc, sqrt(squareddoclength), sqrt(squaredquerylength)]


    #######
    # Query
    #######

    def computeSimilarity(self, phrase, document):
        [alluniquewordsDocs, alluniquewordsQuery, dfForWordInDocs, dfForWordInQuery, numberofwordsindoc, docLength, queryLength] = self.computeMatrix(phrase, document)
        return spmatrix.dot(dfForWordInDocs, dfForWordInQuery)

