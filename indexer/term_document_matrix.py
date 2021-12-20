import pickle

from .tokenizer import Tokenizer
from dataclasses import dataclass
from scipy.sparse import spmatrix
from scipy.sparse import csr_matrix
from .document_collection import DocumentCollection
from math import log10

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

        N = 0
        for doc in self.documentCollection.__iter__():
            N += 1

        i = 0
        documentsArr = [None] * N
        for doc in self.documentCollection.__iter__():
            documentsArr[i] = str(doc.path)[18:21]
            i += 1

        x, y = N, len(positionalIndex.dictionary.items())
        data_arr = csr_matrix((x, y)).toarray()

        k, j = 0, 0
        for term, postingsList in positionalIndex.dictionary.items():
            dft = len(postingsList.postings)
            idft = log10(N / len(postingsList.postings))
            for posting in postingsList.postings:
                tftd = posting.frequency
                tfidftd = tftd * idft
                data_arr[j][k] = tfidftd
                j += 1
            j = 0
            k += 1

        self.matrix = data_arr
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
