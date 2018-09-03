# -*- coding: utf-8 -*-

"""
after first home 8 keys, decide rest 14 keys here.
"""
import itertools
import math
from tqdm import tqdm
from csv_manager import load_ngram_dict
from gram_data import gram_data, gram_ranking, gram_data_separated
from operator import itemgetter
from itertools import combinations
from itertools import product
from itertools import permutations
import csv_wrapper
from time import sleep, time
from numba import jit
from tabulate import tabulate
import numpy as np
import gen_pattern_for_dot
import gen_cost_list_for_dot
from itertools import groupby


def gen_cost_dict(home_keys, second_keys):
    cost_dict = {}
    for hk, sk0, sk1 in product(home_keys, second_keys, second_keys):
        pattern = tuple([hk, sk0, sk1])
        cost_dict[pattern] = gram_data.get_2gram_cost(pattern)
    for hk, sk in product(home_keys, second_keys):
        pattern = tuple([hk, sk])
        cost_dict[pattern] = gram_data.get_2gram_cost(pattern)
    for hk, sk in product(home_keys, second_keys):
        pattern = tuple([hk, sk, 'a'])
        cost_dict[pattern] = 0
    for sk0, sk1 in product(second_keys, second_keys):
        pattern = tuple([sk0, sk1])
        cost_dict[pattern] = gram_data.get_2gram_cost(pattern)
    return cost_dict


def gen_good_data_rows():
    home_keys = 'うたんとかの。し'
    not_home_keys = 'てくなにきはこるがでっょすま:;'
    cost_dict = gen_cost_dict(home_keys, not_home_keys)
    csv_ = csv_wrapper.load_csv('final_output.csv')
    petterns_ = [[1 if i == e else 0 for i in ints for e in range(8)]
                 for ints in permutations(range(8))]
    # petterns_ = petterns_[:100]
    petterns = list(zip(*petterns_))
    np_petterns = np.array(petterns)
    good_data_rows = []
    for row in tqdm(csv_):
        tuple_str, score = row
        second_keys = eval(tuple_str)
        rest_keys = list(set(not_home_keys) - set(second_keys))
        cost_list = [cost_dict[(hk, ok, rk)] for hk, ok in zip(
            home_keys, second_keys) for rk in rest_keys]
        costs = np.dot(cost_list, np_petterns)
        costs_with_permutation = [(cost, second_keys, rest_key_pattern)
                                  for cost, rest_key_pattern in zip(costs, permutations(rest_keys))]
        good_data_rows.extend(costs_with_permutation)
        good_data_rows.sort(key=itemgetter(0), reverse=False)
        good_data_rows = good_data_rows[:10000]
        good_data_rows = [(cost, ''.join(second_keys), ''.join(rest_key_pattern))
                          for cost, second_keys, rest_key_pattern in good_data_rows]
    csv_wrapper.save_csv('good_data_rows.csv', good_data_rows)


def show_good_data_rows():
    home_keys = 'うたんとかの。し'
    good_data_rows = csv_wrapper.load_csv('good_data_rows.csv')
    prev_cost1each = 0
    prev_cost2each = 0
    for row in good_data_rows[:100]:
        print_list = []
        cost2fin, layer1keys, layer2keys = row
        print_list.append(home_keys)
        print_list.append(layer1keys)
        print_list.append(layer2keys)
        cost1each = [gram_data.get_1gram_cost(keys)
                     for keys in zip(home_keys, layer1keys, layer2keys)]
        print_list.append(cost1each)
        cost2each = [gram_data.get_2gram_cost(keys)
                     for keys in zip(home_keys, layer1keys, layer2keys)]
        print_list.append(cost2each)
        cost1all = sum(cost1each)
        if prev_cost1each == cost1each and prev_cost2each == cost2each:
            print('same')
            continue
        prev_cost1each = cost1each
        prev_cost2each = cost2each
        print(tabulate(print_list))
        print(cost2fin, cost1all)
        break


