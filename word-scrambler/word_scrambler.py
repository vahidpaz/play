#!/usr/bin/env python3

import re
import sys
import random
import os
import io


class WordScrambler:
    """Rearranges the order of letters in a text file, while remaining humanly legible. It's fun :)

    The human mind is capable of deciphering words even when the letters
    in the middle of the words have been rearranged. Keeping the first and
    last letters stationary, the others can be shuffled around.

    Given a text file, this class will scramble all its words and save the result
    to the specified output file. The file size of the output will match that
    of the input.

    This class supports unicode characters, thus other languages beyond
    English should be supported. However, this has not been extensively tested.

    A static utility function ``scramble_word()`` is also provided for users to
    rearrange the letters of their own words.
    """

    def __init__(self, input_filename, output_filename):
        self.input_filename = input_filename
        self.output_filename = output_filename

    @staticmethod
    def scramble_word(word):
        if not word.isalpha() or len(word) < 4:
            return word

        first, middle, last = word[0], word[1:-1], word[-1]

        mixed_middle = random.sample(middle, k=len(middle))
        random.shuffle(mixed_middle)
        mixed_middle = ''.join(mixed_middle)

        return first + mixed_middle + last

    def _scrambleline(self, line):
        simpleword_re = re.compile(r'(\w+)|([^\w]+)')
        buffer = io.StringIO()

        for word, non_word in re.findall(simpleword_re, line):
            # Only one of the groups will have matched, and the other will be empty string.
            token = word or non_word

            scrambled = WordScrambler.scramble_word(token)
            assert sorted(token) == sorted(scrambled)
            buffer.write(scrambled)

        result = buffer.getvalue()
        buffer.close()
        return result

    def scramble(self):
        with open(self.input_filename) as reader, open(self.output_filename, 'w') as writer:
            for line in reader:
                writer.write(self._scrambleline(line))
        assert os.path.getsize(self.input_filename) == os.path.getsize(self.output_filename)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Syntax error.\nPlease use the following arguments: <input_filename> <output_filename>', file=sys.stderr)
        sys.exit(1)
    WordScrambler(sys.argv[1], sys.argv[2]).scramble()
