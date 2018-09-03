# -*- coding: utf-8 -*-
from mother import *
from itertools import product, permutations, combinations
from group_combinations import group_combinations


def _read_csv():
    list_ = []
    for filename in ['1gram', '2gram']:
        n_gram = csv2list(filename)
        n_gram.pop(0)  # removing header
        n_gram = [[int(x[0]), x[1]] for x in n_gram]
        # print(n_gram[:100])
        list_.append(n_gram)
    one_gram, two_gram = list_
    return one_gram, two_gram


class Letters():
    def __init__(self):
        one_gram, two_gram = _read_csv()
        self._set_1gram(one_gram)
        self._set_2gram(two_gram)

    def _set_1gram(self, one_gram):
        self.one_gram_dict = {}
        for count, letter in one_gram:
            self.one_gram_dict[letter] = count
        self.onegram_ranking = sorted(
            [(key, value) for key, value in self.one_gram_dict.items()], key=itemgetter(1), reverse=True)

    def _set_2gram(self, two_gram):
        dict_ = {}
        for count, two_letter in two_gram:
            f, s = two_letter
            dict_[f + s] = count
        self.two_gram_dict = {}
        for two_letter, value in dict_.items():
            f, s = two_letter
            fs_cost = dict_[f + s] if f + s in dict_ else 0
            sf_cost = dict_[s + f] if s + f in dict_ else 0
            self.two_gram_dict[f + s] = fs_cost + sf_cost
        for key0, key1 in product(self.one_gram_dict.keys(), self.one_gram_dict.keys()):
            if key0 + key1 not in self.two_gram_dict:
                self.two_gram_dict[key0 + key1] = 0

    def get_1gram_cost(self, *keys):
        if keys not in self.one_gram_dict:
            self.one_gram_dict[keys] = sum(
                self.one_gram_dict[key] for key in keys)
        return self.one_gram_dict[keys]

    def get_2gram_cost(self, *keys):
        if keys not in self.two_gram_dict:
            self.two_gram_dict[keys] = sum(
                self.two_gram_dict[key0 + key1] for key0, key1 in combinations(keys, 2))
        return self.two_gram_dict[keys]

    def gen_maximized_cross_hand_cost_patterns(self, left_len, *keys):
        patterns = []
        for left_keys in combinations(keys, left_len):
            left_keys = set(left_keys)
            right_keys = set(keys) - left_keys
            hand_cross2gram_cost = sum(self.get_2gram_cost(r_key, l_key)
                                       for r_key, l_key in product(left_keys, right_keys))
            l_1gram_cost = self.get_1gram_cost(*left_keys)
            r_1gram_cost = self.get_1gram_cost(*right_keys)
            patterns.append(
                (left_keys, l_1gram_cost, right_keys, r_1gram_cost, hand_cross2gram_cost))
        patterns.sort(key=itemgetter(-1), reverse=True)
        return patterns

    def minimize_same_finger_cost(self, keys_sets0, keys_sets1):
        if keys_sets0 is None:
            keys_sets0 = [{'し'}, {'と'}, {'の'}, {
                'か'}, {'た'}, {'う'}, {'ん'}, {'、'}]
        if keys_sets1 is None:
            keys_sets1 = [{'て'}, {'く'}, {'な'}, {
                'に'}, {'き'}, {'は'}, {'こ'}, {'る'}]
        # create cost dict
        cost_dict = {}
        for key0, key1 in product(keys_sets0, keys_sets1):
            keys = key0 | key1
            cost = self.get_2gram_cost(*keys)
            for key in permutations(keys):
                cost_dict[key] = cost
        costs = []
        for keys_sets1_pattern in permutations(keys_sets1):
            cost = sum(cost_dict[tuple(key0 | key1)]
                       for key0, key1 in zip(keys_sets0, keys_sets1_pattern))
            keys_set = [key0 | key1 for key0, key1 in zip(
                keys_sets0, keys_sets1_pattern)]
            costs.append((cost, keys_set))
        costs.sort(key=itemgetter(0))
        return costs

    def minimize_same_finger_cost_product(self, keys_sets0_patterns, keys_sets1):
        costs = []
        args = [(self, x, keys_sets1)
                for x in chunks(keys_sets0_patterns, 100)]
        list_of_list = Poolbar(multiprocessing_minimize_cost_func, args)
        for list_ in list_of_list:
            costs.extend(list_)
            costs.sort(key=itemgetter(0))
            costs = costs[:100]
        # for i, keys_sets0_pattern in enumerate(keys_sets0_patterns):
        #     new_costs = self.minimize_same_finger_cost(
        #         keys_sets0_pattern, keys_sets1)
        #     print(i)
        #     costs.extend(new_costs)
            # costs.sort(key=itemgetter(0))
            # costs = costs[:100]
        return costs


