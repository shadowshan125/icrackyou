import datetime

class MutationEngine:
    def __init__(self, config):
        """
        Initialize the mutation engine.
        
        Args:
            config (dict): Configuration dictionary containing:
                - mutations: dict of bools (upper, lower, capitalize, leet, etc.)
                - prefixes: list of strings
                - suffixes: list of strings
        """
        self.config = config
        self.current_year = datetime.datetime.now().year
    
    def apply_case_transformations(self, word):
        """
        Yields case variations based on config.
        """
        # Always yield original first (assumed cleaner/filtered handled elsewhere, but good practice)
        # Actually caller might have original, but let's be inclusive.
        
        transforms = set()
        
        if self.config.get('lower'):
            transforms.add(word.lower())
            
        if self.config.get('upper'):
            transforms.add(word.upper())
            
        if self.config.get('capitalize'):
            transforms.add(word.capitalize())
            
        # "Smart" toggle case: e.g. "password" -> "Password", "PASSWORD" are covered.
        # Maybe inverse case? "pASSWORD".
        if self.config.get('inverse'):
            transforms.add(word.swapcase())
            
        return transforms

    def apply_years(self, word):
        """
        Yields year-based mutations.
        """
        years = [str(self.current_year), str(self.current_year + 1), str(self.current_year - 1)]
        # Common historical years if requested, but let's stick to recent/future for "smart"
        # Could add 123, 1, etc here or in suffix.
        return [word + y for y in years]

    def _generate_variations(self, word):
        """
        Core generator for a single base word.
        """
        # 1. Base transformations (Case)
        base_forms = set()
        base_forms.add(word) # Original
        base_forms.update(self.apply_case_transformations(word))
        
        # 2. Leetspeak (if enabled)
        # We apply leet to the *lowercase* version usually, or original.
        if self.config.get('leet'):
            from utils.leet import LeetSpeak
            # Generate leet versions of the unique base forms
            leet_forms = set()
            for form in list(base_forms):
                for leet_word in LeetSpeak.generate_substitutions(form):
                    leet_forms.add(leet_word)
            base_forms.update(leet_forms)

        # 3. Prefixes and Suffixes
        # These are multiplicative.
        prefixes = self.config.get('prefix', []) or []
        suffixes = self.config.get('suffix', []) or []
        
        # Add numeric/symbol suffixes if generic flags set
        if self.config.get('numbers'):
            # Smart numbers
            suffixes.extend(['1', '123', '123456', '01', '007'])
            suffixes.extend([str(self.current_year), str(self.current_year -1)])
            
        if self.config.get('symbols'):
            # Smart symbols
            suffixes.extend(['!', '@', '#', '*', '?!'])
            # Prefixes usually less common for symbols but possible for @user
            # prefixes.extend(['@', '#']) # Let's keep prefixes explicit from user or minimal

        # Dedupe p/s
        prefixes = sorted(list(set(prefixes)))
        suffixes = sorted(list(set(suffixes)))

        # Now combinations
        # Order: Prefix + [Base] + Suffix
        
        for form in base_forms:
            # Yield base form itself (if no mandatory prefix/suffix enforcement logic)
            yield form
            
            # Form + Suffix
            for s in suffixes:
                yield f"{form}{s}"
            
            # Prefix + Form
            for p in prefixes:
                yield f"{p}{form}"
                
                # Prefix + Form + Suffix
                for s in suffixes:
                    yield f"{p}{form}{s}"

    def process(self, words_generator):
        """
        Yields all mutated words from the input generator.
        """
        for word in words_generator:
            yield from self._generate_variations(word)
