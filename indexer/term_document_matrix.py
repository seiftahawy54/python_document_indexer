import pickle
from .tokenizer import Tokenizer
from dataclasses import dataclass
from scipy.sparse import spmatrix
import numpy as np
from .document_collection import DocumentCollection
from collections import Counter
from math import log10

def my_printer(counterObject: Counter):
    for word in counterObject:
        print(f"{word} : {counterObject[str(word)]}")

@dataclass
class TermDocumentMatrix:
    tokenizer: Tokenizer
    documentCollection: DocumentCollection
    matrix: spmatrix

    ##############
    # Construction
    ##############

    def __init__(self, tokenizer, documentCollection, positionalIndex):
        self.tokenizer = tokenizer
        self.documentCollection = documentCollection
        self.computeMatrix(positionalIndex)

    def computeMatrix(self, positionalIndex):

        # frequenceies of all words     -> calculated
        # number of all words           -> finished
        # df for each word              -> calculated
        # idf for each word             -> calculated
        # tf_idf for each word          -> calculated
        # sparse matrix                 -> returned

        # alluniquewordsDocs = Counter()
        dfForWordInDocs = Counter()
        idf_for_word_in_docs = Counter()
        tf_idf_for_words_in_docs = Counter()
        dfForWordInDocsArr = []
        squareddoclength = 0
        numberofwordsindoc = positionalIndex.numberOfDocuments

        # frequenceies of all words && number of all words
        for term, postingsList in positionalIndex.dictionary.items():
            # Compute the number of documents that contains the term.
            dfForWordInDocs[str(term)] = len(postingsList.postings)

        # idf for each word
        for word, postingsList in positionalIndex.dictionary.items():
            idf_for_word_in_docs[str(word)] = log10(numberofwordsindoc / dfForWordInDocs[str(word)])

        # tf_idf for each word
        for word, postingsList in positionalIndex.dictionary.items():
            tf_idf_for_words_in_docs[str(word)] = log10(1 + dfForWordInDocs[str(word)]) * idf_for_word_in_docs[
                str(word)]

        # transform idf counter to idf
        tf_idf_for_words_in_docs_arr = [None] * len(list(dfForWordInDocs))
        for i, word in enumerate(dfForWordInDocs):
            tf_idf_for_words_in_docs_arr[i] = tf_idf_for_words_in_docs[str(word)]

        unique_words_arr = [None] * len(list(dfForWordInDocs))
        for i, word in enumerate(dfForWordInDocs):
            unique_words_arr[i] = word

        # sparse matrix
        self.matrix = [unique_words_arr], [tf_idf_for_words_in_docs_arr]
        print(self.matrix)

    #######
    # Query
    #######

    def computeSimilarity(self, phrase, document):
        pass

    ###########
    # Load/Save
    ###########

    def save(self, fileName):
        with open(self.documentCollection.directory / fileName, "wb") as file:
            # Avoid pickling the runtime text fields.
            if hasattr(self.tokenizer, "text"): del self.tokenizer.text
            if hasattr(self.tokenizer.scanner, "text"): del self.tokenizer.scanner.text

            pickle.dump(self, file, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def load(cls, path):
        with open(path, "rb") as file:
            return pickle.load(file)
