import os
import web_crawl.load_url_data as load_url
import telegram, time

def del_old_log():
    if os.path.isfile('test.log'):
        os.remove('test.log')

if __name__ == "__main__":
    del_old_log()
    os.system("scrapy crawl quotes") # 가맹점마다 재고를 특정할 수 있는 단어의 xpath를 가져와, 검사한다.