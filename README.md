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
./icrackyou.py --upper --numbers --suffix 2024 --limit 1000
```

### Using RockYou or Custom Wordlist
```bash
./icrackyou.py --dict /usr/share/wordlists/rockyou.txt \
    --capitalize --numbers \
    --suffix 2025 \
    --min-length 8 --max-length 12 \
    --output targeted_list.txt
```

### Piping from CeWL
Chaining tools for targeted profiling:
```bash
cewl https://example.com -d 2 -w - | ./icrackyou.py --dict - --leet --symbols --output final_list.txt
```

### CLI Options

| Flag | Description |
|------|-------------|
| `--dict` | Input dictionary file(s) or `-` for stdin |
| `--output` | Output file path (default: stdout) |
| `--config` | Path to YAML config file |
| `--lower`, `--upper` | Enforce case transformations |
| `--capitalize` | Capitalize first letter (Smart) |
| `--inverse` | Inverse case (e.g., `pASSWORD`) |
| `--numbers` | Append smart number sequences (years, 123, etc.) |
| `--symbols` | Append common symbol suffixes |
| `--leet` | Apply leetspeak substitutions (e.g., `e` -> `3`) |
| `--prefix`, `--suffix` | Add custom prefixes/suffixes |
| `--min-length` | Minimum word length to filter |
| `--limit` | Hard limit on generated words |

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
