#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import pycry.linguistics as linguistics
import pycry.cipher.classic as classic
import math
import os

class Caesar(classic.core):
    '''An implementation of the Caesar cipher.
    '''
    def encrypt(self, shift):
        '''Encipher input (plaintext) using the Caesar cipher 
        and return it (ciphertext).
        '''
        ciphertext = []
        for char in self.message:
            if char.upper() in self.alphabet:
                pos = self.ord(char)
                ciphertext.append(
                        self.alphabet[(pos + shift) % len(self.alphabet)])
            else:
                ciphertext.append(char)
        return ''.join(ciphertext)

    def decrypt(self, shift):
        '''
        Decipher input (ciphertext) using the Caesar cipher and return it
        (plaintext).
        '''
        return self.encrypt(-shift)

    def decipher(self):
        '''
        Most effective method.
        '''
        return self.pick()

    def pick(self):
        hypotesa = []
        for j in range(len(self.alphabet)):
            high = self.alphabet_distribued[j]
            for i in range(len(self.statistic())):
                now_high = self.statistic()[i][0]
                key = (self.ord(high) - self.ord(now_high)) % len(self.alphabet)
                ot = self.decrypt(key)
                if len(ot) > 100:
                    score = linguistics.istext_ngramms(ot, self.trigrams)
                else:
                    score = linguistics.istext_ngramms(ot, self.tetragrams)
                hypotesa.append((score, ot, key))
        return max(hypotesa)[1:]

    def bruteforce(self):
        '''Bruteforce with all keys, there are length of alphabet
        of them.
        '''
        hypotesa = []
        for b in range(len(self.alphabet)):
            ot = self.decrypt(b)
            if len(ot) > 100:
                score = linguistics.istext_ngramms(ot, self.trigrams)
            else:
                score = linguistics.istext_ngramms(ot, self.tetragrams)
            hypotesa.append((score, ot, b))
        return max(hypotesa)[1:]

def main():
    from optparse import OptionParser
    parser = OptionParser('usage: ./%prog [options] filename')
    parser.add_option('-a', '--analysis',
                      action = 'store_true', dest = 'analysis', default=True,
                      help = 'make analysis, default action')
    parser.add_option('-e', '--encrypt',
                      metavar="A", 
                      help="encrypt file with A shift")
    parser.add_option('-d', '--decrypt',
                      metavar="A", 
                      help = 'decrypt file with A shift')
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
    else:
        if os.path.exists(args[0]):
            message = open(args[0]).readlines()
        else:
            message = args[0]
        ct = Caesar(message)
        if options.encrypt or options.decrypt:
            if options.encrypt:
                a = options.encrypt
                message = ct.encrypt(int(a))
            elif options.decrypt:
                (a, b) = options.decrypt.split('x')
                message = ct.decrypt(int(a))
            print(message)
        else:
            print("Analysis...")
            print("Defined language is {0}.".format(ct.language))
            ot = ct.decipher()
            print(ot[0])
            print("Decryption parametres is a={0}.".format(ot[1]))

if __name__ == "__main__":
    main()
