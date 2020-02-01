# coding:utf-8
import os
import argparse

# 定义外部变量，做全局记录用
code_lines = 0


# 定义函数
def get_lines_by_suffix(path, suffix):
    # 设置code_lines为全局变量
    global code_lines
    # 列出path下的文件和文件夹，不包括子文件和子文件夹
    file_list = os.listdir(path)
    # 遍历列出的文件及文件夹，如果是文件夹，递归查找，如果是文件，则统计代码行数
    for filename in file_list:
        # path和filename，共同组成查询出的某个文件或文件夹完整路径
        file_path = os.path.join(path, filename)
        # 如果是文件夹
        if os.path.isdir(file_path):
            # 递归查找
            get_lines_by_suffix(file_path, suffix)
        else: # 是文件
            # 判断后缀
            if file_path.split(".")[-1] == suffix:
                # 统计代码行数
                code_lines += get_lines(file_path)
                # 打印查看
                print(code_lines, file_path)
    # 递归查找完毕，返回全部代码条数
    return code_lines


# 定义函数，用于计算单个文件中的代码的函数
def get_lines(file):
    # 打开（连接）文件
    with open(file, encoding="utf-8") as f:
        # 获取读取到的行数，也即文件中代码的行数
        return len(f.readlines())

if __name__ == '__main__':
    description = """
    Count summary codes lines/统计代码行数
    Eg:
        norepeat count_code_nums -p=project -t=py
    """
    parser = argparse.ArgumentParser(description=description,
                                     prog='count_code_nums',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     )

    parser.add_argument('-p', '--path', help='file/directory path')
    parser.add_argument('-t', '--type', help='file type', default='py')
    args = parser.parse_args()
    if args.path and args.type:
        # 测试验证
        src_path = args.path if args.path !='.' else os.getcwd()
        code_lines = get_lines_by_suffix(src_path, args.type)
        print(code_lines)
    else:
        print('Invalid path or type, use -h to have a try')

