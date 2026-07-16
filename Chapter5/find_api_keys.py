"""
Chapter 5 - Finding API keys.
Regex scanner that flags secrets accidentally committed to source (a common recon win).
"""
import re
import sys

PATTERNS = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "Generic API key": r"(?i)api[_-]?key['\"]?\s*[:=]\s*['\"][0-9a-zA-Z]{16,}['\"]",
    "JWT": r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",
    "Slack token": r"xox[baprs]-[0-9A-Za-z-]{10,}",
}

SAMPLE = '''
    api_key = "abcd1234efgh5678ijkl"
    aws = "AKIAIOSFODNN7EXAMPLE"
    token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIn0.sig"
'''


def scan(text: str) -> list[tuple[str, str]]:
    hits = []
    for name, pat in PATTERNS.items():
        for m in re.findall(pat, text):
            hits.append((name, m if isinstance(m, str) else m[0]))
    return hits


if __name__ == "__main__":
    data = open(sys.argv[1]).read() if len(sys.argv) > 1 else SAMPLE
    for name, val in scan(data):
        print(f"[!] {name}: {val}")
