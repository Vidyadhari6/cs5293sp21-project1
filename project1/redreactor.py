#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import nltk
import glob
from dateparser.search import search_dates
from dateutil.parser import parse
from nltk.tree import Tree
from nltk.corpus import wordnet as wn

import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download()
def redact_names(n_lines, input_files):
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
        redacted_names_stats.append([input_files, len(sensitive_names_final)])
    return redated_names, redacted_names_stats

def redact_dates(d_lines, input_files):
    dates = []
    redacted_dates = []
    for line in d_lines:
        for date_token in search_dates(line):
            dates.append(date_token[0])
        dates_final = list(set(dates))
        for date in dates_final:
            try:
                parse(date)
                line = line.replace(date, '█' * len(date))
            except Exception:
                None
        redacted_dates.append(line)
        redacted_dates_stats.append([input_files, len(dates_final)])
    return redacted_dates, redacted_dates_stats

def redact_phones(p_lines, input_files):
    import re
    pattern = r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
    phones = []
    redacted_phones = []
    for line in p_lines:
        for phone_token in re.findall(pattern, line):
            phones.append(phone_token)
        phones_final = list(set(phones))
        for phone in phones_final:
            try:
                line = line.replace(phone, '█' * len(phone))
            except Exception:
                None
        redacted_phones.append(line)
        redacted_phones_stats.append([input_files, len(phones_final)])
    return redacted_phones, redacted_phones_stats

def redact_genders(g_lines, input_files):
    genders = []
    redacted_genders = []
    category = ['male', 'boy', 'guy', 'man', 'he', 'him', 'son', 'his', 'men', 'female', 'girl', 'lady', 'woman', 'daughter', 'women', 'she', 'hers', 'her']
    for line in g_lines:
        for l in line.split("\n"):
            for gender_token in nltk.word_tokenize(l):
                if gender_token.lower() in category:
                    genders.append(" "+ gender_token+ " ")
        genders_final = list(set(genders))
        for gender in genders_final:
            try:
                line = line.replace(gender, '█' * len(gender))
            except Exception:
                None
        redacted_genders.append(line)
        redacted_phones_stats.append([input_files, len(genders_final)])
    return redacted_genders, redacted_genders_stats

def redact_concept(c_lines, input_files, concept):
    a = wn.synsets(concept)
    syssets_c = []
    concepts = []
    redacted_sentences = []
    for i in a:
        syssets_c.append(i)
    for s in syssets_c:
        for k in s.lemmas():
            concepts.append(k.name())
    concepts_final = list(set(concepts))
    for line in c_lines:
        for sentence in line.split("\n"):
            for token_sentence in nltk.sent_tokenize(sentence):
                    for word_token in  nltk.word_tokenize(token_sentence):
                        if word_token.lower() in concepts_final:
                            line = line.replace(sentence, '█' * len(sentence))
        redacted_sentences.append(line)
    return redacted_sentences







if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Source File location", nargs='*', action='append')
    parser.add_argument("--names", required=False, help="indicator to redact names", action='store_true')
    parser.add_argument("--dates", required=False, help="indicator to redact dates", action='store_true')
    parser.add_argument("--phones", required=False, help="indicator to redact phones", action='store_true')
    parser.add_argument("--genders", required=False, help="indicator to redact genders ", action='store_true')
    parser.add_argument("--concept", type=str, required=False, help="redact sentence by concept. It can be passed multiple times")

    # parser.add_argument("--stats", type=str, required=False, help="Gives statistics for redacted files")
    # parser.add_argument("--concept", type=str, required=False, help="Concept word removal")
    # parser.add_argument("--output", type=str, required=True, help="Output File location")

    args = parser.parse_args()
    input_files = glob.glob(args.input[0][0])
    redacted_names_stats = []
    redacted_dates_stats = []
    redacted_phones_stats = []
    redacted_genders_stats = []
    for file in input_files:
        redacted_lines = []
        lines = []
        with open(file, 'r', encoding='UTF-8') as fin:
            lines.append(fin.read())
        if args.names:
            if len(redacted_lines) == 0:
                redacted_lines, redacted_names_stats = redact_names(lines, file)
            else:
                redacted_lines, redacted_names_stats = redact_names(redacted_lines, file)
        if args.dates:
            if len(redacted_lines) == 0:
                redacted_lines, redacted_dates_stats = redact_dates(lines, file)
            else:
                redacted_lines, redacted_dates_stats = redact_dates(redacted_lines, file)
        if args.phones:
            if len(redacted_lines) == 0:
                redacted_lines, redacted_phones_stats = redact_phones(lines, file)
            else:
                redacted_lines, redacted_phones_stats = redact_phones(redacted_lines, file)
        if args.genders:
            if len(redacted_lines) == 0:
                redacted_lines, redacted_genders_stats = redact_genders(lines, file)
            else:
                redacted_lines, redacted_genders_stats = redact_genders(redacted_lines, file)
        if args.concept:
            if len(redacted_lines) == 0:
                redacted_lines = redact_concept(lines, file, args.concept)
            else:
                redacted_lines = redact_concept(redacted_lines, file, args.concept)
        print(redacted_lines)

