
from umihico_commons.functools import load_from_txt


def load_first_dicts():
    filenames = ["dict1gram.txt", "dict2gram.txt"]
    dict1gram, dict2gram = [load_from_txt(filename) for filename in filenames]
    return dict1gram, dict2gram


if __name__ == '__main__':
    from pprint import pprint
    pprint(load_first_dicts())
