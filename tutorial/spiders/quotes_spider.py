import scrapy
import cssutils

class QuotesSpider(scrapy.Spider):
    name = "quotes" # spider name 설정

    def start_requests(self): # 가맹점 url 추가위치
        urls = [
            'http://www.11st.co.kr/products/2935980321',
            'http://www.11st.co.kr/products/2935980321',
            'http://www.ssg.com/item/itemView.ssg?itemId=0000001570515',
            'http://www.ssg.com/item/itemView.ssg?itemId=1000039507427',
            'http://itempage3.auction.co.kr/DetailView.aspx?itemno=C224484103',
            'http://itempage3.auction.co.kr/DetailView.aspx?itemno=B768432406',
            'http://mitem.gmarket.co.kr/Item?goodscode=1808202487',
            'http://mitem.gmarket.co.kr/Item?goodscode=2064152797',
            'https://mw.wemakeprice.com/product/1284302768',
            'https://mw.wemakeprice.com/product/203255871',
            'http://mobile.tmon.co.kr/deals/5262257414',
            'http://mobile.tmon.co.kr/deals/3473350446',
            'https://www.costco.co.kr/p/640013',
            'https://www.costco.co.kr/p/639579',
            'https://smartstore.naver.com/ks1st/products/4497205319',
            'https://smartstore.naver.com/jexco21/products/4952245275'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response): # url을 가져와, 가맹점마다 다른 xpath를 검사
        url = response.url
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
        else:
            print("잘못된 url")

####################### xpath로 특정 단어 찾기 ###########################################################
    def ssg_check(self, response):
        try:
            feature_text = response.xpath('//*[@id="actionPayment"]/span/span/text()').get()
            if '바로구매' in feature_text:
                print('SSG : 재고있음', response.url)
            else:
                print('SSG : ui 변경')
        except:
            print('SSG : 품절', response.url)

    def aution_check(self, response):
        try:
            feature_text = response.xpath('//*[@id="ucItemOrderInfo_ucItemOrderButtons_hdivBuy"]/button[2]/text()').get()
            if '구매하기' in feature_text:
                print('옥션 : 재고있음', response.url)
            else:
                print('옥션 : ui 변경')
        except:
            print('옥션 : 품절', response.url)

    def gmarket_check(self, response):
        try:
            feature_text = response.xpath('//*[@id="vipOptionArea"]/div[1]/div/div/span[1]/a/text()').get()
            if '구매하기' in feature_text:
                print('G마켓 : 재고있음', response.url)
            else:
                print('G마켓 : ui 변경')
        except:
            print('G마켓 : 품절', response.url)

    def wemake_check(self, response):
        try:
            feature_text = response.xpath('//*[@id="_infoDescription"]/div[3]/div[2]/a[2]/span/text()').get()
            if '구매하기' in feature_text:
                print('위메프 : 재고있음', response.url)
            else:
                print('위메프 : ui 변경')
        except:
            print('위메프 : 품절', response.url)

    def tmon_check(self, response):
        try:
            feature_text = response.xpath('//*[@id="prch-controller"]/div[1]/button/text()').get()
            if '구매하기' in feature_text:
                print('티몬 : 재고있음', response.url)
            else:
                print('티몬 : ui 변경')
        except:
            print('티몬 : 품절', response.url)

    def costco_check(self, response):
        try:
            feature_text = response.xpath('//*[@id="buyNowButton"]/text()').get()
            if '바로 결제' in feature_text:
                print('코스트코 : 재고있음', response.url)
            else:
                print('코스트코 : ui 변경')
        except:
            print('코스트코 : 품절', response.url)

    def naver_check(self, response):
        try:
            feature_text = response.xpath('//*[@id="content"]/div/div[2]/div[2]/fieldset/div[8]/ul[1]/li[1]/a/span/text()').get()
            if '구매하기' in feature_text:
                print('네이버 : 재고있음', response.url)
            else:
                print('네이버 : ui 변경')
        except:
            print('네이버 : 품절', response.url)
    
    def eleven_street_check(self, response):
        try:
            feature_text = response.xpath('//*[@id="layBodyWrap"]/div/div[1]/div[2]/div/div[2]/div[3]/div[2]/div[2]/a/text()').get()
            if '구매하기' in feature_text:
                print('11번가 : 재고있음', response.url)
            else:
                print('11번가 : ui 변경')
        except:
            print('11번가 : 품절', response.url)