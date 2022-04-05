import os, json
from typing import Dict

def get_envvars() -> Dict[str, str]:
    vars = {}
    for var in [
            "MONGO_URL", 
            "MONGO_USER",
            "MONGO_PASSWORD"
            ]:
        vars[var] = os.environ[var]

    return vars

def encode_opt(
        value: str,
        kind: str
        ) -> str:
    with open(f"codes/{kind}.json") as f:
        codes = json.load(f)

    return codes[value]

def decode_opt(
        value: str,
        kind: str
        ) -> str:
    with open(f"codes/{kind}.json") as f:
        codes = json.load(f)

    icodes = {val: key for key, val in codes.items()}
    return icodes[value]

