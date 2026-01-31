# icrackyou - Intelligent Wordlist Generator

**icrackyou** is a professional-grade, intelligent wordlist generator designed for offensive security engineers and authorized penetration testing. Unlike simple brute-force tools, `icrackyou` applies smart mutations, pattern matching, and human-behavior modeling to generate high-quality, targeted password lists without combinatorial explosion.

## 🚀 Features

*   **Smart Mutations**: Controlled case, numbers, symbols, and leetspeak transformations.
*   **Modular Engine**: Extendable architecture separate from the CLI.
*   **Kali Linux Integration**: Works seamlessly with `rockyou.txt`, `cewl`, and tools like `hydra` or `hashcat`.
*   **Safety Controls**: Built-in limits, duplicate prevention, and length filtering.
*   **Streaming**: Low memory footprint implementation for handling massive wordlists.

## 📦 Installation

`icrackyou` is a standalone Python 3 tool. No heavy dependencies required.

```bash
git clone https://github.com/shadowshan125/icrackyou
cd icrackyou
chmod +x icrackyou.py
```

*Optional*: Install `PyYAML` for config file support (tool works without it):
```bash
pip install pyyaml
```

## 🛠️ Usage

### Basic Example
Generate mutations from the internal dictionary:
```bash
./icrackyou.py -u -n --suffix 2024 --limit 1000
```

### Using RockYou or Custom Wordlist
```bash
./icrackyou.py -d /usr/share/wordlists/rockyou.txt \
    --capital -n \
    --suffix 2025 \
    -min 8 -max 12 \
    -o targeted_list.txt
```

### Strict Mode (Default)
When you use mutation flags like `-n` (numbers) or `-u` (uppercase), `icrackyou` **automatically strict-filters** the output.
*   `icrackyou -n` -> Generates words with numbers relative to input, and **filters out** any words that DO NOT have numbers.
*   `icrackyou -u` -> Generates uppercase variants and **filters out** non-uppercase results.

### Extended Mutations
Generate advanced password styles (Reverse, Repeat, Sandwich):
```bash
./icrackyou.py -d rockyou.txt --reverse --sandwich -n -o complex_list.txt
# Generates: nimda, 123admin123, !admin!
```

### Smart Numeric & Brute Force Mode
If you run `icrackyou` **without a dictionary**, it detects which character set you want based on flags.

**Numeric Mode:**
```bash
./icrackyou.py -n -o pins.txt
# Generates 0000-9999, years, and common pin codes.
```

**Full Brute Force Mode:**
Provide specific characters (`-l`, `-u`, `-n`, `-s`) and length constraints.
```bash
# Generate all lowercase letters length 1-3 (a...zzz)
./icrackyou.py -l -min 1 -max 3 -o letters.txt

# Generate alphanumeric (lower+numbers) length 4
./icrackyou.py -l -n -min 4 -max 4 -o codes.txt
```

### Pattern Generation (Crunch-Style)

### CLI Options

| Flag | Description |
|------|-------------|
| `-d`, `--dict` | Input dictionary file(s) or `-` for stdin |
| `-p`, `--pattern` | Crunch-style pattern (@, %, ^) |
| `-o`, `--output` | Output file path (default: stdout) |
| `-c`, `--config` | Path to YAML config file |
| `-l`, `--lower` | Convert to lower & **Filter for Lowercase** |
| `-u`, `--upper` | Convert to upper & **Filter for Uppercase** |
| `--capital` | Capitalize first letter |
| `-n`, `--numbers` | Append smart numbers & **Filter for Numbers** |
| `-s`, `--symbols` | Append smart symbols & **Filter for Symbols** |
| `--leet` | Apply leetspeak substitutions |
| `--reverse` | Reverse the word (admin -> nimda) |
| `--repeat` | Repeat the word (admin -> adminadmin) |
| `--sandwich` | Sandwich mutation (prefix+word+suffix mirroring) |
| `-min`, `--min-length` | Minimum word length |
| `-max`, `--max-length` | Maximum word length |
| `--limit` | Hard limit on generated words |
| `--require-numbers` | (Explicit) Content Policy: Output MUST contain a number |
| `--require-upper` | (Explicit) Content Policy: Output MUST contain Uppercase |

## ⚙️ Configuration

You can use a `config.yaml` instead of long CLI flags:

```yaml
# config/default.yaml
mutations:
  capitalize: true
  numbers: true
  leet: false

prefixes: ["admin", "root"]
suffixes: ["2024", "2025", "!"]

filters:
  min_length: 8
  limit: 500000
```

Run with: `python icrackyou.py --config config/default.yaml`

## 🚨 Ethical Use & Disclaimer

**icrackyou** is a security auditing tool.

*   **Authorized Use Only**: Use this tool ONLY on systems you own or have explicit written permission to audit.
*   **No Malicious Use**: The developers are not responsible for any misuse or illegal activities performed with this tool.
*   **Compliance**: Ensure you comply with all local, state, and international laws regarding cybersecurity and penetration testing.

---
*Created for the Advanced Agentic Coding Project.*
