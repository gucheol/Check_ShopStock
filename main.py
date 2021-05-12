import os
import web_crawl.load_url_data as load_url

if __name__ == "__main__":
    load_url.main() # 일부 가맹점, 동적웹페이지 처리, 일반적으로 크롤링하면 데이터가 없다.
    os.system("scrapy crawl quotes") # 가맹점마다 재고를 특정할 수 있는 단어의 xpath를 가져와, 검사한다.