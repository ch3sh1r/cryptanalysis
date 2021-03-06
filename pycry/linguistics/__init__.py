#!/usr/bin/env python
#-*- coding: utf-8 -*-
import math
import json
import os

'''The following are language-specific data on character frequencies.
* kappa is the "index of coincidence"
  [link](http://en.wikipedia.org/wiki/Index_of_coincidence)
* languages represented by ISO 639-1:2002 codes
  [link](http://en.wikipedia.org/wiki/ISO_639-1)
'''
language_list = { 
        'en' :
            { 
                'alphabet': (
                    ('A', 8.16), ('B', 1.49), ('C', 2.78), 
                    ('D', 4.25), ('E',12.70), ('F', 2.22), 
                    ('G', 2.01), ('H', 6.09), ('I', 6.99), 
                    ('J', 0.15), ('K', 0.77), ('L', 4.02), 
                    ('M', 2.41), ('N', 6.74), ('O', 7.50), 
                    ('P', 1.92), ('Q', 0.09), ('R', 5.99), 
                    ('S', 6.32), ('T', 9.05), ('U', 2.75), 
                    ('V', 0.97), ('W', 2.36), ('X', 0.15), 
                    ('Y', 1.97), ('Z', 0.07),
                ), 
                'ligatures': (), 
                'kappa': 0.0667, 
            },
      
        'ru' : 
            { 
                'alphabet': (
                    ('А', 8.04), ('Б', 1.55), ('В', 4.75),
                    ('Г', 1.88), ('Д', 2.95), ('Е', 8.21),
                    ('Ё', 0.22), ('Ж', 0.80), ('З', 1.61),
                    ('И', 7.98), ('Й', 1.36), ('К', 3.49),
                    ('Л', 4.32), ('М', 3.11), ('Н', 6.72),
                    ('О',10.61), ('П', 2.82), ('Р', 5.38),
                    ('С', 5.71), ('Т', 5.83), ('У', 2.28),
                    ('Ф', 0.41), ('Х', 1.02), ('Ц', 0.58),
                    ('Ч', 1.23), ('Ш', 0.55), ('Щ', 0.34),
                    ('Ъ', 0.03), ('Ы', 1.91), ('Ь', 1.39),
                    ('Э', 0.31), ('Ю', 0.63), ('Я', 2.00),
                 ), 
                 'ligatures': (), 
                 'kappa': 0.0776,
            },

        'fr' :
            {
                'alphabet': (
                    ('A', 8.11), ('B', 0.91), ('C', 3.49), 
                    ('D', 4.27), ('E',17.22), ('F', 1.14), 
                    ('G', 1.09), ('H', 0.77), ('I', 7.44), 
                    ('J', 0.34), ('K', 0.09), ('L', 5.53), 
                    ('M', 2.89), ('N', 7.46), ('O', 5.38), 
                    ('P', 3.02), ('Q', 0.99), ('R', 7.05), 
                    ('S', 8.04), ('T', 6.99), ('U', 5.65), 
                    ('V', 1.30), ('W', 0.04), ('X', 0.44), 
                    ('Y', 0.27), ('Z', 0.09),
                ),
                'ligatures': (
                     'À', 'Â', 'Æ', 'Ç', 'É', 
                     'È', 'Ê', 'Î', 'Ï', 'Ô', 
                     'Œ', 'Ù', 'Û', 'Ü', 'Ÿ' 
                ), 
                'kappa': 0.0746, 
            },
      
        'de' :
            { 
                'alphabet': (
                    ('A', 6.50), ('B', 2.56), ('C', 2.83), 
                    ('D', 5.41), ('E',16.69), ('F', 2.04), 
                    ('G', 3.64), ('H', 4.06), ('I', 7.81), 
                    ('J', 0.19), ('K', 1.87), ('L', 2.82), 
                    ('M', 3.00), ('N', 9.90), ('O', 2.28), 
                    ('P', 0.94), ('Q', 0.05), ('R', 6.53), 
                    ('S', 6.76), ('T', 6.74), ('U', 3.70), 
                    ('V', 1.06), ('W', 1.39), ('X', 0.02), 
                    ('Y', 0.03), ('Z', 1.00), 
                ),
                'ligatures': (
                    'Ä', 'Ö', 'Ü',
                ), 
                'kappa': 0.0767,
            },
      
        'it' :
            { 
                'alphabet': (
                    ('A',11.30), ('B', 0.97), ('C', 4.35), 
                    ('D', 3.80), ('E',11.24), ('F', 1.09), 
                    ('G', 1.73), ('H', 1.02), ('I',11.57), 
                    ('J', 0.03), ('K', 0.07), ('L', 6.40), 
                    ('M', 2.66), ('N', 7.29), ('O', 9.11), 
                    ('P', 2.89), ('Q', 0.39), ('R', 6.68), 
                    ('S', 5.11), ('T', 6.76), ('U', 3.18), 
                    ('V', 1.52), ('W', 0.00), ('X', 0.02), 
                    ('Y',0.048), ('Z', 0.95), 
                ),
                'ligatures': (
                    'À', 'Ì', 'Í', 'Î', 'É', 
                    'È', 'Ò', 'Ó', 'Ù', 'Ú', 
                ), 
                'kappa': 0.0733, 
            },
        }

