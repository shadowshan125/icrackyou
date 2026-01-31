#!/usr/bin/env python3
import argparse
import sys
import os
import signal

# Ensure we can import modules from current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engine.dictionary import DictionaryLoader
from engine.mutations import MutationEngine
from engine.filters import FilterEngine
from utils.progress import ProgressBar

try:
    import yaml
except ImportError:
    yaml = None

def load_config(config_path):
    if not config_path or not os.path.exists(config_path):
        return {}
    if not yaml:
        print("Warning: PyYAML not installed. Config file ignored.", file=sys.stderr)
        return {}
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Error loading config: {e}", file=sys.stderr)
        return {}

def main():
    parser = argparse.ArgumentParser(
        description="icrackyou - Intelligent Wordlist Generator",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""Example:
  icrackyou --dict rockyou.txt --capitalize --numbers --suffix 2024 --limit 10000"""
    )

    # Input/Output
    parser.add_argument("--dict", "-d", nargs='+', help="Path to dictionary file(s). Use '-' for stdin.")
    parser.add_argument("--output", "-o", help="Output file path. Defaults to stdout.")
    parser.add_argument("--config", "-c", help="Path to YAML config file.")

    # Mutations
    mut_group = parser.add_argument_group("Mutations")
    mut_group.add_argument("--lower", action="store_true", help="Convert to lowercase")
    mut_group.add_argument("--upper", action="store_true", help="Convert to uppercase")
    mut_group.add_argument("--capitalize", action="store_true", help="Capitalize first letter")
    mut_group.add_argument("--inverse", action="store_true", help="Inverse case (pASSWORD)")
    mut_group.add_argument("--numbers", action="store_true", help="Append smart numbers")
    mut_group.add_argument("--symbols", action="store_true", help="Append smart symbols")
    mut_group.add_argument("--leet", action="store_true", help="Apply leetspeak mutations")
    
    # Custom Prefix/Suffix
    ps_group = parser.add_argument_group("Prefix & Suffix")
    ps_group.add_argument("--prefix", nargs='+', default=[], help="Add specific prefix(es)")
    ps_group.add_argument("--suffix", nargs='+', default=[], help="Add specific suffix(es)")

    # Filters
    filt_group = parser.add_argument_group("Filters")
    filt_group.add_argument("--min-length", type=int, default=0, help="Minimum length")
    filt_group.add_argument("--max-length", type=int, default=999, help="Maximum length")
    filt_group.add_argument("--limit", type=int, default=0, help="Max words to generate (0 = unlimited)")

    args = parser.parse_args()

    # Handle interrupt
    def signal_handler(sig, frame):
        sys.stderr.write("\nInterrupted by user.\n")
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    # Load config
    config = load_config(args.config)
    
    # CLI args override config
    # We construct a consolidated config dictionary
    run_config = config.copy()
    
    # Update boolean flags if set in CLI (CLI takes precedence if True)
    for flag in ['lower', 'upper', 'capitalize', 'inverse', 'numbers', 'symbols', 'leet']:
        if getattr(args, flag):
            run_config[flag] = True
    
    # Extend lists
    if 'prefix' not in run_config: run_config['prefix'] = []
    if 'suffix' not in run_config: run_config['suffix'] = []
    
    run_config['prefix'].extend(args.prefix)
    run_config['suffix'].extend(args.suffix)
    
    # Update filters
    if args.min_length != 0: run_config['min_length'] = args.min_length
    if args.max_length != 999: run_config['max_length'] = args.max_length
    if args.limit != 0: run_config['limit'] = args.limit

    # Setup Components
    # If no dict specified, use internal default unless explicitly empty? 
    # Logic: if args.dict is provided, use it. If not, check config? 
    # If nothing, use internal.
    loader = DictionaryLoader(args.dict, use_internal=(args.dict is None))
    mutator = MutationEngine(run_config)
    filter_engine = FilterEngine(run_config)
    
    # Output stream
    out_file = sys.stdout
    if args.output:
        try:
            out_file = open(args.output, 'w', encoding='utf-8')
        except Exception as e:
            sys.stderr.write(f"Error opening output file: {e}\n")
            sys.exit(1)

    # Pipeline Execution
    # Loader -> Mutator -> Filter -> Output
    
    raw_words = loader.load_words()
    mutated_words = mutator.process(raw_words)
    final_words = filter_engine.filter(mutated_words)
    
    progress = ProgressBar(desc="Generating")
    
    try:
        for word in final_words:
            out_file.write(word + '\n')
            progress.update()
    except BrokenPipeError:
        # Handle pipe closed (e.g. | head)
        sys.stderr.close()
    finally:
        progress.close()
        if args.output and out_file is not sys.stdout:
            out_file.close()

if __name__ == "__main__":
    main()