def calc_hand_of_first_layer():
    home_keys = 'うたんとかの。し'
    good_data_rows = csv_wrapper.load_csv('good_data_rows.csv')
    """
    -----  -----  ------  -----  -----  -----  -----  -----
    う      た      ん       と      か      の      。      し
    く      な      る       て      き      に      :      は
    ;      で      っ       ま      こ      が      ょ      す
    86814  83163  104495  85031  89982  88830  73629  93979
    339    1361   549     1191   1470   2372   82     2257
    -----  -----  ------  -----  -----  -----  -----  -----
    9621 705923
    """
    for row in good_data_rows[:100]:
        print_list = []
        cost2fin, layer1keys, layer2keys = row
        break
    fingers = [keys for keys in zip(home_keys, layer1keys, layer2keys)]
    fingers.extend(['い', ])
    data_rows = []
    for r_fins in combinations(fingers, 5):
        l_fins = set(fingers) - set(r_fins)
        # print(r_fins)
        r_letters = flatten(r_fins)
        l_letters = flatten(l_fins)
        if 'い' not in r_letters:
            continue
        r_hand_1cost = gram_data.get_1gram_cost(r_letters)
        l_hand_1cost = gram_data.get_1gram_cost(l_letters)
        r_hand_2cost = gram_data.get_2gram_cost(r_letters)
        l_hand_2cost = gram_data.get_2gram_cost(l_letters)
        cross_hand_cost = r_hand_2cost + l_hand_2cost
        data_rows.append((cross_hand_cost, l_hand_2cost, r_hand_2cost,  l_hand_1cost,
                          r_hand_1cost, l_fins, r_fins))
    data_rows.sort(key=itemgetter(0), reverse=False)
    for cross_hand_cost, l_hand_2cost, r_hand_2cost,  l_hand_1cost, r_hand_1cost, l_fins, r_fins in data_rows:
        fin_print = list(l_fins)
        fin_print.extend(r_fins)
        fin_print = [''.join(x) for x in fin_print]
        l_fins_1costs = [gram_data.get_1gram_cost(l_fin) for l_fin in l_fins]
        r_fins_1costs = [gram_data.get_1gram_cost(r_fin) for r_fin in r_fins]
        cost_print = list(l_fins_1costs)
        cost_print.extend(r_fins_1costs)
        all_print = list(zip(fin_print, cost_print))
        all_print = list(zip(*all_print))
        print(tabulate(all_print))
        print(cross_hand_cost, l_hand_2cost,
              r_hand_2cost,  l_hand_1cost, r_hand_1cost)


def add_layer(l_fings=['たなで', '。ょ', 'のにが', 'とてま'], r_fings=['うく', 'んるっ', 'かきこ', 'しはす', 'い'], adding_keys='じりもつおらをさあれだ'):
    """
    -----  -----  -----  -----  -----  ------  -----  -----  -----
    たなで    。:ょ    のにが    とてま    うく;    んるっ     かきこ    しはす    い
    83163  73629  88830  85031  86814  104495  89982  93979  74569
    -----  -----  -----  -----  -----  ------  -----  -----  -----
    183135 59059 124076 330653 449839
    """

    names = ['l_fings',     'r_fings']

    # adding_keys = 'じりもつおらをさ'
    # adding_keys = 'じりもつおらをさ'
    # adding_keys = 'じりもつおらをさあれだちせけーよどゅそえ'
    # adding_keys = 'じりもつおらをさあれだちせ'

    fingers = [*l_fings, *r_fings]
    fingers_list = [l_fings, r_fings]
    new_fingers_list = []
    letters = flatten(fingers)
    cost_dict = gen_cost_dict(letters, adding_keys)
    for i, (finger, name) in enumerate(zip([l_fings, r_fings], names)):
        print(f'{name} = {finger}')
        fnames_list, petterns = gen_pattern_for_dot.gen_pattern_for_dot_with_fname_permutation(
            keys=adding_keys, fingers=finger)

        cost_list = gen_cost_list_for_dot.gen_cost_list_only_additional_cost(
            cost_dict, keys=adding_keys, fingers=finger)
        costs = np.dot(cost_list, petterns)
        costs_with_fnames = list(zip(costs, fnames_list))
        costs_with_fnames.sort(key=itemgetter(0), reverse=False)
        costs_with_fnames = costs_with_fnames[:100]
        costs_with_fnames = [(cost, [''.join((k, *[x[1] for x in g])) for k, g in groupby(sorted(fingers), key=itemgetter(0))])
                             for cost, fingers in costs_with_fnames]

        filename = f'costs_with_fnames{i}.csv'
        # csv_wrapper.save_csv(filename, costs_with_fnames[:100])
        # print(cost_list)
        new_finger = list(costs_with_fnames[0][1])
        print(type(new_finger))
        print(f'new_{name} = {new_finger}')
        new_fingers_list.append(new_finger)
        # print(len(costs_with_fnames))
        # for x in costs_with_fnames:
        #     print(*x)
        # print(len(costs_with_fnames))
    return new_fingers_list


