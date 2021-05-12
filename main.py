import os
import web_crawl.load_url_data as load_url
# import telegram

# def read_log():
#     log_path = os.path.abspath(os.path.join(__file__, '..', 'test.log'))
#     f = open(log_path, 'r', encoding='utf8')
#     text = f.read()
#     f.close()
#     return text

# def send_message_to_telegram(text):
#     HTTP_token = "1807456494:AAEc8mICKrJCQT8Xp2Ioo51aB6PPNtkI9-c"
#     chat_id_number = "1274502069"
#     bot = telegram.Bot(token=HTTP_token)
#     bot.sendMessage(chat_id=chat_id_number, text=text)

if __name__ == "__main__":
    load_url.main() # 일부 가맹점, 동적웹페이지 처리, 일반적으로 크롤링하면 데이터가 없다.
    os.system("scrapy crawl quotes") # 가맹점마다 재고를 특정할 수 있는 단어의 xpath를 가져와, 검사한다.
    # text = read_log() # 저장한 가맹점재고 결과 로그 불러오기
    # send_message_to_telegram(text) # 텔레그램으로 메시지 보내기