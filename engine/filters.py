class FilterEngine:
    def __init__(self, config):
        """
        Initialize filter engine.
        
        Args:
            config (dict):
                - min_length (int)
                - max_length (int)
                - limit (int): Hard limit on count
        """
        self.min_length = config.get('min_length', 0)
        self.max_length = config.get('max_length', 999)
        self.limit = config.get('limit', 0)
        self.count = 0
        self.seen = set() # For uniqueness check

    def filter(self, word_generator):
        """
        Yields words that pass filters.
        """
        for word in word_generator:
            if self.limit > 0 and self.count >= self.limit:
                return

            if len(word) < self.min_length:
                continue
            
            if len(word) > self.max_length:
                continue

            if word in self.seen:
                continue
            
            self.seen.add(word)
            self.count += 1
            yield word
