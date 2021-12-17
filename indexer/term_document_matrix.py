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


    def computeMatrix(self):
        alluniquewordsDocs = Counter()
        dfForWordInDocs = Counter()
        numberofwordsindoc = 0
        squareddoclength = 0

        # Compute Document Materix
        allwantedfiles = open(self.documentCollection, "r")

        alluniquewordsDocs = self.tokenizer.scanner(allwantedfiles)

        for word in alluniquewordsDocs:
            dfForWordInDocs[str(word)] = log10(numberofwordsindoc / alluniquewordsDocs[str(word)])

        for value in dfForWordInDocs:
            squareddoclength += dfForWordInDocs[str(value)] ** 2

        self.matrix = dfForWordInDocs

    #######
    # Query
    #######

    def computeSimilarity(self, phrase, document):
        tfidfdoc = 0

        for word in self.matrix:
            tfidfdoc += log10(1 + self.matrix[str(word)]) * log10(self.matrix.len / self.matrix[str(word)])

        return tfidfdoc


