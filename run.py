import numpy as np
import pandas as pd
import re, argparse, datetime
from timeit import default_timer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.metrics import f1_score, make_scorer
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier

def get_parser():
    """ Builds the argument parser for the program. """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=str, dest='clf_key', default='dt', choices=['dt', 'xt', 'xts', 'rf'], help='A classifier to use.')
    parser.add_argument('-m', type=str, dest='mode', default='test', choices=['cv', 'test'], help='Mode to run the program in (cross-validation or test).')
    parser.add_argument('-k', type=int, dest='cv', default=5, help='Number of folds in KFold cross-validation.')
    parser.add_argument('-d', '--data', type=str, dest='data_name', default='econbiz', help='Name of the dataset to use (econbiz or pubmed).')
    parser.add_argument('-f', type=float, dest='data_fraction', default=0.1, help='The fraction of the data to be used (0, 1>.')
    parser.add_argument('-t', type=float, dest='test_size', default=0.1, help='Test size (0, 1>.')
    parser.add_argument('--max_depth', type=int, dest='max_depth', default=None, help='The maximum depth of the tree.')
    parser.add_argument('--min_ss', type=int, dest='min_ss', default=2, help='The minimum number of samples required to split an internal tree node.')
    parser.add_argument('--max_features', type=int, dest='max_features', default=None, help='The number of features to consider when looking for the best split in the tree.')
    parser.add_argument('-n', type=int, dest='n_estimators', default=10, help='The number of estimators in the ensemble.')
    parser.add_argument('-j', type=int, dest='n_jobs', default=-1, help='The number of jobs to run in parallel.')
    parser.add_argument('-v', type=int, dest='verbose', default=0, help='Verbosity of the program.')
    parser.add_argument('-b', '--batch', dest='is_batch_mode', action='store_true', default=False, help='Whether the program runs in a batch mode (affects file locations).')

    return parser

def get_data(options):
    """ Loads and pre-processes the data. """
    if options.verbose > 0:
        print(f'Loading data [dataset: {options.data_name}, fraction: {options.data_fraction}, test size: {options.test_size}]')
    
    # Load the data.
    location_prefix = '../../' if options.is_batch_mode else ''
    data = pd.read_csv(f'{location_prefix}data/{options.data_name}.csv')

    # Get raw values from the DataFrame.
    X_all = data['title'].values
    # Labels are separated by a '\t' character. Convert them into a list of labels per each data row.
    Y_all = [x.split('\t') for x in data['labels'].values]

    # Get only a fraction of the data if necessary
    if options.data_fraction < 1.0:
        data_slice = int(options.data_fraction * X_all.shape[0])
        X_raw, Y_raw = X_all[:data_slice], Y_all[:data_slice]
    else:
        X_raw, Y_raw = X_all, Y_all

    # Allow for tokens fitting into the following pattern only.
    word_regexp = r"(?u)\b[a-zA-Z_][a-zA-Z_]+\b"
    # Take only the most frequent 25k words. Use unigrams.
    terms = CountVectorizer(input='content', stop_words='english', binary=False, token_pattern=word_regexp, max_features=25000, ngram_range=(1, 1))
    X = terms.fit_transform(X_raw)

    # Binrize the labels (convert them into a sparse matrix of one-hot vectors).
    mlb = MultiLabelBinarizer(sparse_output=True)
    Y = mlb.fit_transform(Y_raw)

    return train_test_split(X, Y, test_size=options.test_size)

def get_model(options):
    """ Prepare a classifier for training. """
    classifiers = {
        "dt" : DecisionTreeClassifier(max_depth=options.max_depth,
                                      min_samples_split=options.min_ss,
                                      max_features=options.max_features),
        "xt" : ExtraTreeClassifier(max_depth=options.max_depth,
                                   min_samples_split=options.min_ss,
                                   max_features=options.max_features),
        "xts" : ExtraTreesClassifier(n_estimators=options.n_estimators,
                                     n_jobs=options.n_jobs,
                                     max_depth=options.max_depth,
                                     min_samples_split=options.min_ss,
                                     max_features=options.max_features),
        "rf" : RandomForestClassifier(n_estimators=options.n_estimators,
                                      n_jobs=options.n_jobs,
                                      max_depth=options.max_depth,
                                      min_samples_split=options.min_ss,
                                      max_features=options.max_features)
    }

    # Prepare the pipeline that consists of TF-IDF representation and a classifier.
    trf = TfidfTransformer(sublinear_tf=False, use_idf=True, norm='l2')
    clf = Pipeline([("trf", trf), ("clf", classifiers[options.clf_key])])

    return clf

if __name__ == "__main__":
    # Get and parse passed arguments.
    parser = get_parser()
    options = parser.parse_args()

    if options.verbose > 0:
        print('### Starting ###')
        print('Arguments:', options)

    X_train, X_test, Y_train, Y_test = get_data(options)

    clf = get_model(options)

    # The program can be run in either a 'cross-validation' or a 'test' mode.
    # The former performs k-fold cross-validation, while the latter fits the selected model
    # on the training data and runs predictions against the test set.
    # Both modes report samples-based F1-score, fitting time and prediction time (in seconds).
    if options.mode == 'cv':
        if options.verbose > 0:
            print(f'Running {options.cv}-fold cross-validation')

        scores = cross_validate(clf, X_train.toarray(), Y_train.toarray(), cv=options.cv,
                        scoring=make_scorer(f1_score, average='samples'), n_jobs=options.n_jobs, verbose=options.verbose)

        test_score = scores['test_score']
        fit_time = scores['fit_time']
        score_time = scores['score_time']
        print("F1-score: %0.2f (+/- %0.2f)" % (test_score.mean(), test_score.std()))
        print("Fit time: %0.2f (+/- %0.2f)" % (fit_time.mean(), fit_time.std()))
        print("Prediction time: %0.2f (+/- %0.2f)" % (score_time.mean(), score_time.std()))
    else:
        if options.verbose > 0:
            print('Training the model')
        
        fit_time_start = default_timer()
        clf.fit(X_train.toarray(), Y_train.toarray())
        fit_time_end = default_timer()

        if options.verbose > 0:
            print('Running predictions')

        pred_time_start = default_timer()
        Y_pred = clf.predict(X_test.toarray())
        pred_time_end = default_timer()

        test_score = f1_score(Y_test.toarray(), Y_pred, average='samples')
        print("F1-score: %0.2f" % (test_score))
        print("Fit time: %0.2f" % (fit_time_end - fit_time_start))
        print("Prediction time: %0.2f" % (pred_time_end - pred_time_start))