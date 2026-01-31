#!/usr/bin/env python3
import argparse
import sys
import os
import signal
import time

# Ensure we can import modules from current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engine.dictionary import DictionaryLoader
from engine.mutations import MutationEngine
from engine.filters import FilterEngine
from engine.generator import PatternGenerator
from utils.progress import ProgressBar

try:
    import yaml
except ImportError:
    yaml = None

# --- ANSI Colors for Kali Style ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Safe ASCII Banner construction
BANNER_ASCII = r"""
  _                _     
 (_) ___ _ __ __ _| | _____   _  ___  _   _ 
 | |/ __| '__/ _` | |/ / \ \ / / _ \| | | |
 | | (__| | | (_| |   <| |\ V / (_) | |_| |
 |_|\___|_|  \__,_|_|\_\_| \_/ \___/ \__,_|
                                           """ 
BANNER = Colors.FAIL + BANNER_ASCII + Colors.ENDC + "\n" + Colors.CYAN + "    >> Intelligent Wordlist Generator <<" + Colors.ENDC + "\n"

def load_config(config_path):
    if not config_path or not os.path.exists(config_path):
        return {}
    if not yaml:
        return {}
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"{Colors.WARNING}Error loading config: {e}{Colors.ENDC}", file=sys.stderr)
        return {}

def print_summary(source_desc, run_config):
    """Prints a configuration summary."""
    print(f"{Colors.HEADER}[+] Configuration Summary:{Colors.ENDC}", file=sys.stderr)
    print(f"    {Colors.BOLD}Source:{Colors.ENDC}      {source_desc}", file=sys.stderr)
    
    if run_config.get('pattern'):
         print(f"    {Colors.BOLD}Pattern:{Colors.ENDC}     {Colors.CYAN}{run_config['pattern']}{Colors.ENDC}", file=sys.stderr)
    
    mutations = []
    if run_config.get('lower'): mutations.append("Lowercase")
    if run_config.get('upper'): mutations.append("Uppercase")
    if run_config.get('capitalize'): mutations.append("Capitalize")
    if run_config.get('inverse'): mutations.append("Inverse")
    if run_config.get('numbers'): mutations.append("Smart Numbers")
    if run_config.get('symbols'): mutations.append("Smart Symbols")
    if run_config.get('leet'): mutations.append("Leetspeak")
    if run_config.get('reverse'): mutations.append("Reverse")
    if run_config.get('repeat'): mutations.append("Repeat")
    if run_config.get('sandwich'): mutations.append("Sandwich")
    
    mut_str = ", ".join(mutations) if mutations else "None"
    print(f"    {Colors.BOLD}Mutations:{Colors.ENDC}   {Colors.GREEN}{mut_str}{Colors.ENDC}", file=sys.stderr)
    
    prefixes = run_config.get('prefix', []) or []
    suffixes = run_config.get('suffix', []) or []
    if prefixes:
        print(f"    {Colors.BOLD}Prefixes:{Colors.ENDC}    {', '.join(prefixes)}", file=sys.stderr)
    if suffixes:
        print(f"    {Colors.BOLD}Suffixes:{Colors.ENDC}    {', '.join(suffixes)}", file=sys.stderr)
        
    limits = []
    min_len = run_config.get('min_length', 0)
    max_len = run_config.get('max_length', 999)
    limit_count = run_config.get('limit', 0)
    
    if min_len > 0: limits.append(f"MinLen: {min_len}")
    if max_len < 999: limits.append(f"MaxLen: {max_len}")
    if limit_count > 0: limits.append(f"CountLimit: {limit_count}")
    
    # Policies
    if run_config.get('require_numbers'): limits.append("Must have Number")
    if run_config.get('require_symbols'): limits.append("Must have Symbol")
    if run_config.get('require_upper'): limits.append("Must have Upper")

    limit_str = ", ".join(limits) if limits else "No Limits"
    print(f"    {Colors.BOLD}Filters:{Colors.ENDC}     {Colors.WARNING}{limit_str}{Colors.ENDC}", file=sys.stderr)
    print(f"{Colors.BLUE}{'-'*60}{Colors.ENDC}", file=sys.stderr)

