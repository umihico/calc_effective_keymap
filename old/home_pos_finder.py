from csv_manager import load_ngram_dict
from operator import itemgetter
from gram_data import gram_data
from combinations_func import combinations_count, combinations_with_rest


def main(top_keys):
    patterns = []
    for left_keys, right_keys in combinations_with_rest(top_keys, len(top_keys) // 2):
        L_2gram_cost, R_2gram_cost = [gram_data.get_2gram_cost(
            ''.join(keys)) for keys in [left_keys, right_keys]]
        L_1gram_cost, R_1gram_cost = [gram_data.get_1gram_cost(
            ''.join(keys)) for keys in [left_keys, right_keys]]
        T_2gram_cost = L_2gram_cost + R_2gram_cost
        T_1gram_cost = L_1gram_cost + R_1gram_cost
        patterns.append(
            (''.join(left_keys), L_2gram_cost, L_1gram_cost, ''.join(right_keys), R_2gram_cost, R_1gram_cost, T_2gram_cost, T_1gram_cost))
    patterns.sort(key=itemgetter(-2), reverse=False)
    return patterns


if __name__ == '__main__':
    top_keys = 'うん。しかのとた'
    patterns = main(top_keys)
    for pattern in patterns:
        print(pattern)

    """
    C:\Users\umi\GoogleDrive\code\ergodox\kana>python home_pos_finder.py
    ('うたんと', 13036, 189781, 'かの。し', 15283, 178283, 28319, 368064) I wanna try this
    ('かの。し', 15283, 178283, 'うたんと', 13036, 189781, 28319, 368064)
    ('。うたん', 13712, 204107, 'のかしと', 15710, 163957, 29422, 368064)
    ('のかしと', 15710, 163957, 'う。たん', 13712, 204107, 29422, 368064) I wanna try this
    ('の。うん', 13078, 208621, 'たかしと', 18015, 159443, 31093, 368064)
    ('たかしと', 18015, 159443, 'うの。ん', 13078, 208621, 31093, 368064)
    ('のうたん', 14455, 190164, 'か。しと', 16692, 177900, 31147, 368064)
    ('か。しと', 16692, 177900, 'のうたん', 14455, 190164, 31147, 368064)
    """

    """
    cost_dict_1gram, two_gram_dict = load_ngram_dict()
    sorted_cost_dict_1gram = sorted(
    cost_dict_1gram.items(), key=lambda x: int(x[1]), reverse=True)
    """
    """い get rigth　親指"""
    """for word, count in sorted_cost_dict_1gram:
        print(word, count)
    い 74569 rigth　親指
    う 59235 homepos(1/8)
    ん 58709 homepos(1/8)
    。 52310 homepos(1/8)
    し 48069 homepos(1/8)
    か 39537 homepos(1/8)
    の 38367 homepos(1/8)
    と 37984 homepos(1/8)
    た 33853 homepos(1/8)
    て 27725 firstlayer(1/14)
    く 27579 firstlayer(1/14)
    な 27521 firstlayer(1/14)
    に 27389 firstlayer(1/14)
    き 26011 firstlayer(1/14)
    は 24910 firstlayer(1/14)
    こ 24434 firstlayer(1/14)
    る 24368 firstlayer(1/14)
    が 23074 firstlayer(1/14)
    で 21789 firstlayer(1/14)
    っ 21418 firstlayer(1/14)
    ょ 21319 firstlayer(1/14)
    す 21000 firstlayer(1/14)
    ま 19322 firstlayer(1/14)
    じ 18329
    り 17904
    も 17888
    つ 16984
    お 16377
    ら 16103
    を 15893
    さ 15693
    あ 15658
    れ 14594
    だ 13722
    ち 13140
    せ 12513
    """
