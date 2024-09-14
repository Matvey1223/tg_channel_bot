import requests

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

json_data = {
    'messages': [
        {
            'role': 'user',
            'content': 'привет',
        },

    ],
    'model': 'gpt-3.5-turbo',
    'temperature': 0.5,
    'presence_penalty': 0,
    'frequency_penalty': 0,
    'top_p': 1,
}

response = requests.post('https://chat.fstha.com/api/openai/v1/chat/completions', headers=headers, json=json_data)
result = response.json()
print(result)
result = result['choices'][0]['message']['content']
print(result)