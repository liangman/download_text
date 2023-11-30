import sqlite3

def main():
    # 连接到SQLite数据库
    conn = sqlite3.connect('./example.db')
    cursor = conn.cursor()

    # 执行查询，选择所有的content字段
    cursor.execute('SELECT content FROM texts')

    # 获取查询结果
    result = cursor.fetchall()

    # 关闭数据库连接
    conn.close()

    # 拼接content字段
    concatenated_content = '\n'.join([row[0] for row in result])

    # 将拼接后的内容写入文件
    with open('1.txt', 'w', encoding='utf-8') as file:
        file.write(concatenated_content)

    print('Data has been exported to "output.txt"')

if __name__ == '__main__':
    main()
