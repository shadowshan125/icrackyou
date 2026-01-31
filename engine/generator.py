import itertools
import string

class PatternGenerator:
    def __init__(self, pattern):
        """
        Initialize Pattern Generator.
        
        Pattern Syntax (Crunch-style):
            @ : lower case alpha characters
            , : upper case alpha characters
            % : numeric characters
            ^ : symbol characters
        """
        self.pattern = pattern
        self.char_sets = {
            '@': string.ascii_lowercase,
            ',': string.ascii_uppercase,
            '%': string.digits,
            '^': string.punctuation
        }

    def _parse_pattern(self):
        """
        Parses the pattern into a list of character sets.
        Ex: "abc%" -> [['a'], ['b'], ['c'], ['0'..'9']]
        """
        slots = []
        for char in self.pattern:
            if char in self.char_sets:
                slots.append(list(self.char_sets[char]))
            else:
                # Literal character
                slots.append([char])
        return slots

    def generate(self):
        """
        Yields words matching the pattern.
        """
        if not self.pattern:
            return

        slots = self._parse_pattern()
        
        # itertools.product(*slots) generates the cartesian product equivalent to nested loops
        # This handles the combinatorics efficiently
        for combination in itertools.product(*slots):
            yield "".join(combination)
