import os
import shutil
import argparse



def merge_dir(path, dst_path):
    files = os.listdir(path)
    for f in files:
        sub_path = path + "/" + f
        if os.path.isdir(sub_path):
            merge_dir(sub_path, dst_path)
        else:
            src_path = path + "/" + f
            if not os.path.exists(dst_path):
                os.makedirs(dst_path)

            if os.path.exists(dst_path + "/" + f): # If dst file already
                continue
            shutil.copy(src_path, dst_path)
            print(src_path)

if __name__ == '__main__':
    description = """
    Merge all dirs files to a same directory named 'merge'
    合并迭代所有目录文件夹， 将全部文件合并到merge文件夹下
    Eg:
        norepeat merge_dir -p=test
        before:
            dir
                txt
                    txt2
                        c.txt
                    a.txt
                    b.txt
                png
                    a.png
                    b.png
        after:
            dir
                merge
                    a.txt
                    b.txt
                    c.txt
                    a.png
                    b.png
    """
    parser = argparse.ArgumentParser(description=description,
                                     prog='merge_dir',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     )

    parser.add_argument('-p', '--path', help='dir path, use . for current dir')

    args = parser.parse_args()
    try:
        if not args.path:
            raise Exception('Missing params path')
        src_path = args.path if args.path !='.' else os.getcwd()
        dst_path = src_path + "/merge"
        merge_dir(src_path, dst_path)
    except Exception as e:
        print(str(e))
        print('Use -h to have a try')
