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

#nltk.download()
def redact_names(n_lines, input_files):
    redacted_names_stats = []
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
        redacted_names_stats.append([input_files.split('/')[-1], len(sensitive_names_final)])
    return redated_names, redacted_names_stats

def redact_dates(d_lines, input_files):
    redacted_dates_stats = []
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
        redacted_dates_stats.append([input_files.split('/')[-1], len(dates_final)])
    return redacted_dates, redacted_dates_stats

def redact_phones(p_lines, input_files):
    redacted_phones_stats = []
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
        redacted_phones_stats.append([input_files.split('/')[-1], len(phones_final)])
    return redacted_phones, redacted_phones_stats

def redact_genders(g_lines, input_files):
    genders = []
    redacted_genders = []
    redacted_genders_stats = []
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
        redacted_genders_stats.append([input_files.split('/')[-1], len(genders_final)])
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

def write_output(output_dir, file, docs):
    import os
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    output_file = output_dir + '/' + file.split('/')[-1].split('.')[0] + '.redacted'
    with open(output_file, 'w', encoding = 'UTF-8') as fout:
        fout.truncate()
        fout.write(",".join(docs))





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Source File location", nargs='*', action='append')
    parser.add_argument("--names", required=False, help="indicator to redact names", action='store_true')
    parser.add_argument("--dates", required=False, help="indicator to redact dates", action='store_true')
    parser.add_argument("--phones", required=False, help="indicator to redact phones", action='store_true')
    parser.add_argument("--genders", required=False, help="indicator to redact genders ", action='store_true')
    parser.add_argument("--concept", type=str, required=False, help="Redact a full sentence by a concept type")
    parser.add_argument("--output", type=str, required=True, help="redacted files output directory name")
    parser.add_argument("--stats", type=str, required=False, help="generate stats for redaction process with stats location")

    args = parser.parse_args()
    input_files = glob.glob(args.input[0][0])
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
        if args.output:
            write_output(args.output, file, redacted_lines)

        if args.stats:
            import os
            import csv
            if not os.path.exists(args.stats):
                os.mkdir(args.stats)
            output_stats_file = args.stats + '/' + file.split('/')[-1].split('.')[0] + '.stats'
            with open(output_stats_file, 'w', encoding='utf-8') as fout:
                fout.truncate()
                writer = csv.writer(fout, delimiter='-', quoting=csv.QUOTE_NONE)
                fout.write('Total number of names redacted in the file \n')
                writer.writerows(redacted_names_stats)
                fout.write('Total number of gender identifiers redacted in the file \n')
                writer.writerows(redacted_genders_stats)
                fout.write('Total number of phone numbers redacted in the file \n')
                writer.writerows(redacted_phones_stats)
                fout.write('Total number of dates redacted in the file \n')
                writer.writerows(redacted_dates_stats)