def get_dictionary(lang = 'en'):
    curdir = os.path.abspath(os.path.dirname(__file__))
    with open('{0}/dict/{1}.json'.format(curdir, lang)) as f:
        words = f.read()
    words = json.loads(words)
    return words

def get_ngramms(n, lang = 'en'):
    ngrams = {}
    curdir = os.path.abspath(os.path.dirname(__file__))
    with open('{0}/ngram/{1}-{2}.json'.format(curdir, lang, n)) as f:
        return json.loads(f.read())

def define_language(text):
    distribution = { langcode:0 for langcode in language_list.keys() }
    length = 0
    for letter in text:
        for langcode in language_list.keys():
            alphabet = [x[0] for x in language_list[langcode]['alphabet']]
            if letter.upper() in alphabet:
                distribution[langcode] += 1
                length += 1
    for langcode in distribution.keys():
        if distribution[langcode] > 0:
            distribution[langcode] /= length
    maximum = sorted(distribution.items(), key = lambda x: x[1], reverse = True)[0][0]
    if maximum == 'ru':
        return 'ru'
    else:
        return 'en'

def restore_words(text, maxwordlen=20, lang = 'en'):
    N = 1024908267229
    unseen = [math.log10(10./(N * 10**L)) for L in range(50)]        
    curdir = os.path.abspath(os.path.dirname(__file__))
    with open('{0}/dict/{1}.counted.json'.format(curdir, lang)) as f:
        Pw = json.loads(f.read())
    with open('{0}/dict/{1}.counted_pairs.json'.format(curdir, lang)) as f:
        Pw2 = json.loads(f.read())

    def cPw(word, prev='<UNK>'):
        if word not in Pw: 
            return unseen[len(word)]
        elif prev + ' ' + word not in Pw2: 
            return Pw[word]
        else: 
            return Pw2[prev + ' ' + word]

    prob = [[-99e99] * maxwordlen for _ in range(len(text))]
    strs = [[''] * maxwordlen for _ in range(len(text))]
    for j in range(maxwordlen):
        prob[0][j] = cPw(text[:j + 1])
        strs[0][j] = [text[:j + 1]]
    for i in range(1, len(text)):
        for j in range(maxwordlen):
            if i + j + 1 > len(text): break
            candidates = [(prob[i - k - 1][k] + cPw(text[i:i + j + 1],strs[i - k - 1][k][-1]),
                           strs[i - k - 1][k] + [text[i:i + j + 1]]) for k in range(min(i, maxwordlen))]
            prob[i][j], strs[i][j] = max(candidates)
    ends = [(prob[-i - 1][i],strs[-i - 1][i]) for i in range(min(len(text), maxwordlen))]
    return max(ends)

def istext_ngramms(text, ngr, lang = 'en'):
    ngrams, floor, n = ngr
    score = 0
    for i in range(len(text) - n + 1):
        if text[i: i + n] in ngrams: 
            score += ngrams[text[i: i + n]]
        else: 
            score += floor          
    return score

if __name__ == "__main__":
    pass
