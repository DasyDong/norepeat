#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
1.difflib的HtmlDiff类创建html表格用来展示文件差异，通过make_file方法
2.make_file方法使用
make_file(fromlines, tolines [, fromdesc][, todesc][, context][, numlines])
用来生成一个包含表格的html文件，其内容是用来展示差异。
fromlines和tolines,用于比较的内容，格式为字符串组成的列表
fromdesc和todesc，可选参数，对应的fromlines,tolines的差异化文件的标题，默认为空字符串
context 和 numlines，可选参数，context 为True时，只显示差异的上下文，为false，显示全文，numlines默认为5，
当context为True时，控制展示上下文的行数，当context为false时,控制不同差异的高亮之间移动时“next”的开始位置
3.使用argparse传入两个需要对比的文件
"""
import difflib
import argparse
import sys
import os


# 创建打开文件函数，并按换行符分割内容
def readfile(filename):
    try:
        with open(filename, 'r') as fileHandle:
            text = fileHandle.read().splitlines()
        return text
    except IOError as e:
        print("Read file Error:", e)
        sys.exit()

# 比较两个文件并输出到html文件中
def diff_file(filename1, filename2):
    text1_lines = readfile(filename1)
    text2_lines = readfile(filename2)
    d = difflib.HtmlDiff(wrapcolumn=80)
    # context=True时只显示差异的上下文，默认显示5行，由numlines参数控制，context=False显示全文，差异部分颜色高亮，默认为显示全文
    result = d.make_file(text1_lines, text2_lines, filename1, filename2, context=True)
    return result

def write_diff_file(filename1, filename2):
    result = diff_file(filename1, filename2)
    # 内容保存到result.html文件中
    with open('result.html', 'w') as resultfile:
        resultfile.write(result)

# 比较两个目录中相同并输出到html文件中
def write_diff_dirs(dir1, dir2):
    dir1_names_dict = gen_names_list(dir1, {})
    dir2_names_dict = gen_names_list(dir2, {})
    same_names = dir1_names_dict.keys() & dir2_names_dict.keys()
    same_names = sorted(list(same_names))
    results = []
    for name in same_names:
        results.append(diff_file(dir1_names_dict.get(name), dir2_names_dict.get(name)))

    added_names = dir2_names_dict.keys() - dir1_names_dict.keys()
    removed_names = dir1_names_dict.keys() - dir2_names_dict.keys()

    # 内容保存到result.html文件中
    with open('result.html', 'w') as resultfile:
        d = difflib.HtmlDiff(wrapcolumn=80)
        result = d.make_file(removed_names, added_names, '缺失文件： \n\r', '新增文件： \n\r',  context=True)
        resultfile.write(''.join(result))
        resultfile.write(''.join(results))


def gen_names_list(dir1, names_dict):
    # 列出path下的文件和文件夹，不包括子文件和子文件夹
    file_list = os.listdir(dir1)
    # 遍历列出的文件及文件夹，如果是文件夹，递归查找，如果是文件，则统计代码行数
    for filename in file_list:
        # path和filename，共同组成查询出的某个文件或文件夹完整路径
        file_path = os.path.join(dir1, filename)
        # 如果是文件夹
        if os.path.isdir(file_path):
            # 递归查找
            gen_names_list(file_path, names_dict)
        else:  # 是文件
            names_dict[filename] = file_path
    return names_dict


if __name__ == '__main__':
    description = """
    Compare two files
    对比两个文件差异
    Eg:
        norepeat diff_file -p1=a.md -p2=b.md
    Compare all files that have same name in two dirs including recursive subdirs
    对比迭代所有文件夹下重名文件内容差异(可以跨文件目录搜索文件， 打包输出到一个result文件)
    Eg:
        norepeat diff_file -d1=python-norepeat/norepeat/ -d2=python-norepeat/test/
    """
    parser = argparse.ArgumentParser(description=description,
                                     prog='diff_file',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     )

    parser.add_argument('-p1', '--path1', help='file path')
    parser.add_argument('-p2', '--path2', help='file path')

    parser.add_argument('-d1', '--dir_path1', help='dir path')
    parser.add_argument('-d2', '--dir_path2', help='dir path')

    args = parser.parse_args()
    try:
        if args.path1 and args.path2:
            write_diff_file(args.path1, args.path2)
        elif args.dir_path1 and args.dir_path2:
            write_diff_dirs(args.dir_path1, args.dir_path2)
    except Exception as e:
        print(str(e))
        print('Use -h to have a try')
