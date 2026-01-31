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

### Pattern Generation (Crunch-Style)
Generate words based on a mask (ignore dictionary):
```bash
./icrackyou.py -p "admin%%%%" -o pins.txt
# Generates admin0000 to admin9999
```

### CLI Options

| Flag | Description |
|------|-------------|
| `-d`, `--dict` | Input dictionary file(s) or `-` for stdin |
| `-p`, `--pattern` | Crunch-style pattern (@, %, ^) |
| `-o`, `--output` | Output file path (default: stdout) |
| `-c`, `--config` | Path to YAML config file |
| `-l`, `--lower` | Convert to lowercase |
| `-u`, `--upper` | Convert to uppercase |
| `--capital` | Capitalize first letter |
| `-n`, `--numbers` | Append smart number sequences (years, 123, etc.) |
| `-s`, `--symbols` | Append common symbol suffixes |
| `--leet` | Apply leetspeak substitutions |
| `-min`, `--min-length` | Minimum word length |
| `-max`, `--max-length` | Maximum word length |
| `--limit` | Hard limit on generated words |
| `--require-numbers` | Content Policy: Output MUST contain a number |
| `--require-symbols` | Content Policy: Output MUST contain a symbol |

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
