from config.cfg import TABLE_STREAM
import re

def decode(data: str, table_raw:str) -> str:
    if re.match(r"[01]+", data) is None:
        raise ValueError("Input data must be a binary code!")
    PATTERN = re.compile(r"(\w) -- (\d+)")
    table_match = re.findall(PATTERN, table_raw)
    table = {}
    for k, v in table_match:
        table[v] = k
    print("Used table: ")
    for k, v in table.items():
        print(f"{v} -- {k}")
    decoded = ""
    prefix = ""
    for ch in data:
        prefix += ch
        if prefix in table:
            decoded += table[prefix]
            prefix = ""
    return decoded