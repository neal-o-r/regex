from typing import List, Generator
from itertools import zip_longest


def zip_left(a: str, b: str) -> Generator[tuple, None, None]:
    """
    zip to the length of left arg,
    padding right arg with None
    """
    if len(a) <= len(b):
        return zip(a, b)
    else:
        return zip_longest(a, b)


def eq(r: str, t: str) -> bool:
    """
    does a regex char match a text star?
    """
    return (
        (r == t)  # chars match
        or (r is ".")  # wild card char
        or ((r is "$") and (t is None))  # end anchor
    )


def suffixes(text: str) -> Generator[str, None, None]:
    """
    get all suffixes of a string
    """
    return (text[i:] for i in range(len(text)))


def expand_star(regex: str, text: str) -> Generator[str, None, None]:
    """
    re-write a regex, replacing * with .'s
    """
    front, back = regex.split("*")
    n = 2 + (len(text) - len(regex))
    for i in range(n):
        yield f"{front}{'.' * i}{back}"


def match_here(regex: str, text: str) -> bool:
    """
    do all regex chars match a string at this location?
    """
    return all(eq(r, t) for r, t in zip_left(regex, text))


def match(regex: str, text: str) -> bool:
    if "*" in regex:
        # expand a star, if there is one
        return any(match(exp, text) for exp in expand_star(regex, text))
    elif regex.startswith("^"):
        # if it starts with an anchor, check if matches here
        return match_here(regex[1:], text)
    else:
        # otherwise check all the suffixes
        return any(match_here(regex, t) for t in suffixes(text))


def test():
    assert match("23", "123")
    assert match("^1", "123")
    assert match("^123$", "123")
    assert not match("123$", "1234")
    assert not match("1235", "123")
    assert match("*34", "1234")
    assert not match("13*", "1234")
    assert match("12*3", "1234")