def main():
    if len(sys.argv) == 1:
        print(BANNER, file=sys.stderr)
        print(f"{Colors.BOLD}Usage:{Colors.ENDC} icrackyou -d <file> [options]", file=sys.stderr)
        print(f"Try {Colors.CYAN}--help{Colors.ENDC} for details.", file=sys.stderr)
        sys.exit(0)

    # Use single dash prefix logic if possible, or just add them as aliases.
    # argparse allows adding "-min" directly.
    parser = argparse.ArgumentParser(
        description="icrackyou - Intelligent Wordlist Generator",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=f"""{Colors.BOLD}Examples:{Colors.ENDC}
  icrackyou -d rockyou.txt -n -max 10
  icrackyou -p admin%%%% -s"""
    )

    # Input/Output
    # Supporting both -d and --dict, -p and --pattern
    parser.add_argument("-d", "--dict", nargs='+', help="Dictionary file(s) or '-' for stdin")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("-c", "--config", help="Config file")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode")
    
    # Pattern (Crunch-like)
    parser.add_argument("-p", "--pattern", help="Generate from pattern (@,%%,^)")

    # Mutations (Short and Long)
    mut_group = parser.add_argument_group("Mutations & Enforcements")
    mut_group.add_argument("-l", "--lower", action="store_true", help="Convert to lowercase and REQUIRE lowercase in output")
    mut_group.add_argument("-u", "--upper", action="store_true", help="Convert to uppercase and REQUIRE uppercase in output")
    mut_group.add_argument("--capital", dest="capitalize", action="store_true", help="Capitalize first letter")
    mut_group.add_argument("--inverse", action="store_true", help="Inverse case")
    mut_group.add_argument("-n", "--numbers", action="store_true", help="Append smart numbers and REQUIRE number in output")
    mut_group.add_argument("-s", "--symbols", action="store_true", help="Append smart symbols and REQUIRE symbol in output")
    mut_group.add_argument("--leet", action="store_true", help="Apply leetspeak mutations")
    # Extended
    mut_group.add_argument("--reverse", action="store_true", help="Add reversed words (admin -> nimda)")
    mut_group.add_argument("--repeat", action="store_true", help="Add repeated words (admin -> adminadmin)")
    mut_group.add_argument("--sandwich", action="store_true", help="Add sandwich mutations (123admin123)")
    
    # Prefix/Suffix
    ps_group = parser.add_argument_group("Prefix & Suffix")
    ps_group.add_argument("--prefix", nargs='+', default=[], help="Add prefixes")
    ps_group.add_argument("--suffix", nargs='+', default=[], help="Add suffixes")

    # Filters (Single dash support requested: -min, -max)
    filt_group = parser.add_argument_group("Filters")
    filt_group.add_argument("-min", "--min-length", dest="min_length", type=int, default=0, help="Min length")
    filt_group.add_argument("-max", "--max-length", dest="max_length", type=int, default=999, help="Max length")
    filt_group.add_argument("--limit", type=int, default=0, help="Hard limit")
    
    # Policies
    pol_group = parser.add_argument_group("Policies")
    pol_group.add_argument("--require-numbers", action="store_true", help="Output MUST contain a number")
    pol_group.add_argument("--require-symbols", action="store_true", help="Output MUST contain a symbol")
    pol_group.add_argument("--require-upper", action="store_true", help="Output MUST contain an uppercase letter")
    pol_group.add_argument("--require-lower", action="store_true", help="Output MUST contain a lowercase letter")

    args = parser.parse_args()

    # Handle interrupt
    def signal_handler(sig, frame):
        sys.stderr.write(f"\n{Colors.FAIL}[!] Interrupted.{Colors.ENDC}\n")
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    if not args.quiet:
        print(BANNER, file=sys.stderr)

    config = load_config(args.config)
    run_config = config.copy()
    
    # Sync Flags
    for flag in ['lower', 'upper', 'capitalize', 'inverse', 'numbers', 'symbols', 'leet', 'reverse', 'repeat', 'sandwich']:
        if getattr(args, flag):
            run_config[flag] = True
            
            # STRICT MODE: If user asks for X, enforce X in output.
            if flag == 'numbers': run_config['require_numbers'] = True
            if flag == 'symbols': run_config['require_symbols'] = True
            if flag == 'upper': run_config['require_upper'] = True
            if flag == 'lower': run_config['require_lower'] = True
    
    # Update Policies (Explicit flags still work)
    for flag in ['require_numbers', 'require_symbols', 'require_upper', 'require_lower']: # Added require_lower here
        if getattr(args, flag):
            run_config[flag] = True

    # Sync Others
    if 'prefix' not in run_config: run_config['prefix'] = []
    if 'suffix' not in run_config: run_config['suffix'] = []
    run_config['prefix'].extend(args.prefix)
    run_config['suffix'].extend(args.suffix)
    if args.min_length != 0: run_config['min_length'] = args.min_length
    if args.max_length != 999: run_config['max_length'] = args.max_length
    if args.limit != 0: run_config['limit'] = args.limit
    
    if args.pattern:
        run_config['pattern'] = args.pattern

    # DECIDE MODE: Dictionary or Pattern?
    # If pattern is present, we use PatternGenerator as the source.
    # We can still apply mutations (like appending suffix) to the generated patterns!
    
    if args.pattern:
        source_desc = f"Pattern: {args.pattern}"
        generator = PatternGenerator(args.pattern).generate()
    else:
        # Default Dictionary Mode
        source_desc = "Internal Dictionary"
        use_internal = (args.dict is None)
        
        # SMART GENERATION MODE check
        # If no dict provided, check which "Character Flags" are set.
        # Flags: -n (numbers), -l (lower), -u (upper), -s (symbols)
        # If ANY of these are set, we assume user wants to generate combinations of those chars.
        
        char_flags = []
        if args.numbers: char_flags.append('numbers')
        if args.lower: char_flags.append('lower')
        if args.upper: char_flags.append('upper')
        if args.symbols: char_flags.append('symbols')
        
        # Condition: No dict AND at least one char flag set
        is_generation_request = (args.dict is None and len(char_flags) > 0)
        
        loader = DictionaryLoader(args.dict, use_internal=use_internal)
        
        if is_generation_request:
            # Build Charset
            import string
            charset = ""
            desc_parts = []
            
            if args.numbers: 
                charset += string.digits
                desc_parts.append("Numbers")
            if args.lower: 
                charset += string.ascii_lowercase
                desc_parts.append("Lower")
            if args.upper: 
                charset += string.ascii_uppercase
                desc_parts.append("Upper")
            if args.symbols: 
                charset += string.punctuation
                desc_parts.append("Symbols")
            
            desc_str = "+".join(desc_parts)
            
            # Numeric Smart Mode Special Case:
            # If ONLY numbers are requested AND min_len is default (0), we usually prefer the Smart List (Years/Pins).
            # But if min_len > 0 is set, user wants brute force 000..999.
            # If Letters/Symbols are involved, we ALWAYS brute force (no "smart list" for letters yet).
            
            is_pure_numeric_smart = (len(char_flags) == 1 and args.numbers and args.min_length == 0)
            
            if is_pure_numeric_smart:
                 source_desc = "Smart Numeric Generator"
                 loader.set_numeric_mode(True)
                 loader.set_config(min_len=0, max_len=args.max_length)
            else:
                 # Generalized Brute Force
                 source_desc = f"Brute Force Generator [{desc_str}]"
                 loader.set_numeric_mode(True) # Reusing this flag to skip dict
                 loader.set_config(min_len=args.min_length, max_len=args.max_length, charset=charset)

        if args.dict:
            if args.dict == ['-']:
                source_desc = "Stdin"
            else:
                source_desc = f"Files: {len(args.dict)}"
                
        generator = loader.load_words()

    if not args.quiet:
        print_summary(source_desc, run_config)
        time.sleep(1)
        
    # Pipeline: Generator -> Mutator -> Filter
    # Even patterns can be mutated (e.g. pattern "admin" + suffix "123")
    
    mutator = MutationEngine(run_config)
    filter_engine = FilterEngine(run_config)

    mutated_words = mutator.process(generator)
    final_words = filter_engine.filter(mutated_words)
    
    # Output loop
    
    out_file = sys.stdout
    if args.output:
        try:
            out_file = open(args.output, 'w', encoding='utf-8')
            if not args.quiet:
                print(f"{Colors.GREEN}[*] Output: {args.output}{Colors.ENDC}", file=sys.stderr)
        except Exception:
            sys.exit(1)

    progress = ProgressBar(desc=f"{Colors.BLUE}Gen{Colors.ENDC}")
    try:
         for word in final_words:
             out_file.write(word + '\n')
             progress.update()
    except BrokenPipeError:
        sys.stderr.close()
    finally:
        progress.close()
        if args.output and out_file is not sys.stdout:
            out_file.close()
        if not args.quiet:
             print(f"{Colors.GREEN}[+] Done.{Colors.ENDC}", file=sys.stderr)

if __name__ == "__main__":
    main()
