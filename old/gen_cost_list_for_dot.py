import gram_data
gram_data.gram_data


def __readable_example():
    keys = 'abcde'
    fingers = 'ABC'
    cost_list = [''.join([fin, key]) for key in keys for fin in fingers]
    return cost_list


def gen_cost_list(cost_dict, keys='abcde', fingers='ABC'):
    cost_list = [gram_data.gram_data.get_2gram_cost(
        [*fin, key]) for key in keys for fin in fingers]
    return cost_list


def gen_cost_list_only_additional_cost(cost_dict, keys='abcde', fingers='ABC'):
    cost_list = [
        gram_data.gram_data.get_2gram_cost([*fin, key]) -
        gram_data.gram_data.get_2gram_cost(fin)
        for key in keys for fin in fingers]
    return cost_list


if __name__ == '__main__':
    from gen_pattern_for_dot import gen_pattern, gen_fieldnames
    fieldnames = gen_fieldnames(keys='abcde', fingers='ABC')
    print(fieldnames)
    print(__readable_example())
    # p= gen_pattern(keys='abcde', fingers='ABC')
    # l.extend(p)
    # print(tabulate(l[: 30]))
