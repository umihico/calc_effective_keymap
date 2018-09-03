"""
after first home 8 keys, decide rest 14 keys here.
"""
import itertools
import math
from tqdm import tqdm
from csv_manager import load_ngram_dict
from gram_data import gram_data
from operator import itemgetter
from itertools import combinations
from itertools import product
from itertools import permutations
import csv_wrapper
from combinations_func import combinations_count, combinations_with_rest
from time import sleep, time
from numba import jit
from tabulate import tabulate
import numpy as np
from multiprocessing import Pool
from multiprocessing import current_process
from multiprocessing import cpu_count
import psutil


def calculation(args):
    cost_dict, np_petterns, home_keys, okay_permutations, rest_keys = args
    # min_indexes = [(i, np.ndarray.min(np.dot([cost_dict[(hk, ok, rk)] for hk, ok in zip(
    #     home_keys, okay_keys_sorted) for rk in rest_keys], okay_petterns))) for i, okay_keys_sorted in enumerate(okay_permutations)]
    """check"""
    min_indexes = [
        (i, np.ndarray.min(np.dot([cost_dict[(hk, ok, rk)] for hk, ok in zip(
            home_keys, okay_keys_sorted) for rk in rest_keys], np_petterns))) for i, okay_keys_sorted in enumerate(okay_permutations)
    ]
    """check no list comp
    min_indexes = []
    for i, okay_keys_sorted in tqdm(enumerate(okay_permutations)):
        cost_list = [cost_dict[(hk, ok, rk)] for hk, ok in zip(
            home_keys, okay_keys_sorted) for rk in rest_keys]
        costs = np.dot(cost_list, np_petterns)
        x = (i, np.ndarray.min(costs))
        min_indexes.append(x)
        for j, rest_keys_sorted in enumerate(permutations(rest_keys)):
            cost = sum(cost_dict[key] for key in zip(
                home_keys, rest_keys_sorted, okay_keys_sorted))
            print(bool(cost == costs[j]), cost, costs[j])
        raise
    """
    return [(okay_permutations[i], min_cost) for i, min_cost in min_indexes]


