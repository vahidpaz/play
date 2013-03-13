#!/usr/bin/env python

#    Desc: Answer to Google Code Jam 2010 Qualification Round: "T9 Spelling" Problem
#          https://code.google.com/codejam/contest/351101/dashboard#s=p2
# Created: January 2013
#  Status: Successful with Google Code Jam sample input
#  Author: Vahid Pazirandeh (vpaziran@gmail.com)

import sys


# Note: Most of the classes below were purposely created in an abstract
# manner so that they can support not only the T9 key mapping, but any
# other key mapping between digits and chars (more generally called "keys"
# and "values", respectively). This is simply a practice at creating a
# few small and flexible set of classes. Indeed the use of a single
# dictionary could replace a couple of these classes.


class KeypadButton:
    def __init__(self, key, mappedValues):
        self.key = key
        self.mappedValues = mappedValues

    def __eq__(self, other):
        if not other:
            return False
        return self.key == other.key and self.mappedValues == self.mappedValues

    def __str__(self):
        return 'key={}, mappedValues={}'.format(self.key, self.mappedValues)


# A keypad that allows looking up KeypadButtons based on one of their values
# rather than based on the key itself. For example, on T9 based keypads this
# would allow looking up by 'f' rather than '3'.
#
# TODO: Write pydocs
class ValueBasedKeypad:
    def __init__(self, keyMapping):
        self.valueToKey = {}
        for key, mappedValues in keyMapping.iteritems():
            for val in mappedValues:
                self.valueToKey[val] = KeypadButton(key, mappedValues)

    def __getitem__(self, val):
        return self.valueToKey[val]


# TODO: New name please? :)
class ValueToKeyConverter:
    def __init__(self, keypad):
        self.lastButton = None
        self.keypad = keypad

    def toKeyPresses(self, val):
        button = self.keypad[val]
        insertPause = ''

        if button == self.lastButton:
            insertPause = ' '
        else:
            self.lastButton = button

        pressCount = button.mappedValues.index(val) + 1
        return insertPause + (button.key * pressCount)


class T9SpellingSolution:
    # Of the form {key:val, key2:val2, ...}.
    t9KeyMappings = {'2':'abc',  '3':'def', '4':'ghi',  '5':'jkl', '6':'mno',
                     '7':'pqrs', '8':'tuv', '9':'wxyz', '0':' '}

    def __init__(self, problemFilePath):
        self.t9Keypad = ValueBasedKeypad(self.__class__.t9KeyMappings)
        with open(problemFilePath) as f:
            f.readline()
            # TODO: How do I read all lines while ignoring the line ending??? Bla!
            self.testCases = map(lambda x: x.rstrip(), f.readlines())

    def run(self):
        for i, testCaseString in enumerate(self.testCases):
            conv = ValueToKeyConverter(self.t9Keypad)
            result = []
            for char in testCaseString:
                result.append(conv.toKeyPresses(char))
            result = ''.join(result)
            print 'Case #{}: {}'.format(i+1, result)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: {} <pathToProblemInputFile>'.format(sys.argv[0])
        sys.exit(1)
    solution = T9SpellingSolution(sys.argv[1])
    solution.run()

# EOF
