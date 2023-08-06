import re

ALL_EMPTY_SPACES = re.compile(r'\s+', flags=re.UNICODE)


def remove_all_empty_spaces(sentence):
    return re.sub(ALL_EMPTY_SPACES, "", sentence)