import numpy as np
import sklearn.metrics.pairwise
import sklearn
import math
import gzip
from scipy import sparse
import logging
import pickle
import re
import numpy as np

class QwordPreprocess:
    def __init__(self):
        self.q_words = ["", "who", "what", "when", "where", "why", "how", "is", "whom"]

    def get_question_word_data(self, dataset):
        final_list = []
        with gzip.open(dataset, 'rb') as f:
            next(f)
            for line in f:
                line = line.decode('UTF-8')
                line = line.lower()
                arr = line.split("\t")
                alpha = re.compile('[^0-9a-zA-Z]')
                q = alpha.sub(' ', str(arr[1]))
                q = q.split()
                index = 0
                if q[0] in self.q_words:
                    index = self.q_words.index(q[0])
                final_list.append(index)
        return np.asarray(final_list)
    
    def get_question_word_run(self, data):
        final_list = []
        for pair in data:
            question = pair[0]
            question = question.lower()
            alpha = re.compile('[^0-9a-zA-Z]')
            q = alpha.sub(' ', question)
            index = 0
            if question[0] in self.q_words:
                index = self.q_words.index(q[0])
            final_list.append(index)
        return np.asarray(final_list)
