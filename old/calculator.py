# -*- coding: utf-8 -*-
from mother import *
from itertools import combinations, permutations, product
import chunk_combi
from multiprocessing import Pool
import data


class Letter():
    def __init__(self, letter_str, count):
        self.letter = letter_str
        self.one_gram = count
        self.two_gram_dict = {}

    def __setitem__(self, key, value):
        self.two_gram_dict[key] = value

    def __getitem__(self, key):
        key = str(key)
        try:
            return self.two_gram_dict[key]
        except KeyError as e:
            if len(key) > 1:
                self.two_gram_dict[key] = 0
                for letter in key:
                    try:
                        self.two_gram_dict[key] += self.two_gram_dict[letter]
                    except (Exception, ) as e:
                        pass

                return self.two_gram_dict[key]
            else:
                self.two_gram_dict[key] = 0
                return 0
                # print("I'm {}".format(self))
                # print(e)

    def __repr__(self):
        return self.letter


class Letter_special(Letter):
    def __init__(self, letters, *letter_strs):
        self.letter = ''.join([letter_str for letter_str in letter_strs])
        self.letters = [letters[letter_str] for letter_str in letter_strs]
        self.one_gram = sum([letters[letter_str].one_gram
                             for letter_str in letter_strs])
        self.two_gram_dict = {}

    def __getitem__(self, key):
        cost = 0
        try:
            for letter_obj in self.letters:
                cost += letter_obj.two_gram_dict[str(key)]
        except (Exception, ) as e:
            pass
        return cost




def decide_homepos_fingers_decide_hands(letters):
    top8letters = sorted([(value, value.one_gram) for key,
                          value in letters.items()], key=itemgetter(1), reverse=True)[:8]
    top8letters = set([x[0] for x in top8letters])
    print(top8letters)
    cost_list = []
    for l_hand in list(combinations(top8letters, 4)):
        l_hand = set(l_hand)
        r_hand = top8letters - l_hand
        r_cost = calc_two_gram_cost(r_hand)
        l_cost = calc_two_gram_cost(l_hand)
        r_cost_one_gram = calc_one_gram_cost(r_hand)
        l_cost_one_gram = calc_one_gram_cost(l_hand)
        cost = r_cost + l_cost
        cost_list.append((cost, l_cost, r_cost, l_hand, r_hand,
                          l_cost_one_gram, r_cost_one_gram))
    cost_list.sort(key=itemgetter(0), reverse=False)
    return cost_list


def calc_one_gram_cost(letters):
    return sum([x.one_gram for x in letters])


def calc_two_gram_cost(letters):
    sum_ = 0
    for first_letter in letters:
        for second_letter in letters:
            # print(first_letter, second_letter)
            sum_ += first_letter[second_letter]
    return sum_


def mp(args):
    i, home_pos_finger_patterns, next_letters_patterns, letters = args
    next_letters_patterns_new = []
    for next_letters_pattern in next_letters_patterns:
        for one_set in next_letters_pattern:
            new_pattern = [*next_letters_pattern]
            copy_next_letters_pattern = deepcopy(next_letters_pattern)
            copy_next_letters_pattern.remove(one_set)
            for one_letter in one_set:
                copy_next_letters_pattern.append(set([one_letter, ]))
            next_letters_patterns_new.append(copy_next_letters_pattern)

    scores = []
    for home_pos_finger_pattern in home_pos_finger_patterns:
        for next_letters_pattern in next_letters_patterns_new:
            cost = calc_two_gram_cost2(
                letters, home_pos_finger_pattern, next_letters_pattern)
            scorevals = [x[0] for x in scores]
            max_score = max(scorevals) if len(scores) > 0 else 0
            if max_score == 0 or cost < max_score:
                scores.append((cost, next_letters_pattern,
                               home_pos_finger_pattern))
                scores.sort(key=itemgetter(0), reverse=False)
                scores = scores[:30]
        # print(i, home_pos_finger_pattern)
    return scores


def decide_second_letters(home_pos_fingers, next_letters, letters):
    next_letters_patterns = chunk_combi.chunk_combinations(
        next_letters, chunk_size=2)
    beep()
    p = Pool(7)
    args = [(home_pos_fingers, next_letters_patterns, letters)
            for home_pos_fingers in chunks(permutations(home_pos_fingers), 1000)]
    # args = args[:2]
    # [print(x) for x in args]
    resultList = Poolbar(mp, args)
    print(resultList)
    scores = []
    for result in resultList:
        scores.extend(result)
    scores.sort(key=itemgetter(0), reverse=False)
    scores = scores[:100]
    return scores
    # for next_letters_pattern, home_pos_finger_pattern in product(next_letters_patterns_new, permutations(home_pos_fingers)):
    #     cnt += 1
    #     if cnt % 10000 == 0:
    #         print(cnt)
    #     cost = calc_two_gram_cost2(
    #         letters, home_pos_fingers, next_letters_pattern)
    #
    #     max_score = max(scores, key=itemgetter(0)
    #                     ) if len(scores) > 0 else 0
    #     if cost < max_score:
    #         scores.append((cost, next_letters_pattern,
    #                        home_pos_finger_pattern))
    #         scores.sort(key=itemgetter(0), reverse=False)
    #         scores = scores[:30]
    # return scores
# if __name__ == '__main__':
#
#   argList = [ 1, 2, 3]
#
#   p = Pool()
#   resultList = p.map(twiceFunc, argList)
#   # resultList ... [ 2, 4, 6]
#
#   print(resultList[0], resultList[1], resultList[2])


