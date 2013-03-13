#!/usr/bin/env python2

#    Desc: Answer to Google Code Jam 2009 Qualification Round: "Alien Language" Problem
#          https://code.google.com/codejam/contest/90101/dashboard#s=p0
# Created: December 2012
#  Status: Successful with Google Code Jam sample input
#  Author: Vahid Pazirandeh (vpaziran@gmail.com)

import sys
import re


DEBUG = False


class Pattern():
    def __init__(self, pattern):
        # Extract pattern into a list of possible sets of letters that
        # the word may have. Each set may be a single letter (e.g., 'a')
        # or contain several letters with its enclosing parentheses
        # (e.g, '(abc)').
        #
        # Thus, the pattern '(ab)(cd)d' will be translated to
        # ['(ab)', '(cd)', 'd'].
        self.letterSets = re.findall(r'[a-z]|\([a-z]+\)', pattern)

    def __str__(self):
        return str(self.letterSets)

    def matches(self, string):
        '''Return true if this pattern matches the specified string.'''
        for letter, possibleLetters in zip(string, self.letterSets):
            if letter not in possibleLetters:
                return False
        return True


class ProblemInput():
    def __init__(self, pathToInputFile):
        '''Instantiate the problem using its input text file.'''
        inputFile = open(pathToInputFile)

        wordLengthChars, numWords, numPatterns = map(int, inputFile.readline().rstrip().split())

        if DEBUG:
            print 'wordLengthChars=%d, numWords=%d, numPatterns=%d' % (wordLengthChars, numWords, numPatterns)

        words = []
        for line in inputFile:
            words.append(line.rstrip())
            if len(words) == numWords:
                break

        patterns = []
        for line in inputFile:
            patterns.append(Pattern(line.rstrip()))
            if len(patterns) == numPatterns:
                break

        inputFile.close()

        self.words = words
        self.patterns = patterns

        #allLines = inputFile.readlines()
        #indexOfFirstWord = 1
        #indexOfLastWord = indexOfFirstWord + numWords - 1
        #indexOfFirstPattern = indexOfLastWord + 1
        #indexOfLastPattern = indexOfFirstPattern + numPatterns - 1
        #
        # TODO: How can this be written better? Lots of copying of arrays going on just to get data in the right format. I hate the newlines. :)
        #self.words = allLines[indexOfFirstWord:indexOfLastWord+1]
        #self.words = map(str.rstrip, self.words)
        #
        #self.patterns = allLines[indexOfFirstPattern:indexOfLastPattern+1]
        #self.patterns = map(str.rstrip, self.patterns)
        #self.patterns = map(Pattern, self.patterns)


prob = ProblemInput(sys.argv[1])

if DEBUG:
    for word in prob.words:
        print 'Word: %s' % word

    for pattern in prob.patterns:
        print 'Pattern: %s' % pattern

for i, pattern in enumerate(prob.patterns):
    totalMatches = 0
    for word in prob.words:
        if pattern.matches(word):
            totalMatches += 1
    print 'Case #%d: %d' % (i+1, totalMatches)

# EOF
