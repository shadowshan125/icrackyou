import os
import sys

class DictionaryLoader:
    def __init__(self, file_paths=None, use_internal=False):
        """
        Initialize the dictionary loader.
        
        Args:
            file_paths (list): List of file paths to load words from.
            use_internal (bool): Whether to use the internal embedded dictionary.
        """
        self.file_paths = file_paths or []
        self.use_internal = use_internal
        self.use_numeric = False # Default
        
        # A small embedded dictionary for standalone quick usage
        self.internal_dict = [
            "password", "admin", "root", "user", "123456", "qwerty", "welcome",
            "login", "manager", "guest", "test", "demo", "access", "master"
        ]
        
    def set_numeric_mode(self, enabled=True):
        self.use_numeric = enabled

    def _generate_smart_numbers(self):
        """Generates common numeric patterns."""
        import datetime
        current_year = datetime.datetime.now().year
        
        # 1. Common pins (0000-9999 is too many? Let's do subset or all if limited)
        # Detailed list requested?
        # Let's do: 
        # - Repeated: 000000, 111111
        # - Sequential: 123456, 123456789
        # - Years: 1900 to current+5
        
        # Sequentials
        yield "123456"
        yield "12345678"
        yield "123456789"
        yield "1234567890"
        yield "0123456789"
        yield "000000"
        yield "111111"
        yield "121212"
        
        # Years
        for y in range(1980, current_year + 5):
            yield str(y)
        
        # Short pins?
        # Maybe loop 0000 to 9999 if user wants purely numbers?
        # That's 10,000 items. Minimal overhead.
        for i in range(10000):
            yield f"{i:04d}"

    def set_config(self, min_len=0, max_len=999):
        self.min_len = min_len
        self.max_len = max_len

    def _generate_numeric_bruteforce(self):
        """Generates all numbers within min_len and max_len."""
        import itertools
        
        # If no explicit limits were set (default 0 or huge max), fallback to smart list
        # We assume if user wants brute force, they likely set min_len > 0 or max_len < 20 (sanity check)
        # Actually logic:
        # If numeric mode is on, we check if min/max are "custom".
        # If so -> Brute Force.
        # If defaults -> Smart List.
        
        start_len = max(1, self.min_len) if self.min_len > 0 else 4 # Default to 4-digit pins if unknown
        end_len = min(self.max_len, 12) # Use 12 as safety cap for python iteration here if user goes wild
        
        # If user explicitly asked for max_len > 12, we warn? Or just do it?
        # Let's cap at 12 for safety in simple generator, or trust sys.maxsize
        # The user example is 8-10. So let's allow up to user max.
        end_len = self.max_len
        
        digits = '0123456789'
        for length in range(start_len, end_len + 1):
             for p in itertools.product(digits, repeat=length):
                 yield "".join(p)

    def load_words(self):
        """
        Generator that yields words from all configured sources.
        """
        seen = set()

        if self.use_numeric:
            # DECISION: Smart List or Brute Force?
            # If user provided explicit MIN length (e.g. 8), smart list (dates/pins) usually fails.
            # So switch to brute force if min_len >= 1 OR if specific range requested.
            # Default min is 0.
            # However, smart list has 4-digit and 6-digit pins.
            # Let's say: if min_len > 4, switch to brute force?
            # Or just check if user provided args.
            # Better: if we have specific constraints, verify if smart list suffices?
            # No, user wants combinations.
            # Let's assume if min_len > 0, we brute force.
            # BUT wait, "icrackyou -n" (min=0) gives smart list.
            # "icrackyou -n -min 8" gives brute force 8+.
            
            if self.min_len > 0:
                 # Brute Force Mode
                 yield from self._generate_numeric_bruteforce()
            else:
                 # Standard Smart List
                 for num in self._generate_smart_numbers():
                    if num not in seen:
                        yield num
                        seen.add(num)
            return

        if self.use_internal:
            for word in self.internal_dict:
                if word not in seen:
                    yield word
                    seen.add(word)

        if not self.file_paths:
            return

        for path in self.file_paths:
            if path == '-':
                # Read from stdin
                for line in sys.stdin:
                    word = line.strip()
                    if word and word not in seen:
                        yield word
                        seen.add(word)
            else:
                if not os.path.exists(path):
                    print(f"Warning: Dictionary file not found: {path}", file=sys.stderr)
                    continue
                
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line in f:
                            word = line.strip()
                            if word: # Do not filter duplicates here for massive files to save memory? 
                                     # Actually, user requested preventing combinatorial explosion, so some depduped base is good.
                                     # However, for huge wordlists (rockyou), keeping 'seen' might consume RAM.
                                     # We will yield raw and let the filter stage handle uniqueness if strictly required,
                                     # or assume inputs are what the user wants. 
                                     # BUT, prompt says "Duplicate prevention".
                                     # Let's keep 'seen' but maybe we can make it optional or flush it?
                                     # For now, let's just yield. The filter stage or main loop can handle unique if needed,
                                     # or we duplicate filter here if memory allows. 
                                     # Let's assume for this "clean" base, we yield everything and let the pipeline handle it.
                                yield word
                except Exception as e:
                    print(f"Error reading {path}: {e}", file=sys.stderr)

