import scrapy, os

class QuotesSpider(scrapy.Spider):
    log = []
    name = "quotes" # spider name 설정
    
    def start_requests(self): # 가맹점 url 추가위치
        urls = [
            'http://www.11st.co.kr/products/3335249590',
            'http://www.ssg.com/item/itemView.ssg?itemId=0000001570515',
            'http://www.ssg.com/item/itemView.ssg?itemId=1000039507427',
            'http://itempage3.auction.co.kr/DetailView.aspx?itemno=C224484103',
            'http://itempage3.auction.co.kr/DetailView.aspx?itemno=B822693636',
            'http://mitem.gmarket.co.kr/Item?goodscode=2134616928',
            'http://mitem.gmarket.co.kr/Item?goodscode=2064152797',
            'https://mw.wemakeprice.com/product/1284302768',
            'https://mw.wemakeprice.com/product/203255871',
            'http://mobile.tmon.co.kr/deals/5262257414',
            'http://mobile.tmon.co.kr/deals/3473350446',
            'https://www.costco.co.kr/rest/v2/korea/products/645803/?fields=FULL&lang=ko&curr=KRW',
            'https://www.costco.co.kr/rest/v2/korea/products/609542/?fields=FULL&lang=ko&curr=KRW'
            'https://smartstore.naver.com/ks1st/products/4497205319',
            'https://smartstore.naver.com/jexco21/products/5222435156',
            'https://www.coupang.com/vp/products/1341628026'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response): # url을 가져와, 가맹점마다 다른 xpath를 검사
        url = response.url
        self.check_stock(response, url)

    def check_stock(self, response, url):
        if 'ssg' in url:
            self.ssg_check(response)
        elif 'auction' in url:
            self.aution_check(response)
        elif 'gmarket' in url:
            self.gmarket_check(response)
        elif 'wemakeprice' in url:
            self.wemake_check(response)
        elif 'tmon' in url:
            self.tmon_check(response)
        elif 'costco' in url:
            self.costco_check(response)
        elif 'naver' in url:
            self.naver_check(response)
        elif '11st' in url:
            self.eleven_street_check(response)
        elif 'coupang' in url:
            self.coupang_check(response)
        else:
            print("잘못된 url")

####################### xpath로 특정 단어 찾기 ###########################################################
    def write_log_exist(self, shop_name, url):
        print(f'{shop_name} : 재고있음', url)
        self.write_log(f'{shop_name} : 재고있음 {url}')

    def write_log_empty(self, shop_name, url):
        print(f'{shop_name} : 품절', url)
        self.write_log(f'{shop_name} : 품절 {url}')

    def find_xpath_text(self, response, shop_name, hint_text, hint_xpath):
        isDebug = False
        feature_text = response.xpath(hint_xpath).get()
        if hint_text in feature_text:
            if isDebug == True:
                self.write_log_exist(shop_name, response.url)
        else:
            print(f'{shop_name} : ui 변경', response.url)

    def write_log(self, text):
        with open('test.log', 'a') as f:
            f.write(text +'\n')

    def check(self, response, shop_name, hint_text, hint_xpath, hint_xpath2 = None):
        try:
            self.find_xpath_text(response, shop_name, hint_text, hint_xpath)
        except:
            if hint_xpath2 != None: # 네이버 xpath가 수시로 바뀜
                try:
                    self.find_xpath_text(response, shop_name, hint_text, hint_xpath2)
                except:
                    self.write_log_empty(shop_name, response.url)    
            else:
                self.write_log_empty(shop_name, response.url)

    def network_file_check(self, response, shop_name): # 코스트코는 iframe
        goods_num = response.url.split('products/')[-1].split('/?fields')[0]
        response_url = 'https://www.costco.co.kr/p/' + goods_num
        if 'outOfStock' in response.text:
            self.write_log_empty(shop_name, response_url)

    def coupang_check(self, response):
        shop_name = '쿠팡'
        hint_text = '바로구매'
        hint_xpath = '//*[@id="contents"]/div[1]/div/div[3]/div[16]/div[2]/div[2]/button[2]/span/text()'
        self.check(response, shop_name, hint_text, hint_xpath)
        
    def ssg_check(self, response):
        shop_name = 'SSG'
        hint_text = '바로구매'
        hint_xpath = '//*[@id="actionPayment"]/span/span/text()'
        self.check(response, shop_name, hint_text, hint_xpath)

    def aution_check(self, response):
        shop_name = '옥션'
        hint_text = '구매하기'
        hint_xpath = '//*[@id="ucItemOrderInfo_ucItemOrderButtons_hdivBuy"]/button[2]/text()'
        self.check(response, shop_name, hint_text, hint_xpath)

    def gmarket_check(self, response):
        shop_name = 'G마켓'
        hint_text = '구매하기'
        hint_xpath = '//*[@id="vipOptionArea"]/div[1]/div/div/span[1]/a/text()'
        self.check(response, shop_name, hint_text, hint_xpath)

    def wemake_check(self, response):
        shop_name = '위메프'
        hint_text = '구매하기'
        hint_xpath = '//*[@id="_infoDescription"]/div[3]/div[2]/a[2]/span/text()'
        self.check(response, shop_name, hint_text, hint_xpath)

    def tmon_check(self, response):
        shop_name = '티몬'
        hint_text = '구매하기'
        hint_xpath = '//*[@id="prch-controller"]/div[1]/button/text()'
        self.check(response, shop_name, hint_text, hint_xpath)

    def costco_check(self, response):
        shop_name = '코스트코'
        self.network_file_check(response, shop_name)

    def naver_check(self, response):
        shop_name = '네이버'
        hint_text = '구매하기'
        hint_xpath = '//*[@id="content"]/div/div[2]/div[2]/fieldset/div[8]/ul[1]/li[1]/a/span/text()'
        hint_xpath2 = '//*[@id="content"]/div/div[2]/div[2]/fieldset/div[7]/ul[1]/li/a/span/text()'
        self.check(response, shop_name, hint_text, hint_xpath, hint_xpath2=hint_xpath2)
    
    def eleven_street_check(self, response):
        shop_name = '11번가'
        hint_text = '구매하기'
        hint_xpath = '//*[@id="layBodyWrap"]/div/div[1]/div[2]/div/div[2]/div[3]/div[2]/div[2]/a/text()'
        self.check(response, shop_name, hint_text, hint_xpath)
