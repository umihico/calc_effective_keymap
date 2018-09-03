import csv_wrapper
import itertools
"""
https://kouy.exblog.jp/9731073/
http://web1.nazca.co.jp/kouy/N-gram_2gram.txt
"""


def load_one_gram():
    one_gram_list = csv_wrapper.load_csv('1gram.csv')
    one_gram_dict = dict(one_gram_list)
    one_gram_dict = {k: int(v) for k, v in one_gram_dict.items()}
    return one_gram_dict


def gen_2gram_dict_separated():
    data = csv_wrapper.load_csv('2gram_original_no_edit.csv')
    separated_2gram_dict = {word: int(count)
                            for count, word, gram_type in data}
    return separated_2gram_dict


def load_ngram_dict_separated():
    one_gram_dict = load_one_gram()
    two_gram_dict = gen_2gram_dict_separated()
    return one_gram_dict, two_gram_dict


def load_ngram_dict():
    one_gram_dict = load_one_gram()
    two_gram_list = csv_wrapper.load_csv('2gram_no_order.csv')
    two_gram_dict = dict(two_gram_list)
    two_gram_dict = {k: int(v) for k, v in two_gram_dict.items()}
    return one_gram_dict, two_gram_dict


def _convert_2gram_both_direction():
    data = csv_wrapper.load_csv('2gram_original_no_edit.csv')
    two_gram_dict = dict()
    both_direction_two_gram_dict = dict()
    for count, word, gram_type in data:
        count = int(count)
        two_gram_dict[word] = count
        if word in both_direction_two_gram_dict:
            both_direction_two_gram_dict[word] += count
        else:
            both_direction_two_gram_dict[word] = count
        reversed_word = word[1] + word[0]
        if reversed_word in both_direction_two_gram_dict:
            both_direction_two_gram_dict[reversed_word] += count
        else:
            both_direction_two_gram_dict[reversed_word] = count
    """check sum"""
    print(two_gram_dict['あい'])
    print(two_gram_dict['いあ'])
    print(both_direction_two_gram_dict['あい'])
    print(both_direction_two_gram_dict['いあ'])

    """put 0 missing unfamous keys"""
    one_gram_dict = load_one_gram()
    keys = one_gram_dict.keys()
    for k0, k1 in itertools.product(keys, keys):
        key = ''.join([k0, k1])
        if key not in both_direction_two_gram_dict:
            both_direction_two_gram_dict[key] = 0

    """merge 、 and 。
    del　、 add 。"""
    print(both_direction_two_gram_dict['す。'])
    print(both_direction_two_gram_dict['す、'])
    for word, count in both_direction_two_gram_dict.items():
        if '、' in word:
            replaced_word = word.replace('、', '。')
            both_direction_two_gram_dict[replaced_word] += count
    del_keys = [word for word,
                count in both_direction_two_gram_dict.items() if '、' in word]
    for del_key in del_keys:
        del both_direction_two_gram_dict[del_key]
    print(both_direction_two_gram_dict['す。'])
    print('す、' in both_direction_two_gram_dict)

    csv_wrapper.save_csv('2gram_no_order.csv',
                         both_direction_two_gram_dict.items())


def _save_1gram():
    data = csv_wrapper.load_csv('1gram_original_no_edit.csv')
    dict_ = dict()
    for count, word, gram_type in data:
        count = int(count)
        dict_[word] = count
    del dict_['〓']
    dict_['。'] += dict_['、']
    del dict_['、']
    print(dict_)
    csv_wrapper.save_csv('1gram.csv',
                         dict_.items())


if __name__ == '__main__':
    _convert_2gram_both_direction()
    _save_1gram()
    d1, d2 = load_ngram_dict()
