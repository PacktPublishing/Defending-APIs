"""
Chapter 6 - Passive discovery.
Generates Google/GHDB-style "dork" queries for locating exposed API artefacts.
No requests are made -- this only builds the search strings.
"""

DORKS = [
    'inurl:"/api/v1" filetype:json',
    'inurl:swagger.json',
    'intitle:"index of" "openapi.yaml"',
    'site:{domain} inurl:api',
    '"api_key" ext:env',
]


def build(domain: str) -> list[str]:
    return [d.format(domain=domain) if "{domain}" in d else d for d in DORKS]


if __name__ == "__main__":
    for q in build("example.com"):
        print(q)
