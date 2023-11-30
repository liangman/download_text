import requests
import sqlite3
from bs4 import BeautifulSoup
import time

def get_html_content(url):
    try:
        # 发送HTTP GET请求
        response = requests.get(url)
        response.raise_for_status()  # 检查是否请求成功
        return response.text  # 返回HTML内容
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("Oops, something went wrong:",err)

    return ''

def parse_html(html_content):
    content = ''
    next_url = ''
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 找到特定的<div class="word_read">
    word_read_div = soup.find('div', class_='word_read')
    if word_read_div:
        # 在该<div>下查找下一章的链接（a标签的href值）
        next_chapter_link = word_read_div.find('a', string='下一章')
        if next_chapter_link:
            next_chapter_href = next_chapter_link.get('href')
            print("下一章的链接:", next_chapter_href)
            next_url = next_chapter_href

        # 在该<div>下查找所有p标签的内容
        paragraphs = word_read_div.find_all('p')
        for paragraph in paragraphs:
            #print("p标签内容:", paragraph.get_text())
            content += paragraph.get_text() + '\n'
    else:
        print("未找到<div class='word_read'>标签")

    return [content, next_url]

def down_text(host, uri, filename):
    # 连接到 SQLite 数据库（如果不存在则会创建）
    conn = sqlite3.connect('./example.db')

    # 创建一个游标对象，用于执行 SQL 语句
    cursor = conn.cursor()

    # 创建一个表格
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS texts (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            filename TEXT,
            url TEXT,
            content TEXT,
            UNIQUE(filename, url)
        )
    ''')

    while True:
        html_content = get_html_content(host+uri)

        if len(html_content) > 0:
            result = parse_html(html_content)

            if len(result[0]) == 0 or len(result[1]) == 0:
                print('deal {} error!'.format(host+uri))
                return

            # 插入数据
            text_data = [
                (filename, host+uri, result[0]),
            ]

            cursor.executemany('INSERT OR REPLACE INTO texts (filename, url, content) VALUES (?, ?, ?)', text_data)

            # 提交更改
            conn.commit()

            uri = result[1]
        else:
            print('deal {} error!'.format(host+uri))
            return

        time.sleep(1)

    # 关闭连接
    conn.close()
        
def main():
    host = 'https://www.xiaoyanwenxue.com'
    uri = '/aikan/5163343_150485760.html'
    filename = '1'

    down_text(host, uri, filename)

if __name__ == '__main__':
    main()
