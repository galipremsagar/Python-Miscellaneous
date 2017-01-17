def hash(s):
    h = 7
    letters = "acdegilmnoprstuw"
    for i in xrange(len(s)):
        h = (h * 37 + letters.index(s[i]))
    return h

def rev_hash(hash):
    letters = "acdegilmnoprstuw"
    actual_string = ""
    while hash > 7:
        i = hash%37
        actual_string = letters[i] + actual_string
        hash = (hash - i)/37
    print actual_string
    return actual_string

def tests():
    assert 680131659347 == hash("leepadg")
    assert "leepadg" == rev_hash(680131659347)