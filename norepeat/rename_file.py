import os
import argparse

def rename_multiples(dir_path, prefix='', suffix='', remove=False):
    i = 0
    for filename in os.listdir(dir_path):
        file_type = filename.split('.')[1]
        file_name = filename.split('.')[0]
        src = dir_path  + '/' + filename
        if remove:
            dst = prefix + file_name + suffix + str(i) + '.' +file_type
        else:
            dst = prefix + suffix + str(i) + '.' + file_type

        dst = dir_path + '/' + dst

        os.rename(src, dst)
        i += 1


if __name__ == '__main__':
    description = """
    Rename multiple file names  批量重命名
    Eg:
        norepeat rename_file -d=test -p=test -s=end -r=true -i=true
        before:
            dir
                a.txt
                b.txt
        after:
            dir
                testaend1.txt
                testbend1.txt
        
    """
    parser = argparse.ArgumentParser(description=description,
                                     prog='rename_file',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     )

    parser.add_argument('-d', '--dir_path', help='directory path')
    parser.add_argument('-p', '--prefix', help='new file name prefix', default='')
    parser.add_argument('-s', '--suffix', help='new file name suffix', default='')
    parser.add_argument('-r', '--remove', help='new file name with removing src name', default=False)
    parser.add_argument('-i', '--id', help='new file name need id', default=True)


    args = parser.parse_args()
    try:
        src_path = args.dir_path if args.dir_path !='.' else os.getcwd()
        rename_multiples(src_path, args.prefix, args.suffix, args.remove)
    except Exception as e:
        print(str(e))
        print('Use -h to have a try')