def calc_two_gram_cost2(letters, home_pos_fingers, second_priority_fingers, min_cost):
    if home_pos_fingers is None:
        home_pos_fingers = ['し', 'と', 'の', 'か', 'た', 'う', 'ん', ]
    if second_priority_fingers is None:
        second_priority_fingers = [{'が', 'っ'}, {'て', 'は'}, {
            'く', 'る'}, {'な', 'き'}, {'に', 'こ'}, {'で'}, {'ょ'}]
    cost = 0
    for home_key, second_keys in zip(home_pos_fingers, second_priority_fingers):
        one_finger_keys = [home_key, *second_keys]
        for key0, key1 in combinations(one_finger_keys, r=2):
            cost += letters[key0][key1] + letters[key1][key0]
    return cost


def cost2gram(letters, *keys):
    cost = 0
    for two_key in combinations(keys, 2):
        f_key, s_key = two_key
        cost += (letters[f_key][s_key] + letters[s_key][f_key])
    return cost


def cost1gram(letters, *keys):
    cost = 0
    for key in keys:
        cost += letters[key].one_gram
    return cost


def preview(res, letters):
    for row in res:
        samefinger_cost, second_keys, first_keys = row
        finger_keys = [(*second_key, first_key)
                       for second_key, first_key in zip(second_keys, first_keys)]
        finger_keys_costs = [(finger_key, cost2gram(letters, *finger_key), cost1gram(letters, *finger_key), [
                              cost1gram(letters, a_finger_key) for a_finger_key in finger_key]) for finger_key in finger_keys]
        [print(x) for x in finger_keys_costs]
        total_1gram_cost = sum([x[2] for x in finger_keys_costs])
        total_2gram_cost = sum([x[1] for x in finger_keys_costs])
        print(total_1gram_cost, total_2gram_cost)
        print(finger_keys)


def hands_classifier(finger_keys, letters):
    finger_keys = set(finger_keys)
    finger_count = len(finger_keys) // 2  # 8//2 = 4
    cross_costs = []  # maximize this
    for left_hand in combinations(finger_keys, finger_count):
        left_hand = set(left_hand)
        rigth_hand = finger_keys - left_hand
        left_keys = []
        [left_keys.extend(left_finger) for left_finger in left_hand]
        rigth_keys = []
        [rigth_keys.extend(rigth_finger) for rigth_finger in rigth_hand]
        # print(left_keys, rigth_keys)
        this_pattern_cross_cost = 0
        for left_key, rigth_key in product(left_keys, rigth_keys):
            this_pattern_cross_cost += cost2gram(letters, left_key, rigth_key)
        left_1gram_cost = cost1gram(letters, *left_keys)
        rigth_1gram_cost = cost1gram(letters, *rigth_keys)
        cross_costs.append((this_pattern_cross_cost, left_hand,
                            rigth_hand, left_1gram_cost, rigth_1gram_cost))
    cross_costs.sort(key=itemgetter(0), reverse=True)
    # cross_costs = cross_costs[:100]
    for this_pattern_cross_cost, left_hand, rigth_hand, left_1gram_cost, rigth_1gram_cost in cross_costs:
        ok = True
        # if all([bool(any([bool(letter in finger) for finger in handside])) for letter, handside in [('い', rigth_hand), ('ん', left_hand), ('は', rigth_hand), ('う', rigth_hand)]]):
        print(left_hand)
        print(rigth_hand)
        print(this_pattern_cross_cost, left_1gram_cost, rigth_1gram_cost)
    return [{('に', 'が', 'の'), ('て', 'ょ', 'と'), ('く', 'ん'), ('で', 'な', 'た')}, {('き', 'こ', 'か'), ('い', '。、', 'ー'), ('る', 'っ', 'う'), ('は', 'し')}]
    # 264122 345309 405861


# def adjust_high(data, letters):
#     for hand in data:
#         # remove home keys
#         for removing_letter in ['し', 'と', 'の', 'か', 'た', 'い', 'う', 'ん', ]:
#             for finger in hand:
#                 finger = set(finger)
#                 finger.discard(removing_letter)
def set_hand_side_to_second_home_keys(second_home_keys, letters, decided_keys):

    pass


if __name__ == '__main__':
    one_gram, two_gram = read_csv()
    letters = create_letters(one_gram, two_gram)
    del letters['い']
    cost_list = decide_homepos_fingers_decide_hands(letters)
    [print(x) for x in cost_list]
    lineno()
    # (39050, 17604, 21446, {し, と, の, か}, {た, い, う, ん}, 163957, 226366)
    [print(letters[x].one_gram, x) for x in [
        'し', 'と', 'の', 'か', 'た',  'う', 'ん', ]]
    home_pos_fingers = ['し', 'と', 'の', 'か', 'た', 'う', 'ん', 'て']
    next_letters = ['く', 'な', 'に', 'き',
                    'う', 'こ', 'る', 'が', 'で', 'っ', 'ょ', '。、', 'す', 'ま']
    # home_pos_fingers.remove('い')
    # next_letters.remove('。')
    if True:
        res = decide_second_letters(home_pos_fingers, next_letters, letters)
    else:
        res = data.new_data
    [print(x) for x in res]
    lineno()
    preview(res, letters)
    picked_from_res = [('で', 'な', 'た'), ('に', 'が', 'の'), ('き', 'こ', 'か'),
                       ('る', 'っ', 'う'), ('て', 'ょ', 'と'), ('く', 'ん'), ('は', 'し')]
    picked_from_res.append(('い', '。、', 'ー'))
    data = hands_classifier(picked_from_res, letters)
    second_home_keys = ['す', 'ま', 'じ', 'り', 'も', 'つ', 'お',
                        'ら', 'を', 'さ', 'あ', 'れ', 'だ', 'ち', 'せ', 'け', ]
    # print(len(list(combinations(second_home_keys, 8))))
    set_hand_side_to_second_home_keys(second_home_keys, letters, data)
    # adjust_high(data, letters)
