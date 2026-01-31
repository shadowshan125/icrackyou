class FilterEngine:
    def __init__(self, config):
        """
        Initialize filter engine.
        Args:
            config (dict):
                - min_length (int)
                - max_length (int)
                - limit (int)
                - require_numbers (bool)
                - require_symbols (bool)
                - require_upper (bool)
        """
        self.min_length = config.get('min_length', 0)
        self.max_length = config.get('max_length', 999)
        self.limit = config.get('limit', 0)
        
        self.require_numbers = config.get('require_numbers', False)
        self.require_symbols = config.get('require_symbols', False)
        self.require_upper = config.get('require_upper', False)
        
        self.count = 0
        self.seen = set()

    def filter(self, word_generator):
        """
        Yields words that pass filters.
        """
        import re
        # Pre-compile regexes for performance
        re_num = re.compile(r'\d') if self.require_numbers else None
        re_sym = re.compile(r'[!@#$%^&*(),.?":{}|<>]') if self.require_symbols else None
        # Upper check can stick to string method or regex, regex usually fine here.
        re_upper = re.compile(r'[A-Z]') if self.require_upper else None

        for word in word_generator:
            if self.limit > 0 and self.count >= self.limit:
                return

            if len(word) < self.min_length:
                continue
            
            if len(word) > self.max_length:
                continue

            # Policy Checks
            if re_num and not re_num.search(word):
                continue
            if re_sym and not re_sym.search(word):
                continue
            if re_upper and not re_upper.search(word):
                continue

            if word in self.seen:
                continue
            
            self.seen.add(word)
            self.count += 1
            yield word
