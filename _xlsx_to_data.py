from umihico_commons.xlsx_wrapper import load_xlsx
from umihico_commons.functools import save_as_txt

filenames = ["raw1gram.xlsx", "raw2gram.xlsx"]
new_filenames = ["dict1gram.txt", "dict2gram.txt"]
for filename, new_filename in zip(filenames, new_filenames):
    rows = load_xlsx(filename)
    dict_ = {key: int(count.replace(".0", ''))
             for count, key, gramtype in rows}
    print(new_filename)
    save_as_txt(new_filename, dict_)
