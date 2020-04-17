# coding: utf-8
"""
The spell check is checking word spelling correct in project
"""
import os
import enchant
import argparse
import re

WORD_CHECK = {}
WORD_IGNORE = []

def camel2underscore(camelized_str):
    """
    Convert AbcDefGo value to abc_def_go, is used for split Camel-Case word
    """
    first_cap_re = re.compile('(.)([A-Z][a-z]+)')
    all_cap_re = re.compile('([a-z0-9])([A-Z])')

    sub1 = first_cap_re.sub(r'\1_\2', camelized_str)
    return all_cap_re.sub(r'\1_\2', sub1).lower()

def find_word(content):
    pat = '[a-zA-Z]+'
    words_english = re.findall(pat, content.decode('utf-8'))
    return words_english

def check_file(ent, file_path):
    try:
        with open(file_path, 'rb') as f_p:
            for line in f_p:
                words_line = line.strip()
                if words_line:
                    check_words_each_line(ent, words_line)
    except Exception as ex:
        print(str(ex))

# def support_file_type():
#     return ['.go', '.yaml', '.md', '.sh', '.rst']

def check_words_each_line(ent, words_line):
    """

    :param ent:
    :param words_line:
    :return:
    """
    words_english = find_word(words_line)
    for word in words_english:
        if word_is_need_check(word):
            # Convert AbcDefGo value to abc_def_go, is used for split Camel-Case word
            # Split GetClientOutOfClusterOrDie to [get client out of cluster or die]
            word_split = camel2underscore(word).split('_')
            for w_d_p in word_split:
                if w_d_p and word_is_need_check(w_d_p):
                    WORD_CHECK[word] = 1 if check_word_typo(ent, w_d_p) else 0

def word_is_need_check(w_d):
    """Skip check if False"""
    return w_d.lower() not in [w_c.lower() for w_c in (list(WORD_CHECK.keys()) + WORD_IGNORE)]

def check_word_typo(ent, word):
    """
    spell check word
    """
    return not ent.check(word)

def walk_file(pathname):
    """
    :param pathname:
    :return:Wal all files in path
    """
    all_files = []
    for root, _, files in os.walk(pathname):
        for f_s in files:
            all_files.append(os.path.join(root, f_s))
    return all_files

def check_spell(ent, full_pathname):
    """
    check all spell word in path_name
    """
    if os.path.isfile(full_pathname):
        # if os.path.splitext(full_pathname)[1] in support_file_type():
        check_file(ent, full_pathname)
    elif os.path.isdir(full_pathname):
        all_files = walk_file(full_pathname)
        for f_i in all_files:
            # if os.path.splitext(f_i)[1] in support_file_type():
            check_file(ent, f_i)

def write_word_to_file(words):
    """
    Write words to file
    """
    with open('spell_check_wrong.txt', 'w+') as s_p:
        for word in words:
            s_p.writelines(word)
            s_p.writelines('\n')

def set_word_ignore():
    """Skip check word in ignore file"""
    global WORD_IGNORE
    if not os.path.isfile("spell_check_ignore.txt"):
        with open('spell_check_ignore.txt', 'a+') as s_p:
            WORD_IGNORE = []
    else:
        with open('spell_check_ignore.txt', 'r+') as s_p:
            WORD_IGNORE = [str(w_i.replace('\n', '')).lower() for w_i in s_p.readlines()]


def main(path):
    if not os.path.exists(path):
        print('The path {} is invalid'.format(path))
        return

    ent = enchant.Dict("en_US")
    set_word_ignore()
    check_spell(ent, path)

    write_word_to_file([k for k, v in WORD_CHECK.items() if v == 1])


if __name__ == '__main__':
    description = """
    It's used to check en-US word typo in project
    spell-check用来检查项目中英文单词拼写问题
    Eg:
        norepeat spell_check -p=test
    output:
        spell_check_ignore.txt : ignore checking words 
        spell_check_wrong.txt : wrong spell words
    """
    parser = argparse.ArgumentParser(description=description,
                                     prog='spell_check',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     )

    parser.add_argument('-p', '--path', help='directory path')

    args = parser.parse_args()
    try:
        if not args.path:
            raise Exception('Missing params path')
        main(args.path)
    except Exception as e:
        print(str(e))
        print('Use -h to have a try')
