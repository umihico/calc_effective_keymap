from csv_manager import load_ngram_dict, load_ngram_dict_separated
from operator import itemgetter
import itertools


class GramData():
    def __init__(self):
        cost_dict_1gram, two_gram_dict = load_ngram_dict()
        self.cost_dict_1gram = cost_dict_1gram
        self.two_gram_dict = two_gram_dict

    def get_2gram_cost(self, keys):
        sum_ = 0
        for x in itertools.combinations(keys, 2):
            key = ''.join(x)
            if key in self.two_gram_dict:
                sum_ += self.two_gram_dict[key]
            else:
                print(f'{key} is missing in GramData.two_gram_dict')
        return sum_

    def get_1gram_cost(self, keys):
        return sum(self.cost_dict_1gram.get(key, 0) for key in keys)


class GramDataSeparated(GramData):
    def __init__(self):
        cost_dict_1gram, separated_two_gram_dict = load_ngram_dict_separated()
        self.cost_dict_1gram = cost_dict_1gram
        self.two_gram_dict = separated_two_gram_dict

    def get_2gram_cost(self, front_keys, back_keys):
        sum_ = 0
        for key_tuple in itertools.product(front_keys, back_keys):
            key = ''.join(key_tuple)
            if key in self.two_gram_dict:
                sum_ += self.two_gram_dict[key]
            else:
                print(f'{key} is missing in GramData.two_gram_dict')
        return sum_


class GramRanking():
    def __init__(self, gram_data):
        self.gram_data = gram_data

    def print_1gram_ranking(self, print_=True):
        rank_list = list(self.gram_data.cost_dict_1gram.items())
        rank_list.sort(key=itemgetter(1), reverse=True)
        for key, count in rank_list:
            if print_:
                print(key, count)
        return rank_list


gram_data = GramData()
gram_data_separated = GramDataSeparated()
gram_ranking = GramRanking(gram_data)


if __name__ == '__main__':
    print(gram_data.get_2gram_cost('あう'))
    print(gram_data.get_2gram_cost('あい'))
    print(gram_data.get_2gram_cost('うい'))
    print(gram_data.get_2gram_cost('うあい'))
    print(gram_data.get_1gram_cost('あ'))
    print(gram_data.get_1gram_cost('い'))
    print(gram_data.get_1gram_cost('う'))
    print(gram_data.get_1gram_cost('うあい'))
    gram_ranking.print_1gram_ranking()
