import csv


def _open(path, mode):
    return open(path, mode, encoding='UTF-8', newline='')


# def _iter_common(old_rows, func):
#     for row in old_rows:
#         func(row)


def save_csv(path, list_of_list):
    with _open(path, mode='w') as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        w.writerows(list_of_list)


def load_csv(path):
    with _open(path, mode='r') as f:
        csv_ = csv.reader(f)
        rows = list(csv_)
    return rows


def save_csv_dict(path, list_of_dict):
    fieldnames = set()
    for dict_ in list_of_dict:
        for key in dict_.keys():
            fieldnames.add(key)
    fieldnames = list(fieldnames)
    with _open(path, mode='w') as f:
        w = csv.DictWriter(f, fieldnames, restval="__NoValue__")
        fieldnames = {k: k for k in fieldnames}
        list_of_dict.insert(0, fieldnames)
        w.writerows(list_of_dict)


def load_csv_dict(path):
    with _open(path, mode='r') as f:
        csv_ = csv.DictReader(f)
        rows = []
        for row in csv_:
            row = dict(row)
            row = {k: v for k, v in row.items() if v != "__NoValue__"}
            rows.append(row)
    return rows


if __name__ == '__main__':
    test_file_name = 'test_csv.csv'
    list_of_list = [
        ['a', 'b', 'c'],
        ['1', '2', '3'],
    ]
    save_csv(test_file_name, list_of_list)
    print(load_csv(test_file_name))

    list_of_dict = [
        {'a': 'b', 'c': 'd'},
        {1: 2, 3: 4},
    ]
    save_csv_dict(test_file_name, list_of_dict)
    print(load_csv_dict(test_file_name))
