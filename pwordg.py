#!/usr/bin/python3

import random
import argparse
import requests

class PasswordGenerator:
    """ A really simple password generator

    Generates passwords that are increadibly easy to remember, and
    somewhat random.

    It loads words from a file, and randomly generates a password
    from those words, numbers and special characters.

    """

    extendedSymbols = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    reducedSymbols = "!-/#.,'+"

    def __init__(self, useReducedSymbols = False):
        # Use system-time as seed
        random.seed(None)
        self._symbols = self.reducedSymbols if useReducedSymbols else self.extendedSymbols

    def useReducedSymbols(self):
        self._symbols = self.reducedSymbols

    def useExtendedSymbols(self):
        self._symbols = self.extendedSymbols

    @property
    def symbols(self):
        return self._symbols

    def loadWords(self, filePath, minWordLen, maxWordLen):
        """ Loads words from a file

        Words are filtered by length so that each word is at least
        minWordLen long and not longer than maxWordLen

        Arguments:
            filePath (str) : Full path to the word-file
            minWordLen (int) : Length of the shortest acceptable word
            maxWordLen (int) : Length of the longest acceptable word
        """

        with open(filePath) as word_file:
            valid_words = set(word_file.read().split())

        assert minWordLen <= maxWordLen

        # Filter out lenght
        words = filter(lambda x : len(x) >= minWordLen and len(x) <= maxWordLen, valid_words)

        # Remove words that begin with the same letter
        words = filter(lambda x : x[0] != x[1], words)

        self.words = list(words)
        return self.words

    def getWord(self):
        """ Get a random word from the internal list of words """
        return self.words[random.randint(0, len(self.words)-1)]

    def getSymbol(self):
        """ Get a random symbol """
        return self.symbols[random.randint(0, len(self.symbols)-1)]

    def generatePassword(self, minWordCount, minNumberCount, minSymbolCount, capitalize = True, minLength = 8):
        """ Generates a password

        Arguments:
            minWordCount (int) : the smallest count of words to include
            minNumberCount (int) : the smallest count of numbers to include
            minSymbolCount (int) : the smallest count of symbols to include
            capitalize (boolean) : Indicates if each word should have the first letter capitalized
            minLength (int) :  The shortest length of acceptable password
        """
        # Define component classes
        WORD = 0
        SYMBOL = 1
        NUMBER = 2
        NOTHING = -1

        while True:

            password = ''
            lastClass = NOTHING
            numberCount = 0
            symbolCount = 0
            wordCount = 0

            while wordCount < minWordCount or numberCount < minNumberCount or symbolCount < minSymbolCount:

                # Update odds for component class
                skew = 1
                kSymbol = max(1, minSymbolCount - symbolCount + skew)
                kNumber = max(1, minNumberCount - numberCount + skew)
                kWord = max(1, minWordCount - wordCount + skew)
                kTot = kSymbol + kNumber + kWord

                # Compute probabillities
                pSymbol = kSymbol / kTot
                pNumber = kNumber / kTot

                if minSymbolCount > 0 and lastClass != SYMBOL and random.random() < pSymbol:
                    elementClass = SYMBOL
                elif minNumberCount > 0 and lastClass != NUMBER and random.random() < pNumber:
                    elementClass = NUMBER
                else:
                    elementClass = WORD

                if elementClass == WORD:
                    word = self.getWord()
                    if capitalize:
                        word = word[0].upper() + word[1:]
                    password += word
                    wordCount += 1
                elif elementClass == NUMBER:
                    password += str(random.randint(0,9))
                    numberCount += 1
                elif elementClass == SYMBOL:
                    password += self.getSymbol()
                    symbolCount += 1
                else:
                    print("ERROR")

                lastClass = elementClass
                
            if len(password) >= minLength:
                break

        return password


def downloadWordList(url = "", fileName = 'words_alpha.txt'):
    """ Downloads a word list from an URL """
    req = requests.get(url, allow_redirects = True)
    open(fileName,'wb').write(req.content)

def main():
    """ Main entry point for the program """

    parser = argparse.ArgumentParser(description='Random wordly password generator')
    # The last argument for a certain dest will be the default
    parser.add_argument('count', type=int, nargs='?', default=20, help='Number of passwords to generate, default is 20')
    parser.add_argument('-A', '--no-capitalize', help='Only lower-case letters',          dest='capitalize', action='store_false')
    parser.add_argument('-c', '--capitalize', help='Include at least one capital letter', dest='capitalize', action='store_true')
    parser.add_argument('-n', '--numerals', help='Smallest number of numerals', type=int, default=1)
    parser.add_argument('-s', '--symbols', help='Smallest number of symbols', type=int, default=1)
    parser.add_argument('-w', '--words', help='Smallest number of words', type=int, default=2)
    parser.add_argument('-l', '--length', help='Shortest acceptable password length', type=int, default=8)
    parser.add_argument('-r', '--reduced', help='Use reduced symbol set: '+PasswordGenerator.reducedSymbols, action='store_true')
    parser.add_argument('--min-word-len', help='Shortest word length', type=int, default=2)
    parser.add_argument('--max-word-len', help='Longest word length', type=int, default=5)
    parser.add_argument('--wordlist', help='File containing words', type=str, default='words_alpha.txt')
    parser.add_argument('--download', help='Download default word file', action='store_true')

    args = parser.parse_args()

    assert args.min_word_len <= args.max_word_len

    if args.download:
        downloadWordList('https://github.com/dwyl/english-words/raw/master/words_alpha.txt')

    pwgen = PasswordGenerator(args.reduced)
    pwgen.loadWords(args.wordlist, args.min_word_len, args.max_word_len)

    for _ in range(args.count):
        print(pwgen.generatePassword(args.words, args.numerals, args.symbols, args.capitalize, args.length))

if __name__ == '__main__':
    main()
