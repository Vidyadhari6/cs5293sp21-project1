import glob
import argparse
import nltk
from nltk import word_tokenize
from nltk.tree import Tree
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.naive_bayes import GaussianNB
import re


def find_entity(lines, file):
    ratings = re.findall(r'_(\d{1,2}).txt', file)
    persons = []
    names_list = []
    for line in lines:
        for word_token in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(line))):
            if type(word_token) == Tree and word_token.label() == 'PERSON':
                name = ""
                for c in word_token.leaves():
                    name += c[0]
                    name += " "
                persons.append(name[:-1])
        person_set = set(persons)
        person_list = sorted(list(person_set), key=len, reverse=True)
        word_count = len(word_tokenize(line))
        for person in person_list:
            name_dict = {'name': person, 'word_count': len(person.replace(" ", "")),
                         'name_length': len(person), 'doc_length': word_count, 'ratings': ratings}
            names_list.append(name_dict)
    return names_list


def test_entity(lines, file):
    ratings = re.findall(r'_(\d{1,2}).txt', file)
    masker = '\u2588'
    test_list = []
    for line in lines:
        word_count = len(word_tokenize(line))
        check = masker + r'+\s*' + masker + r'+\s*' + masker + r'+\s*' + masker + r'+\s*' + masker + r'+'
        masked_names = re.findall(check, line)
        for masked_name in masked_names:
            test_dict = {'word_count': len(masked_name.replace(" ", "")),
                         'name_length': len(masked_name), 'doc_length': word_count, 'ratings': ratings}
            test_list.append(test_dict)
    return test_list


def redact_names(n_lines):
    sensitive_names = []
    redated_names = []
    for line in n_lines:
        for word_token in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(line))):
            if type(word_token) == Tree:
                if word_token.label() == 'PERSON':
                    for i in word_token:
                        sensitive_names.append(i[0])
            elif type(word_token) == tuple:
                None
        sensitive_names_final = list(set(sensitive_names))
        for name in sensitive_names_final:
            line = line.replace(name, '█' * len(name))
        redated_names.append(line)
    return redated_names


def write_output(output_dir, file, docs):
    import os
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    with open(output_dir, 'w', encoding='UTF-8') as fout:
        fout.truncate()
        fout.write(",".join(docs))
    return output_dir


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", type=str, required=True, help="Train Files location", nargs='*',
                        action='append')
    parser.add_argument("--test", type=str, required=False, help="Test Files location", nargs='*',
                        action='append')
    parser.add_argument("--output", type=str, required=False, help="redacted files output directory name")
    args = parser.parse_args()
    dict_vec = DictVectorizer(sparse=False)
    input_train_files = []
    train_names = []
    if args.train:
        for f in args.train[0]:
            input_train_files.append(f)
        for ind, file in enumerate(input_train_files):
            lines = []
            with open(file, 'r', encoding='UTF-8') as fin:
                lines.append(fin.read())
            train_names.append(find_entity(lines, file))
        labels = []
        features = []
        for d in train_names[0]:
            labels.append(d['name'])
            del d['name']
            features.append(d)
        target_labels = np.array(labels)
        features_train = dict_vec.fit_transform(features)
        model = GaussianNB()
        model.fit(features_train, target_labels)
        # ------------------------------------------------------------------------
        test_names = []
        test_features = []
        if args.test:
            test_files = glob.glob(args.test[0][0])
            lines = []
            for file in test_files:
                test_lines = []
                with open(file, 'r', encoding='UTF-8') as fin:
                    lines.append(fin.read())
                    redacted_lines = redact_names(lines)
                    output_location = write_output(args.output, file, redacted_lines)
                    with open(output_location, 'r', encoding='UTF-8') as fin:
                        test_lines.append(fin.read())
                        test_names.append(test_entity(test_lines, file))
            for d in test_names[0]:
                test_features.append(d)
            features_test = dict_vec.transform(test_features)
            label_pred = model.predict(features_test)
            print("Below list contains the predicted names for a given test file")
            print(label_pred)
