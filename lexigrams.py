import numpy as np

class Dictionary:
    def __init__(self, DICT='english.dic'):
        self.dictionary = [w.strip() for w in open(DICT).readlines()]
        self.dict_cca = np.array([self.to_cca(word) for word in self.dictionary])

    def index(self, c):
        ''' Map Z->N and W->M, etc. '''
        if c == ord('Z'): c = ord('N')
        elif c == ord('W'): c = ord('M')
        return c - ord('A')

    def to_cca(self, word):
        ''' Returns 26-index array of letter counts in string '''
        W = [self.index(c) for c in bytearray(word.upper(), 'utf-8')]
        return np.array([W.count(i) for i in range(26)])

    def find_lexigrams(self, full, used):
        ''' Returns possible lexigrams from leftover letters. If the anagram
        cannot be spelled with the input letters, will return useful error
        message instead. '''
        letter_bank = self.to_cca(full) - self.to_cca(used)
        res = []
        if min(letter_bank) < 0:
            for c in np.where(letter_bank<0)[0]:
                pluralizer = '\'s' if letter_bank[c] < -1 else ''
                res.append('Short {} letter {}{}'.format(-letter_bank[c],chr(c+ord('A')),pluralizer))
        else:
            w = np.where(np.min(letter_bank-self.dict_cca, axis=1) >= 0)
            res = [self.dictionary[i] for i in w[0]]
        return '\n'.join(res)
