import ast
import concurrent
import json
import concurrent.futures
import time
from database import database as db
import requests
import asyncio
from bs4 import BeautifulSoup
from loguru import logger

class ParseSourcesTg():
    def __init__(self):
        self.urls = db.select_sources()
        self.url = self.change_tg_urls()
        # print(self.url)

    def change_tg_urls(self):
        for i in range(len(self.urls)):
            if 't.me' in self.urls[i][0]:
                self.urls[i] = self.urls[i][0][:13] + 's/' + self.urls[i][0][13:]
            else:
                self.urls[i] = self.urls[i][0]
        return self.urls

    def fetch_url(self, url):
        headers = {
            'authority': 't.me',
            'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        posts = soup.find_all('div', class_ = 'tgme_widget_message_wrap js-widget_message_wrap')
        last_post = posts[-1]
        a_tag = soup.find_all('a', class_='tgme_widget_message_photo_wrap')[-1]
        style_attribute = a_tag['style']
        start_index = style_attribute.find("('") + 2
        end_index = style_attribute.find("')")
        image_url = style_attribute[start_index:end_index]
        return last_post.text.strip().replace('\n', '*'), image_url


    def send_request(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(self.fetch_url, self.url))
        for res in range(len(results)):
            db.add_new(self.urls[res], results[res][0], results[res][1])

    def gpt_request(self):
        self.send_request()
        all_news = db.select_news()
        print(all_news)
        final = []
        headers = {
            'authority': 'chat.fstha.com',
            'accept': '*/*',
            'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'authorization': 'Bearer ak-chatgpt-nice',
            'content-type': 'application/json',
            # 'cookie': '_ga=GA1.1.510188668.1708803636; _ga_4R749CZ0MY=GS1.1.1708803636.1.1.1708805181.0.0.0',
            'origin': 'https://chat.fstha.com',
            'referer': 'https://chat.fstha.com/',
            'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
            'x-requested-with': 'XMLHttpRequest',
        }

        for i in range(len(all_news)):
             logger.info(all_news[i][1])
             json_data = {
                 'question': '{} \n Убери из этой новости все лишнее, рекламу и прочие ссылки. Оставь только новость!!! И если новость на другом языке, то переводи на русском.'.format(
                    all_news[i][1]),
                 'chat_id': '65d7c82c2a21dfc146e34d36',
                 'timestamp': 1708640306883
             }
             json_data = {
                 'messages': [
                     {
                         'role': 'user',
                         'content': '{} \n Убери из этой новости все лишнее, рекламу и прочие ссылки. Оставь только новость!!!'.format(
                    all_news[i][1]),
                     },

                 ],
                 'model': 'gpt-3.5-turbo',
                 'temperature': 0.5,
                 'presence_penalty': 0,
                 'frequency_penalty': 0,
                 'top_p': 1,
             }
             response = requests.post('https://chat.fstha.com/api/openai/v1/chat/completions', headers=headers,
                                      json=json_data)
             result = response.json()
             string = result['choices'][0]['message']['content']
             logger.info(string)
             db.add_new_gpt(self.urls[i], string) #кидаем все новости по очереди в бд
             time.sleep(10)


    def gpt_response(self):
        self.gpt_request()
        # db.clear_news_gpt()



# while True:
#     parser.gpt_response()
#     db.clear_news_gpt()
#     db.clear_news_table()
# parser.gpt_request()


