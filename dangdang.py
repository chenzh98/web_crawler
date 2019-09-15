import requests
import re
import json
import pandas as pd


def get_text(url):
    try :
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


def parse_result(html):
    pattern = re.compile(r'<li>.*?list_num.*?(\d+).</div>.*?<img src="(.*?)".*?class="name".*?title="(.*?)">.*?class="star".*?target="_blank">(.*?)</a>.*?class="tuijian">(.*?)</span>.*?class="publisher_info">.*?title="(.*?)".*?class="publisher_info".*?target="_blank">(.*?)</a>.*?class="price".*?class="price_n">&yen;(.*?)</span>.*?</li>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield dict(Rank=item[0], Image=item[1], Name=item[2], Comments=item[3], Recommend=item[4], Author=item[5],
                   Publisher=item[6])


def write_into_file(item):
    print('Start to write the file ====>  ' + str(item))
    with open(r'book.txt', 'a', encoding='UTF-8') as f:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')


def main():
    book_list = []
    for page in range(1, 26):
        url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-' + str(page)
        html = get_text(url)
        items = parse_result(html)
        for item in items:
            write_into_file(item)
            book_list.append(item)
    book_list_table = pd.DataFrame(book_list)
    rank = book_list_table['Rank']
    book_list_table.drop(labels=['Rank'], axis=1, inplace=True)
    book_list_table.insert(0, 'Rank', rank)
    book_list_table.to_csv('book_list.csv', index=False)
    book_list_table.to_excel('book_list.xlsx', index=False)


if __name__ == '__main__':
    main()