def test(home_keys=None, second_keys=None):
    home_keys = home_keys or 'うたんとかの。し'
    second_keys = second_keys or 'てくなにきはこるがでっょすま:;'
    patterns = []
    cost_dict = {}
    for hk, sk0, sk1 in product(home_keys, second_keys, second_keys):
        pattern = tuple([hk, sk0, sk1])
        patterns.append(pattern)
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

    def gen_okay_permutations(keys, np_petterns):
        cost_list = [cost_dict[(hk, k)]
                     for hk in home_keys for k in keys]
        costs = np.dot(cost_list, np_petterns)
        """check
        for i, keys_sorted in enumerate(permutations(keys)):
            cost = sum(cost_dict[key] for key in zip(home_keys, keys_sorted))
            print(bool(cost == costs[i]))
        """
        okay_permutations = [keys_sorted for cost, keys_sorted in zip(
            costs, permutations(keys)) if cost < 10000]
        return okay_permutations

    petterns_ = [[1 if i == e else 0 for i in ints for e in range(8)]
                 for ints in permutations(range(8))]
    # petterns_ = petterns_[:100]
    petterns = list(zip(*petterns_))
    np_petterns = np.array(petterns)
    # print(np_petterns.shape[0])
    # print(np_petterns.shape[1])
    final_output = []

    tasks = []
    for top_keys, bottom_keys in tqdm(list(combinations_with_rest(second_keys, 8, True))):
        top_keys = [x.replace(';', ':') for x in top_keys]
        bottom_keys = [x.replace(';', ':') for x in bottom_keys]
        if ':' in top_keys and ':' in bottom_keys:
            top_okay_permutations = gen_okay_permutations(
                top_keys, np_petterns)
            bottom_okay_permutations = gen_okay_permutations(
                bottom_keys,  np_petterns)
            okay_permutations, other_keys = (top_okay_permutations, bottom_keys) if len(
                top_okay_permutations) < len(bottom_okay_permutations) else (bottom_okay_permutations, top_keys)
            """costs check
            for i, top_keys_sorted in enumerate(permutations(top_keys)):
                cost = sum(cost_dict[key] for key in zip(
                    home_keys, top_keys_sorted))
                print(bool(cost == costs[i]), cost, costs[i])
            raise
            """
            # final_output.extend(calculation([okay_permutations, other_keys]))

            task = [cost_dict, np_petterns, home_keys,
                    okay_permutations, other_keys]
            print('okay_permutations:', len(okay_permutations))
            tasks.append(task)
            if len(tasks) > 50:
                list_of_list = Poolbar(calculation, tasks)
                list_ = flatten(list_of_list)
                final_output.extend(list_)
                final_output_dict = dict(final_output)
                final_output = list(final_output_dict.items())
                final_output.sort(key=itemgetter(1), reverse=False)
                final_output = final_output[:10000]
                for x in final_output[:10]:
                    print(*x)
                csv_wrapper.save_csv('final_output.csv', final_output)
                tasks = []
            # break
    # costs_list = [calculation(task) for task in tasks]
    # print('a', costs_list)
    # costs_list = Poolbar(calculation, tasks)
    # costs = flatten(costs_list)
    # for cost in costs:
    #     print(cost)

    """
        cost_list = [(hk, tk, bk) for hk, tk in zip(home_keys, top_keys_sorted)
                    for bk in bottom_keys]
        pettern = [1 if i == e else 0 for i in range(8) for e in range(8)]
        for finger_key, digit in zip(cost_list, pettern):
            print(finger_key, digit, bool(digit))
        ('う', 'こ', 'が') 1 True
        ('う', 'こ', 'ょ') 0 False
        ('う', 'こ', 'で') 0 False
        ('う', 'こ', ';') 0 False
        ('う', 'こ', 'ま') 0 False
        ('う', 'こ', ':') 0 False
        ('う', 'こ', 'っ') 0 False
        ('う', 'こ', 'す') 0 False
        ('た', 'く', 'が') 0 False
        ('た', 'く', 'ょ') 1 True
        ('た', 'く', 'で') 0 False
        for ints in itertools.permutations(range(8)):
            print([1 if i == e else i for i in ints for e in range(8)])
            for i in ints:
                print([1 if i == e else i for e in range(8)])
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 2, 2, 2, 2, 3, 3, 3, 1, 3, 3, 3, 3,
            4, 4, 4, 4, 1, 4, 4, 4, 5, 5, 5, 5, 5, 1, 5, 5, 6, 6, 6, 6, 6, 6, 1, 6, 7, 7, 7, 7, 7, 7, 7, 1]
        [1, 0, 0, 0, 0, 0, 0, 0]
        [1, 1, 1, 1, 1, 1, 1, 1]
        [2, 2, 1, 2, 2, 2, 2, 2]
        [3, 3, 3, 1, 3, 3, 3, 3]
        [4, 4, 4, 4, 1, 4, 4, 4]
        [5, 5, 5, 5, 5, 1, 5, 5]
        [6, 6, 6, 6, 6, 6, 1, 6]
        [7, 7, 7, 7, 7, 7, 7, 1]
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 2, 2, 2, 2, 3, 3, 3, 1, 3, 3, 3, 3,
            4, 4, 4, 4, 1, 4, 4, 4, 5, 5, 5, 5, 5, 1, 5, 5, 7, 7, 7, 7, 7, 7, 7, 1, 6, 6, 6, 6, 6, 6, 1, 6]
        [1, 0, 0, 0, 0, 0, 0, 0]
        [1, 1, 1, 1, 1, 1, 1, 1]
        [2, 2, 1, 2, 2, 2, 2, 2]
        [3, 3, 3, 1, 3, 3, 3, 3]
        [4, 4, 4, 4, 1, 4, 4, 4]
        [5, 5, 5, 5, 5, 1, 5, 5]
        [7, 7, 7, 7, 7, 7, 7, 1]
        [6, 6, 6, 6, 6, 6, 1, 6]
        """


def Poolbar(func, iter):
    with Pool(cpu_count()) as p:
        this_process = psutil.Process()
        children = this_process.children(recursive=True)
        all_process = [this_process, *children]
        for process in all_process:
            process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
        return list(tqdm(p.imap(func, iter), total=len(iter)))


def flatten(list_of_list): return [
    item for sublist in list_of_list for item in sublist]


if __name__ == '__main__':
    test(home_keys=None, second_keys=None)
