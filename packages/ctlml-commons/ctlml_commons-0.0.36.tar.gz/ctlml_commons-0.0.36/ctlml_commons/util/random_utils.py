import random
import uuid
from typing import Any, Optional, Sequence, Set
from uuid import UUID


def random_float(end: float, start: float = 0.0):
    return random.uniform(start, end)


# TODO: deprecate in favor of random_unique_items
def get_unique_randoms(iterable: Sequence, count: int) -> Set[str]:
    return set([i.symbol for i in list(random_unique_items(iterable=iterable, count=count))])


def random_unique_items(iterable: Sequence, count: int) -> Set[Any]:
    return set(random.choices(iterable, k=min(len(iterable), count)))

def random_unique_items(iterable: Sequence, count: int, subscript: Optional[bool] = False) -> Set[str]:
    values: Set[str] = set()
    num_items: int = min(len(iterable), count)

    while len(values) < num_items:
        values.add(random.choice(iterable))

    return values


def get_uuid() -> UUID:
    return uuid.uuid4()
