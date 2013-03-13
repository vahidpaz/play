#!/usr/bin/env python2

#    Desc: Answer to Google Code Jam 2011 Qualification Round: "Magicka" Problem
#          https://code.google.com/codejam/contest/975485/dashboard#s=p1
# Created: December 2012
#  Status: Successful with Google Code Jam sample input
#  Author: Vahid Pazirandeh (vpaziran@gmail.com)

import sys


class ElementList():
    def __init__(self, combinedPairs, opposedPairs):
        self.combinedPairs = combinedPairs
        self.opposedPairs = opposedPairs
        self.elements = []

    def __str__(self):
        return str(self.elements).replace('\'', '')

    def add(self, baseElement):
        self.elements.append(baseElement)
        if not self._processCombinedPairs():
            self._processOpposedPairs()

    def _processCombinedPairs(self):
        result = False
        while len(self.elements) >= 2:
            lastTwo = (self.elements[-2], self.elements[-1])

            if not self.combinedPairs.canCombine(*lastTwo):
                break

            # Replace last two elements with non-base element.
            self.elements[-2:] = self.combinedPairs.combine(*lastTwo)
            result = True
        return result

    def _processOpposedPairs(self):
        if self.opposedPairs.isOpposed(self.elements[-1], self.elements[:-1]):
            self.elements = []
            return True
        return False


class CombinedPairs():
    def __init__(self):
        # Dict structure: key=tuple(<baseElementPair>), val=<resultElement>
        self.combinations = {}

    def _makeKey(self, base1, base2):
        key = [base1, base2]
        key.sort()
        return tuple(key)

    def add(self, base1, base2, result):
        # Dict key is sorted so that lookups can be made without regard to pair order.
        # TODO: Is there an easier way of doing this than generating a tuple? Better data structure?
        key = self._makeKey(base1, base2)
        self.combinations[key] = result

    def combine(self, base1, base2):
        key = self._makeKey(base1, base2)
        if key in self.combinations:
            return self.combinations[key]
        else:
            return None

    def canCombine(self, base1, base2):
        return self.combine(base1, base2) != None


class OpposedPairs():
    def __init__(self):
        # Dict structure: key=<element>, val=list(<opposedElements>)
        self.opposed = {}

    def add(self, opp1, opp2):
        # TODO: Is there a Pythonic way of doing this?
        # Meaning, "check if key exists in dict, then do this, else do that".
        # I don't like the "try, except KeyError" technique as it's not as universally readable.
        if opp1 in self.opposed:
            self.opposed[opp1].append(opp2)
        else:
            self.opposed[opp1] = [opp2]

        if opp2 in self.opposed:
            self.opposed[opp2].append(opp1)
        else:
            self.opposed[opp2] = [opp1]

    def _opposedTo(self, rival):
        if rival in self.opposed:
            return self.opposed[rival]
        else:            
            return []

    def isOpposed(self, rival, possibleOpposersToTest):
        actualOpposers = self._opposedTo(rival)
        # Use set intersection to find present opposers.
        return len(set(actualOpposers) & set(possibleOpposersToTest)) > 0


class MagickaInput():
    def __init__(self, inputStream):
        self.testCases = []

        # TODO: This is very annoying. I almost never want the newline
        # that is retrieved in the readline() method. How can I stop
        # that from being retrieved??
        numTestCases = int(inputStream.readline().rstrip())

        for i in range(numTestCases):
            # TODO: Would it be better to use a class to represent
            # TestCase rather than a dictionary?
            testCase = {'combinedPairs': CombinedPairs(),
                        'opposedPairs':  OpposedPairs(),
                        'baseElements':  []}

            lineTokens = inputStream.readline().rstrip().split()
            index = 0

            numCombinations = int(lineTokens[0])
            index += 1

            if numCombinations > 0:
                for combinedPair in lineTokens[index:index+numCombinations]:
                    testCase['combinedPairs'].add(*combinedPair)
                index += numCombinations

            numOppositions = int(lineTokens[index])
            index += 1

            if numOppositions > 0:
                for opposedPair in lineTokens[index:index+numOppositions]:
                    testCase['opposedPairs'].add(*opposedPair)
                index += numOppositions

            baseElementsLen = int(lineTokens[index])
            index += 1

            testCase['baseElements'] = lineTokens[index]
            self.testCases.append(testCase)


class MagickaOutput():
    def __init__(self, magickaInputStream, resultOutStream):
        self.resultOutStream = resultOutStream
        self.magickaInput = MagickaInput(magickaInputStream)

    def run(self):
        for i, testCase in enumerate(self.magickaInput.testCases):
            resultList = ElementList(testCase['combinedPairs'], testCase['opposedPairs'])

            for baseElement in testCase['baseElements']:
                resultList.add(baseElement)

            self.resultOutStream.write('Case #{} {}\n'.format(i+1, resultList))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: {} <pathToProblemInputFile>'.format(sys.argv[0])
        sys.exit(1)

    print '{:*^60}'.format(' [Magicka] ')
    inputFile = open(sys.argv[1])
    out = MagickaOutput(inputFile, sys.stdout)
    out.run()
    inputFile.close()

# EOF