def iter_add_layer():
    """first values"""
    l_fings = ['たなで', '。ょ', 'のにが', 'とてま']
    r_fings = ['うく', 'んるっ', 'かきこ', 'しはす', 'い']
    rank_list = gram_ranking.print_1gram_ranking(print_=False)
    letters = [x[0] for x in rank_list]
    while True:
        used_letters = ''.join(
            [*flatten(l_fings), *flatten(r_fings)])
        unused_letters = [x for x in letters if x not in used_letters]
        if len(unused_letters) == 0:
            break
        adding_keys = ''.join(unused_letters[:10])
        print(f'adding_keys = {adding_keys}')
        new_fingers_list = add_layer(l_fings, r_fings, adding_keys)
        l_fings, r_fings = new_fingers_list

    # new_fingers_list = add_layer(l_fings, r_fings, adding_keys)


def get_additional_10keys():
    # original_l_fings = ['たなで', '。ょ', 'のにが', 'とてま']
    # original_r_fings = ['うく', 'んるっ', 'かきこ', 'しはす', 'い']
    original_l_fings = ['たなでおさじ', '。ょ', 'のにが', 'とてま']
    original_r_fings = ['うくあ', 'んるっ', 'かきこもだよ', 'しはす', 'い']
    """おさじ,  もだ, あ"""
    # l_fings = [
    #     'たなでおさじせそよひふほぐずむぞぷぽづぬぴ',
    #     '。ょつもれえゅーみゃろござぶぃへゆぅぇヴ',
    #     'のにがりをけだばやげびぱべぁぉ',
    #     'とてまあらちどめわぎねぜぼぢぺ', ]
    # r_fings = [
    #     'うくあれえーひみぎねぜべぅぬ',
    #     'んるっつらちゅふろずむぞゆぢヴ',
    #     'かきこじもだよばやぐごぱぽぇぺ',
    #     'しはすおさけせほめざぶぷへぁぉ',
    #     'いりをそどゃわげびぃぼづぴ', ]
    l_fings = [
        'たなでおさじせそひふほぐずむぞぷぽづぬぴ',
        '。ょつれえゅーみゃろござぶぃへゆぅぇヴ',
        'のにがりをけばやげびぱべぁぉ',
        'とてまらちどめわぎねぜぼぢぺ', ]
    r_fings = [
        'うくあれえーひみぎねぜべぅぬ',
        'んるっつらちゅふろずむぞゆぢヴ',
        'かきこもだよばやぐごぱぽぇぺ',
        'しはすけせほめざぶぷへぁぉ',
        'いりをそどゃわげびぃぼづぴ', ]
    original_l_fings_dict = {k: v for k, v in zip(original_l_fings, l_fings)}
    original_r_fings_dict = {k: v for k, v in zip(original_r_fings, r_fings)}
    new_l_fings = {k: [] for k in original_l_fings_dict.keys()}
    new_r_fings = {k: [] for k in original_r_fings_dict.keys()}
    rakn_list = gram_ranking.print_1gram_ranking()
    for l, count in rakn_list:
        if l in flatten(original_l_fings) or l in flatten(original_r_fings):
            continue
        for lk, rk in product(new_l_fings, new_r_fings):
            if l in original_l_fings_dict[lk] and l in original_r_fings_dict[rk]:
                if len(new_l_fings[lk]) < 10 and len(new_r_fings[rk]) < 8:
                    new_l_fings[lk].append(l)
                    new_r_fings[rk].append(l)
                    break
    print(new_l_fings)
    print(new_r_fings)
    return new_l_fings, new_r_fings


