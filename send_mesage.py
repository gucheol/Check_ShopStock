import telegram
import os

def read_log():
    log_path = os.path.abspath(os.path.join(__file__, '..', 'test.log'))
    f = open(log_path, 'r', encoding='utf8')
    text = f.read()
    f.close()
    return text

def send_message_to_telegram(text):
    HTTP_token = "1807456494:AAEc8mICKrJCQT8Xp2Ioo51aB6PPNtkI9-c"
    chat_id_number = "1274502069"
    bot = telegram.Bot(token=HTTP_token)
    bot.sendMessage(chat_id=chat_id_number, text=text)

if __name__ == '__main__':
    if os.path.isfile('test.log'):
        text = read_log() # 저장한 가맹점재고 결과 로그 불러오기
        send_message_to_telegram(text) # 텔레그램으로 메시지 보내기