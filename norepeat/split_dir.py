import os
import shutil
import argparse


def split_dir(path, remove):
    files = os.listdir(path)
    for f in files:
        if os.path.isdir(f) or len(f.split(".")) == 1:
            continue
        end = f.split(".")[-1]
        if not os.path.exists(path + "/" + end):
            os.makedirs(path + "/" + end)

        src_path = path + "/" + f
        dst_path = path + "/" + end
        if os.path.exists(dst_path + "/" + f):  # If dst file already
            continue
        if remove:
            shutil.move(src_path, dst_path)
        else:
            shutil.copy(src_path, dst_path)

if __name__ == '__main__':
    description = """
    Split files to a new directory for same type 根据文件类型分离目录下文件到不同文件夹
    Eg:
        norepeat split_dir -p=test
        before:
            dir
                a.txt
                b.txt
                a.png
                b.png
        after:
            dir
                txt
                    a.txt
                    b.txt
                png
                    a.png
                    b.png
    """
    parser = argparse.ArgumentParser(description=description,
                                     prog='split_dir',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     )

    parser.add_argument('-p', '--path', help='dir path, use . for current dir')
    parser.add_argument('-r', '--remove', help='if remove src files, default is No', default='')

    args = parser.parse_args()
    try:
        if not args.path:
            raise Exception('Missing params path')
        src_path = args.path if args.path !='.' else os.getcwd()
        split_dir(src_path, args.remove)
    except Exception as e:
        print(str(e))
        print('Use -h to have a try')
