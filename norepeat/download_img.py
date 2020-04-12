# coding : utf-8
import requests
import argparse
import os


def download_img(img_url, name):
    print (img_url)
    if not name:
        try:
            name = img_url.split('/')[-1].split('.')[0]
        except:
            name = img_url[:-10]
    r = requests.get(img_url, stream=True)
    print(r.status_code)
    if r.status_code == 200:
        dir_current = os.getcwd()
        open(dir_current + '/' + name +'.png', 'wb').write(r.content)
        print("done")
    del r


if __name__ == '__main__':
    description = """
    Download image to current directory 下载网络图片到本地目录
    Eg:
        norepeat download_img -u=https://a.trip.com/a/b/test.png
        norepeat download_img -u=https://a.trip.com/a/b/test.png -n custom
        
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