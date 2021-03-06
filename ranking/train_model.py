from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
from sklearn.utils import resample
from sklearn.preprocessing import MinMaxScaler
import pickle
import numpy as np
from random import shuffle

def subtractive_balance(x, y):
    '''
    Given feature matrix x and label vector y, return subset of x and y
    (subset of the rows) such that there are as many positive labels
    as negative labels.
    Data that we have has more negative than positive. But any ML algos
    prefer a balance between pos and negative. Subtractive balancing
    removes negative examples until a balance is reached between pos
    and negative exemplars.
    '''

    # Compute the row indices of positive, negative samples
    id_pos = [i for i in range(y.shape[0]) if y[i] == 1]
    id_neg = [i for i in range(y.shape[0]) if y[i] == 0]

    # Create an array of the row indices of all positive samples and
    # a random subset of the negative samples (equal in size to the set
    # of all positive samples).
    num_pos = len(id_pos)
    shuffle(id_neg)
    id_bal = np.array(id_pos + id_neg[:int(num_pos * 1.8)])

    # Return features (x) and labels (y) for our new, balanced subset of
    # the data.
    print('balancing {} samples down to {}'.format(
        y.shape[0], id_bal.shape[0]))
    return (x[id_bal], y[id_bal])


def train_model_SVM(train_data, dev_data, num_resamples=5):
    x_train = train_data['x']
    scaler = MinMaxScaler()
    det = x_train[:, 2].reshape(-1, 1)
    infinites = np.argwhere(np.isinf(det))
    for n in infinites:
        det[n] = 0
    scaler.fit(det)
    s = x_train[:, 3].reshape(-1, 1)
    scaler.fit(s)
    vec1 = scaler.transform(det).flatten()
    vec2 = scaler.transform(s).flatten()
    x_train[:, 2] = vec1
    x_train[:, 3] = vec2
    y_train = train_data['y']
    #(x_train, y_train) = subtractive_balance(x_train, y_train)
    x_dev = dev_data['x']
    #x_dev = x_dev.reshape(-1, 1)
    y_dev = dev_data['y']

    det = x_dev[:, 2].reshape(-1, 1)
    infinites = np.argwhere(np.isinf(det))
    for n in infinites:
        det[n] = 0
    scaler.fit(det)
    s = x_dev[:, 3].reshape(-1, 1)
    scaler.fit(s)
    vec1 = scaler.transform(det).flatten()
    vec2 = scaler.transform(s).flatten()
    x_dev[:, 2] = vec1
    x_dev[:, 3] = vec2

    C = 1e-7
    curr_best_C = 0
    best_f1 = 0
    best_p = 0
    best_r = 0
    f1_scores = []
    best_model = LinearSVC()
    # x_train = x_train[:, 1].reshape(-1, 1)
    # x_dev = x_dev[:, 1].reshape(-1, 1)
    while (C <= 1e7):
        for sample_num in range(num_resamples):
            model = LinearSVC(C=C)
            (x_train_boot, y_train_boot) = resample(x_train, y_train)
            model.fit(x_train_boot, y_train_boot)
            y_dev_pred = model.predict(x_dev)
            f1 = f1_score(y_dev, y_dev_pred)
            if f1 > best_f1:
                best_f1 = f1
                curr_best_C = C
                best_p = precision_score(y_dev, y_dev_pred)
                best_r = recall_score(y_dev, y_dev_pred)
                best_model = model
        C = C * 10
    print(best_f1)
    print(best_p)
    print(best_r)
    print(curr_best_C)
    print(best_model)

def train_MLP(train_data, dev_data, num_resamples=5):
    x_train = train_data['x']
    #x_train = x_train.reshape(-1, 1)
    y_train = train_data['y']
    x_dev = dev_data['x']
    #x_dev = x_dev.reshape(-1, 1)
    y_dev = dev_data['y']

    scaler = MinMaxScaler()
    det = x_train[:, 2].reshape(-1, 1)
    infinites = np.argwhere(np.isinf(det))
    for n in infinites:
        det[n] = 0
    scaler.fit(det)
    s = x_train[:, 3].reshape(-1, 1)
    scaler.fit(s)
    vec1 = scaler.transform(det).flatten()
    vec2 = scaler.transform(s).flatten()
    x_train[:, 2] = vec1
    x_train[:, 3] = vec2
    y_train = train_data['y']
    (x_train, y_train) = subtractive_balance(x_train, y_train)
    x_dev = dev_data['x']
    #x_dev = x_dev.reshape(-1, 1)
    y_dev = dev_data['y']

    det = x_dev[:, 2].reshape(-1, 1)
    infinites = np.argwhere(np.isinf(det))
    for n in infinites:
        det[n] = 0
    scaler.fit(det)
    s = x_dev[:, 3].reshape(-1, 1)
    scaler.fit(s)
    vec1 = scaler.transform(det).flatten()
    vec2 = scaler.transform(s).flatten()
    x_dev[:, 2] = vec1
    x_dev[:, 3] = vec2

    C = 1e-7
    curr_best_C = 0
    best_f1 = 0
    best_p = 0
    best_r = 0
    best_prob = None
    f1_scores = []
    best_model = MLPClassifier()
    while (C <= 1e7):
        model = MLPClassifier(solver='lbfgs', alpha=C, random_state=1, activation='tanh')
        for sample_num in range(num_resamples):
            (x_train_boot, y_train_boot) = resample(x_train, y_train)
            model.fit(x_train_boot, y_train_boot)
            probs = model.predict_proba(x_dev)
            y_dev_pred = model.predict(x_dev)
            y_dev_pred_prob = model.predict_proba(x_dev)
            np.set_printoptions(threshold=np.nan)
            f1 = f1_score(y_dev, y_dev_pred)
            if f1 > best_f1:
                best_prob = y_dev_pred_prob 
                best_f1 = f1
                curr_best_C = C
                best_p = precision_score(y_dev, y_dev_pred)
                best_r = recall_score(y_dev, y_dev_pred)
                best_model = model
        C = C * 10
    print(best_f1)
    print(best_p)
    print(best_r)
    print(curr_best_C)
    print(best_model)
    
    return(best_model)


def main():
    query_cands = []
    with gzip.open("../data/WikiQA/WikiQA-dev.tsv.gz") as f:
            next(f)
            for line in f:
                line = line.decode('UTF-8')
                line = line.lower()
                arr = line.split("\t")
                alpha = re.compile('[^0-9a-zA-Z]')
                qid = arr[0]
                qids[qid] = True
                aid = arr[4]
                aids[aid] = True
                pair = [str(arr[1]), str(arr[5])]
                 query_cands.append(pair)
    print(query_cands)
    
    train_data = pickle.load(open("./processed_train.p", "rb"))
    dev_data = pickle.load(open("./processed_dev.p", "rb"))
    #train_model_SVM(train_data, dev_data)
    model = train_MLP(train_data, dev_data)
    with open("trained_model.p", "wb") as p:
        pickle.dump(model, p)



if __name__ == '__main__':
    main()

