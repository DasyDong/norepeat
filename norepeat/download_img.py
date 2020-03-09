# coding : utf-8
import requests
import argparse
import os


def download_img(img_url, name):
    print (img_url)
    r = requests.get(img_url, stream=True)
    print(r.status_code)
    if r.status_code == 200:
        dir_current = os.getcwd()
        open(dir_current + '/' + name +'.png', 'wb').write(r.content)
        print("done")
    del r


if __name__ == '__main__':
    description = """
    Download image to current directory
    Eg:
        norepeat download_img -u=https://test.png -n=test.png
    """
    parser = argparse.ArgumentParser(description=description,
                                     prog='download_img',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     )
    parser.add_argument('-u', '--url', help='img url')
    parser.add_argument('-n', '--name', help='image name')
    args = parser.parse_args()

    try:
        download_img(args.url, args.name)
    except Exception as e:
        print(str(e))
        print('Use -h to have a try')