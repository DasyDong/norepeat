# -*- coding:utf-8 -*-
import re
import argparse
d = {"#": 1, "##": 2, "###": 3, "####": 4, "#####": 5, "######": 6}
pattern = '#+\s'


def gan_menu(filename, is_prefix=''):

    def convert(f, f2, is_prefix, toc=False):

        head_id = 0
        skip_convert_in_code = 0
        for i in f.readlines():
            ## skip origin toc
            if '- [' in i:
                continue
            # check if # in code
            if '```' in i:
                skip_convert_in_code += 1

            # If just for toc, have a check regex #
            if toc:
                if not re.match(pattern, i.strip(' \t\n')):
                    continue
                else:
                    if skip_convert_in_code % 2 != 0:
                        continue
            else:
                if not re.match(pattern, i.strip(' \t\n')):
                    f2.write(i)
                    continue

            i = i.strip(' \t\n')
            head = i.split(' ')[0]

            if is_prefix and head.count('#') == 3:
                head_id += 1
                prefix = str(head_id)
                prefix_dot = prefix + "."
            else:
                prefix = ''
                prefix_dot = ''

            # Generate toc structure: - [1.python](#1python)
            pre_str = i[:len(head)] + " "
            suf_str = i[len(head):].strip(' \t\n')
            # update origin prefix
            split_str = suf_str.split('.')
            if suf_str and suf_str[0].isdigit() and len(split_str) != 1:

                try:
                    if int(split_str[0]):
                        suf_start_index = len(head) + len(split_str[0])
                        suf_str = i[suf_start_index+2:]
                except:
                    pass

            if toc:
                blank_prvit = ' ' * (len(head) - 1) * 4 + '- '
                new_title = '['  + prefix_dot + suf_str + '](#'
                # blank should replace -
                # others should r4place by empty
                p = re.compile(r"[,$().#+&*:?{}=，'？。（）、/!@%^-]")
                suf_str = re.sub(p, "", suf_str).replace(' ', '-').lower()

                if head_id != 0:
                    tag = prefix + suf_str + ')   \n'
                else:
                    tag = suf_str + ')   \n'

                final_after_convert = blank_prvit + new_title + tag
            else:
                final_after_convert = pre_str + prefix_dot + suf_str + '\n'

            f2.write(final_after_convert)


    targetname = filename.split('.')[0] + "_bak.md"
    with open(targetname, 'w+') as f2:
        with open(filename, 'r') as f:
            convert(f, f2, is_prefix, toc=True)
        with open(filename, 'r') as f:
            convert(f, f2, is_prefix)


if __name__ == '__main__':
    description = """
    Generate markdown Menu(TOC(Table of Content)) automatically
    生成Markdown TOC目录结构， 对###三层可以增加自动序号
    Eg:
        norepeat gen_markdown_menu -n=sample.md
        - [Python](#python)
            - [markdown](#markdown)
        OR
        - [Python](#python)
            - [1.markdown](#1markdown)
    
    then you will get a sample_back.md with contents
    sample_back.md is new generated file including menu
    """

    parser = argparse.ArgumentParser(description=description,
                                     prog='gen_markdown_menu',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     )
    parser.add_argument('-n', '--name', help='file name')
    parser.add_argument('-p', '--prefix', help='auto generate num prefix for menu', default='')
    args = parser.parse_args()

    try:
        gan_menu(args.name, args.prefix)
    except Exception as e:
        print(str(e))