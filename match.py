Char  = str
Regex = str
Text  = str

def slices(text: Text):
    """
    take a text, and return steps through the text like:
    text, ext, xt, t
    """
    yield text
    for i in range(len(text) + 1):
        yield text[i+1:]



def match(regexp: Regex, text: Text) -> bool:
    """
    Match reports whether regexp matches anywhere in text
    """
    if regexp != "" and regexp[0] == "^":
        return matchhere(regexp[1:], text)

    for t in slices(text):
        if matchhere(regexp, t):
            return True
        if t == "":
            return False


def matchhere(regexp: Regex, text: Text) -> bool:
    """
    matchhere reports whether regexp matches at beginning of text.
    """
    if regexp == "":
        return True
    elif regexp == "$":
        return text == ""
    elif len(regexp) >= 2 and regexp[1] == "*":
        return matchstar(regexp[0], regexp[2:], text)
    elif text != "" and (regexp[0] == "." or regexp[0] == text[0]):
        return matchhere(regexp[1:], text[1:])
    else:
        return False


def matchstar(c: Char, regexp: Regex, text: Text) -> bool:
    """
    matchstar reports whether c*regexp matches at beginning of text
    """
    for t in slices(text):
        if matchhere(regexp, t):
            return True
        if t == "" or (t[0] != c and c != "."):
            return False


def test():
    assert match("23", "123")
    assert match("^1", "123")
    assert match("^123$", "123")
    assert not match("123$", "1234")
    assert not match("1235", "123")
    assert match("12*3", "1234")