def decide_front_or_back():
    l_fings, r_fings = get_additional_10keys()
    two_tap_letters_cost_dict = {}
    for fings, left_boolean in zip([l_fings, r_fings], [True, False]):
        for one_tap_letters, two_tap_letters in fings.items():
            for two_tap_letter in two_tap_letters:
                if two_tap_letter not in two_tap_letters_cost_dict:
                    two_tap_letters_cost_dict[two_tap_letter] = 0
                rest_keys_in_the_finger = [x for x in itertools.chain(
                    one_tap_letters, two_tap_letters) if x != two_tap_letter]
                if left_boolean:
                    l_being_front_cost = gram_data_separated.get_2gram_cost(
                        front_keys=[two_tap_letter, ], back_keys=rest_keys_in_the_finger)
                    l_being_back_cost = gram_data_separated.get_2gram_cost(
                        front_keys=rest_keys_in_the_finger, back_keys=[two_tap_letter, ])
                    two_tap_letters_cost_dict[two_tap_letter] += l_being_back_cost
                    two_tap_letters_cost_dict[two_tap_letter] -= l_being_front_cost
                else:
                    r_being_front_cost = gram_data_separated.get_2gram_cost(
                        front_keys=[two_tap_letter, ], back_keys=rest_keys_in_the_finger)
                    r_being_back_cost = gram_data_separated.get_2gram_cost(
                        front_keys=rest_keys_in_the_finger, back_keys=[two_tap_letter, ])
                    two_tap_letters_cost_dict[two_tap_letter] += r_being_front_cost
                    two_tap_letters_cost_dict[two_tap_letter] -= r_being_back_cost
    two_tap_letters_cost_list = list(two_tap_letters_cost_dict.items())
    two_tap_letters_cost_list.sort(key=lambda x: abs(x[1]),  reverse=True)
    for letter, shold_be_l_front_r_back_point in two_tap_letters_cost_list:
        print(letter, shold_be_l_front_r_back_point)
    print()
    print(r_fings)
    print(l_fings)
    two_tap_letters_l_front_bool_dict = {
        k: None for k in two_tap_letters_cost_dict.keys()}
    for letter, shold_be_l_front_r_back_point in two_tap_letters_cost_list:
        r_finger = [(k, v) for k, v in r_fings.items() if letter in v][0]
        # '。ょ': ['も', 'つ', 'れ', 'ー', 'ゅ', 'え', 'み', 'ろ', 'ゃ', 'ぶ']
        l_finger = [(k, v) for k, v in l_fings.items() if letter in v][0]
        front_is_full_in_r_finger = bool(len(r_finger[1]) == sum(
            1 for l in r_finger[1] if two_tap_letters_l_front_bool_dict[l] == True))
        back_is_full_in_r_finger = bool(len(r_finger[1]) == sum(
            1 for l in r_finger[1] if two_tap_letters_l_front_bool_dict[l] == False))
        front_is_full_in_l_finger = bool(len(l_finger[1]) == sum(
            1 for l in l_finger[1] if two_tap_letters_l_front_bool_dict[l] == True))
        back_is_full_in_l_finger = bool(len(l_finger[1]) == sum(
            1 for l in l_finger[1] if two_tap_letters_l_front_bool_dict[l] == False))
        if two_tap_letters_l_front_bool_dict[letter] is not None:
            raise Exception('not None')
        if shold_be_l_front_r_back_point > 0:
            if not front_is_full_in_l_finger and not back_is_full_in_r_finger:
                two_tap_letters_l_front_bool_dict[letter] = True
            else:
                two_tap_letters_l_front_bool_dict[letter] = False
        else:
            if not front_is_full_in_r_finger and not back_is_full_in_l_finger:
                two_tap_letters_l_front_bool_dict[letter] = False
            else:
                two_tap_letters_l_front_bool_dict[letter] = True

    print(two_tap_letters_l_front_bool_dict)


