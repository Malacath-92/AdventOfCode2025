from collections import deque
from itertools import islice

def sliding_window(iterable, n):
    iterator = iter(iterable)
    window = deque(islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)
