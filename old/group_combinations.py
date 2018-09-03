# -*- coding: utf-8 -*-0
import itertools
from copy import deepcopy


def _group_combinations_main(letters, rest, recoder, chunk_size):
    new_rests = []
    if len(list(itertools.combinations(rest, chunk_size))):
        for pick in itertools.combinations(rest, chunk_size):
            pick = set(pick)
            new_rest = rest - pick
            if any([bool(pick <= new_rest) for new_rest in new_rests]):
                # already exist
                continue
            else:
                new_rests.append(new_rest)
                new_letters = deepcopy(letters)
                new_letters.append(pick)
                _group_combinations_main(
                    new_letters, new_rest, recoder, chunk_size)
    else:
        recoder.append(letters)


def group_combinations(letters, chunk_size):
    letters = set(letters)
    recoder = []
    _group_combinations_main([], letters, recoder, chunk_size)
    return recoder


if __name__ == '__main__':
    next_letters = ['て', 'く', 'な', 'に', 'き',
                    'は', 'こ', 'る', 'が', 'で', 'っ', 'ょ', ]
    recoder = group_combinations(next_letters, chunk_size=2)
    [print(x) for x in recoder]
    print(len(recoder))
