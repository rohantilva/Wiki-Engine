# ranking and shit=
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
from sklearn.utils import resample
import pickle
import numpy as np
from random import shuffle
import logging

def pre_ranking(x_features, model, query_cands, uuidDict):
    retDict = {}
    probs = model.predict_proba(x_features)
    for i in range(len(probs)):
        prob_yes = probs[i][1]
        logging.info(prob_yes)
        logging.info("\n\n\n\n\n\n\n")
        sentence = query_cands[i][1]
        uuid = uuidDict[sentence]
        retDict[uuid] = prob_yes
    return retDict
