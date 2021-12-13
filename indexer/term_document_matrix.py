from . tokenizer import Tokenizer
from dataclasses import dataclass
from scipy.sparse import spmatrix
from . document_collection import DocumentCollection
import os


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
        alluniquewords = dict()
        # firstdoc = open("../sample_collection/001", "r")
        # paragraphs = firstdoc.read()

        allwantedfiles = os.listdir('../sample_collection')

        for file in allwantedfiles:
            currentfile = open('../sample_collection/' + file, "r")
            filecontent = currentfile.read()

            for word in filecontent.split():
                word = word.lower()
                if word in alluniquewords:
                    alluniquewords[str(word)] += 1
                else:
                    alluniquewords[str(word)] = 1

        writing_file = open("unique_words", "w+")
        for words in alluniquewords:
            writing_file.write(words + " : " + str(alluniquewords[words]))

    #######
    # Query
    #######

    def computeSimilarity(self, phrase, document):
        raise NotImplementedError
