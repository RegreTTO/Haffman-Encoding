import math
from queue import PriorityQueue, Queue
from collections import Counter
import sys

from config.cfg import ROUND_PRECISION


class Node:
    def __init__(self, data: str, prob: float, next: list, char=None) -> None:
        self.data = data
        self.prob = prob
        self.parents = next
        self.char = char

    def __lt__(self, other):
        return self.prob < other.prob

    def __str__(self) -> str:
        return f"data: {self.data}, char: {self.char}, prob: {self.prob}, parents: {self.parents}"


class EncodeData:
    def __init__(self, data, table) -> None:
        self.data = data
        self.table = table


def encode(data: str) -> EncodeData:
    counter = Counter(data)
    pq = PriorityQueue()
    for k, v in counter.items():
        p = round(v / len(data), ROUND_PRECISION)
        pq.put(Node("", p, [None, None], char=k))

    while pq.qsize() > 2:
        a: Node = pq.get()
        b: Node = pq.get()
        c = a.prob + b.prob
        c = round(c, ROUND_PRECISION)
        new_node = Node("", c, [a, b])
        pq.put(new_node)
    a: Node = pq.get()
    b: Node = pq.get()
    a.data = "0"
    b.data = "1"
    q = Queue()
    q.put(b)
    q.put(a)
    nodes = []
    while not q.empty():
        this: Node = q.get()
        p1: Node
        p2: Node
        p1, p2 = this.parents
        if p1 is None and p2 is None:
            nodes.append(this)
            continue
        if p1 is not None:
            p1.data = this.data + "1"
            q.put(p1)
        if p2 is not None:
            p2.data = this.data + "0"
            q.put(p2)

    assert len(nodes) == len(counter)
    per_sym_av = 0
    entropy = 0
    table = {}
    for node in nodes:
        node: Node
        per_sym_av += node.prob * len(node.data)
        entropy += node.prob * math.log2(node.prob)
        table[node.char] = node.data

    per_sym_av = round(per_sym_av, ROUND_PRECISION)
    entropy = -round(entropy, ROUND_PRECISION)
    encoded_data = ""
    for ch in data:
        encoded_data += table[ch]
    print(
        f"Entropy: {entropy}\n\
Per-symbol signal average: {per_sym_av}\n\
Compression ratio: {len(encoded_data) / (len(data)*8)}"
    )
    return EncodeData(encoded_data, table)