def decide_fin_pos():
    r_fings = {'うくあ': ['れ', 'ー', 'え', 'み', 'ひ', 'ね', 'ぎ', 'ぜ'], 'んるっ': ['つ', 'ら', 'ち', 'ゅ', 'ろ', 'ふ', 'む', 'ず'], 'かきこもだよ': [
        'ば', 'や', 'ご', 'ぐ', 'ぱ', 'ぽ', 'ぺ'], 'しはす': ['せ', 'け', 'め', 'ほ', 'ぶ', 'ぷ', 'ぁ', 'ぉ'], 'い': ['り', 'を', 'ど', 'そ', 'わ', 'ゃ', 'げ', 'び']}
    l_fings = {'たなでおさじ': ['せ', 'そ', 'ひ', 'ほ', 'ふ', 'む', 'ず', 'ぐ', 'ぷ', 'ぽ'], '。ょ': ['つ', 'れ', 'ー', 'ゅ', 'え', 'み', 'ろ', 'ゃ', 'ぶ', 'ご'], 'のにが': [
        'り', 'を', 'け', 'ば', 'や', 'げ', 'び', 'ぱ', 'ぁ', 'ぉ'], 'とてま': ['ら', 'ち', 'ど', 'わ', 'め', 'ね', 'ぎ', 'ぜ', 'ぺ']}

    r_fings_flat = [''.join([*k, *v]) for k, v in r_fings.items()]
    l_fings_flat = [''.join([*k, *v]) for k, v in l_fings.items()]
    for letters_in_fin in itertools.chain(r_fings_flat, [''], l_fings_flat):
        try:
            cost = gram_data.get_1gram_cost(letters_in_fin)
        except (Exception, ) as e:
            cost = 0
        print(cost, letters_in_fin)
        print([gram_data.get_1gram_cost(l) for l in letters_in_fin])
    # print(r_fings_flat)
    for flayer_fings in [r_fings, l_fings]:
        # up_down_keys = flatten([ks[1:] for ks in flayer_fings.keys()])
        up_down_keys = flatten([ks for ks in flayer_fings.keys()])
        print(up_down_keys)
        list_ = sorted([(sorted(keys), gram_data.get_2gram_cost(keys)) for keys in product(
            up_down_keys, up_down_keys)], key=lambda x: x[1])
        for keys, cost in list_:
            print(keys, cost)


def check_dot_calculation():
    tuple_ = (14664, ['とてまじ', 'のにがり', '。ょも', 'たなでつ', 'たなでお'])
    cost0, fingers = tuple_
    cost = sum(gram_data.get_2gram_cost(keys) for keys in fingers)
    print(cost, cost0)


def flatten(list_of_list):
    return [item for sublist in list_of_list for item in sublist]


if __name__ == '__main__':
    # test2()
    # show_good_data_rows()
    # calc_hand_of_first_layer()
    # add_layer()
    # iter_add_layer()
    # get_additional_10keys()
    decide_front_or_back()
    decide_fin_pos()
    # check_dot_calculation()
