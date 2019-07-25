from nltk.tokenize import sent_tokenize, word_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    line_a_set = set(a.split('\n'))
    line_b_set = set(b.split('\n'))

    line_repeat_set = line_a_set & line_b_set
    line_repeat_list = list(line_repeat_set)

    return line_repeat_list

def sentences(a, b):
    """Return sentences in both a and b"""

    sent_a = set(sent_tokenize(a))
    sent_b = set(sent_tokenize(b))

    return sent_a & sent_b

def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    sub_a = []
    sub_b = []

    for i in range(len(a) - n + 1):
        sub_a.append(a[i:i + n])
    for j in range(len(b) - n + 1):
        sub_b.append(b[j:j + n])

    return set(sub_a) & set(sub_b)