"""
일방적인 크롤링 방법으론 데이터를 얻을 수 없어서 만든 스크립트
(동적 웹페이지?)
적용 가맹점 : 쿠팡
url 정보 : https://m.coupang.com/vm/products/1487807826 -> https://m.coupang.com/vm/v4/enhanced-pdp/products/1487807826
웹페이지 네트워크 검사를 통하여 오른쪽 url 주소를 알아내고 정보를 뽑아야한다.
스크립트 동작 과정 :
1. url data 정보를 .json 으로 json 폴더에 저장
2. stock 과 관련된 value 위치를 찾아 검사
"""
import json
import os
import glob
############## URL DATA DOWNLOAD ##############
def url_json_data_download(url_dict, download_folder_path):
    for url_key in url_dict:
        json_name = url_key
        url = url_dict[url_key]
        download_path = os.path.join(download_folder_path, json_name)
        os.system(f"scrapy fetch --nolog {url} > {download_path}")
############## 가맹점 stock check ##############
def all_url_stock_check(json_file_path, url_dict): # 가맹점 추가 시, 수정해야 됨
    if 'cupang' in json_file_path:
        cupang_check(json_file_path, url_dict)
    else:
        print('unknown json')

def cupang_check(json_file_path, url_dict): # 가맹점 추가 시, 이런 방식으로 추가해야 됨
    with open(json_file_path) as json_file:
        json_data = json.load(json_file)
    hint_text = json_data['rData']['vendorItemDetail']['item']['stockStatusDescription'][0]['text']
    print_stock_status(json_file_path, url_dict, hint_text)

############### util ##############
def print_stock_status(json_file_path, url_dict, hint_text):
    json = os.path.basename(json_file_path)
    url = url_dict[json]
    json_name = json.split('.')[0]
    print(f'{json_name} : {hint_text} {url}')
############# main ################
def main():
    url_dict = {
        'cupang_1.json' : 'https://m.coupang.com/vm/v4/enhanced-pdp/products/1487807826',
        'cupang_2.json' : 'https://m.coupang.com/vm/v4/enhanced-pdp/products/230257151'
    }
    json_folder_path = os.path.abspath(os.path.join(__file__, '..', 'json'))

    url_json_data_download(url_dict, json_folder_path)

    json_file_list = glob.glob(f'{json_folder_path}/*.json')
    for json_file_path in json_file_list:       
        all_url_stock_check(json_file_path, url_dict)


if __name__ == '__main__':
    main()
