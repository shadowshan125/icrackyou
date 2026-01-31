class LeetSpeak:
    """
    Handles leetspeak character substitutions.
    """
    
    COMMON_LEET = {
        'a': ['4', '@'],
        'b': ['8'],
        'e': ['3'],
        'g': ['6', '9'],
        'i': ['1', '!'],
        'l': ['1', '!'],
        'o': ['0'],
        's': ['5', '$'],
        't': ['7', '+'],
        'z': ['2']
    }

    @staticmethod
    def generate_substitutions(word):
        """
        Generates leetspeak variations for a given word.
        This is a generator that yields variations.
        
        Note: To avoid explosion, we can implement levels.
        For now, we will implement a basic randomizer or exhaustive for smartlist.
        
        For a non-brute force tool, we probably just want to return ONE or TWO common variations,
        or all simple single-char substitutions.
        """
        # For simplicity and "smart" behavior, we might return:
        # 1. The word with ALL common leet subs (e.g. password -> p@ssw0rd)
        # 2. Key single char subs.
        
        # Strategy: Return a "heavy" leet version and a "light" leet version if possible.
        # But for iteration, let's just do a standard comprehensive map.
        
        chars = list(word)
        indices = [i for i, c in enumerate(chars) if c.lower() in LeetSpeak.COMMON_LEET]
        
        if not indices:
            return

        # Simple approach: "Basic" leet (all chars replaced)
        # This is deterministic and "smart" rather than "all combinations"
        
        # Variation 1: Replace all occurrences
        leet_all = list(chars)
        for i in indices:
            char = leet_all[i].lower()
            if char in LeetSpeak.COMMON_LEET:
                leet_all[i] = LeetSpeak.COMMON_LEET[char][0] # Pick primary
        yield "".join(leet_all)
        
        # Variation 2: Replace only vowels/numbers if applicable (Light)
        # For now, let's add a few random patterns if we wanted, but deterministic is better for this tool.
        
        # Variation 3: Alternative symbols for common chars
        leet_alt = list(chars)
        changed = False
        for i in indices:
            char = leet_alt[i].lower()
            subs = LeetSpeak.COMMON_LEET[char]
            if len(subs) > 1:
                leet_alt[i] = subs[1]
                changed = True
            else:
                 leet_alt[i] = subs[0] # Fallback
        
        res_alt = "".join(leet_alt)
        if res_alt != "".join(leet_all):
             yield res_alt