def multiprocessing_minimize_cost_func(args):
    letters, keys_sets0_chunks, keys_sets1 = args
    costs = []
    for keys_sets0 in keys_sets0_chunks:
        new_costs = letters.minimize_same_finger_cost(
            keys_sets0, keys_sets1)
        costs.extend(new_costs)
        costs.sort(key=itemgetter(0))
        costs = costs[:100]
    return costs


# def create_keyset1and2():
#     keys_sets = [{'て'}, {'く'}, {'な'}, {'に'}, {'き'}, {'は'}, {
#         'こ'}, {'る'}, {'が'}, {'で'}, {'っ'}, {'ょ'}, {'す'}, {'ま'}]


if __name__ == '__main__':

    letters = Letters()
    home_pos_fingers = ['し', 'と', 'の', 'か', 'た', 'う', 'ん', 'て']
    home_pos_patterns = letters.gen_maximized_cross_hand_cost_patterns(
        4, *home_pos_fingers)
    home_pos_patterns = home_pos_patterns[:30]
    # for pattern in home_pos_patterns:
    #     print(pattern)
    """
    中段ホームポジション
    {'か', 'の', 'と', 'し'}, 163957, {'ん', 'う', 'た', 'て'}, 179522, 59718)
    """
    [print(*x) for x in letters.onegram_ranking]

    # print([set(x) for x in home_pos_fingers])
    # keys_sets0 = [{'し'}, {'と'}, {'の'}, {'か'}, {'た'}, {'う'}, {'ん'}, {'、'}]

    next_keys = 'くなにきはこるがでっょすまじ::'
    list_ = group_combinations(letters=next_keys, chunk_size=3)
    print(len(list_))

# # keys_sets1 = [{'て'}, {'く'}, {'な'}, {'に'}, {'き'}, {'は'}, {'こ'}, set()]
# keys_sets1 = [{'て'}, {'く'}, {'な'}, {'に'}, {'き'}, {'は'}, set(), set()]
# costs = letters.minimize_same_finger_cost(keys_sets0, keys_sets1)
# print_costs = costs[:30]
# [print(x) for x in print_costs]
#
# print(len(costs))
# costs = costs[:int(len(costs) * 0.1)]
# # costs = costs[:10]  # test
# keys_sets0_patterns = [x[1] for x in costs]
# # keys_sets2 = [{'が'}, {'で'}, {'っ'}, {'ょ'}, {'す'}, {'ま'}, set(), set()]
# # keys_sets2 = [{'が'}, {'で'}, {'っ'}, {'ょ'}, {'す'}, {'ま'}, {'る'}, set()]
# keys_sets2 = [{'が'}, {'で'}, {'っ'}, {'ょ'}, {'す'}, {'ま'}, {'こ'}, {'る'}]
# if False:
#     costs = letters.minimize_same_finger_cost_product(
#         keys_sets0_patterns, keys_sets2)
#     print_costs = costs[:100]
#     [print(x) for x in print_costs]
# else:
#     data = csv2list('csv_data')
#     data = [[int(x[0]), *x[1:]] for x in data]
#     rows = [[x[0], *[set(y) for y in x[1:]]] for x in data]
#     rows.sort(key=itemgetter(0))
#     rows = [(col[0], *[(x, letters.get_1gram_cost(*x), letters.get_2gram_cost(*x))
#                        for x in col[1:]]) for col in rows]
#     for col in rows:
#         total2gram_cost, *keys = col
#     [print(x) for x in rows]
