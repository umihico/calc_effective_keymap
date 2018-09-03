import itertools
from tabulate import tabulate
import numpy


def __readable_example(keys, fingers):
    """
    Aa  Ba  Ca  Ab  Bb  Cb  Ac  Bc  Cc  Ad  Bd  Cd  Ae  Be  Ce
    1   0   0   0   1   0   0   0   1   1   0   0   0   1   0
    1   0   0   0   1   0   0   0   1   0   1   0   1   0   0
    1   0   0   0   1   0   1   0   0   0   0   1   0   1   0
    1   0   0   0   1   0   0   1   0   0   0   1   1   0   0
    1   0   0   0   1   0   1   0   0   0   1   0   0   0   1
    1   0   0   0   1   0   0   1   0   1   0   0   0   0   1
    1   0   0   0   0   1   0   1   0   1   0   0   0   1   0
    1   0   0   0   0   1   0   1   0   0   1   0   1   0   0
    1   0   0   1   0   0   0   1   0   0   0   1   0   1   0
    1   0   0   0   1   0   0   1   0   0   0   1   1   0   0
    1   0   0   1   0   0   0   1   0   0   1   0   0   0   1
    1   0   0   0   1   0   0   1   0   1   0   0   0   0   1
    1   0   0   0   0   1   1   0   0   0   1   0   0   1   0
    """
    multi_finger = (fingers * 100)[:len(keys)]  # 'ABCAB'
    print_list = []
    print_list.append([(f + k) for k in keys for f in fingers])
    for keys_sorted in itertools.permutations(keys):
        exist_list = [(f + k) for f, k in zip(multi_finger, keys_sorted)]
        print(exist_list)
        # ['Aa', 'Bb', 'Cc', 'Ad', 'Be']
        # print([(f + k, 1 if (f + k) in exist_list
        #         else 0) for k in keys for f in fingers])
        # [('Aa', 1), ('Ba', 0), ('Ca', 0), ('Ab', 0), ('Bb', 1), ('Cb', 0), ('Ac', 0), ('Bc', 0), ('Cc', 1), ('Ad', 1), ('Bd', 0), ('Cd', 0), ('Ae', 0), ('Be', 1), ('Ce', 0)]
        digit_list = [1 if (f + k) in exist_list
                      else 0 for k in keys for f in fingers]
        # print(digit_list)
        # [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0]
        print_list.append(digit_list)

    print(tabulate(print_list[: 100]))


def gen_pattern(keys='abcde', fingers='ABC'):
    assert len(keys) >= len(fingers)
    adjusted_fingers = (fingers * 100)[: len(keys)]  # 'ABCAB'
    l = [tuple([1 if (f + k) in [(f + k) for f, k in zip(adjusted_fingers, k_sorted)]
                else 0 for k in keys for f in fingers]) for k_sorted in itertools.permutations(keys)]
    l = list(set(l))
    return l


def gen_pattern_for_dot_with_fname_permutation(keys='abcde', fingers='ABC'):
    fieldnames = gen_fieldnames(keys, fingers)
    patterns = gen_pattern(keys, fingers)
    # print(fieldnames)
    # print(patterns[0])
    fnames_list = [[fn for fn, int_ in zip(
        fieldnames, ints) if int_ == 1] for ints in patterns]
    p_ = list(zip(*patterns))
    np_p = numpy.array(p_)
    return fnames_list, np_p


def gen_fieldnames(keys='abcde', fingers='ABC'):
    return [(f,  k) for k in keys for f in fingers]


def tests():
    # fingers = 'ABC'
    # keys = 'abcde'
    fingers = ['A', 'B', 'C', 'D']
    keys = 'abcdefg'
    __readable_example(keys, fingers)
    fieldnames = gen_fieldnames(keys, fingers)
    l = [fieldnames, ]
    p = gen_pattern(keys, fingers)
    l.extend(p)
    print(tabulate(l[: 30]))
    fieldnames = gen_fieldnames(keys, fingers)
    l = [fieldnames, ]
    p = gen_pattern(keys, fingers)
    l.extend(p)
    print(tabulate(l[: 30]))
    fnames_list, patterns = gen_pattern_for_dot_with_fname_permutation(
        keys, fingers)
    for fnames in fnames_list:
        print(fnames)


if __name__ == '__main__':
    tests()
