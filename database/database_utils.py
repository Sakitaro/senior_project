import os
import mysql.connector

def create_database_connection():
    password = os.getenv('DB_PASSWORD')
    cnx = mysql.connector.connect(
        host='local_host',
        user='root',
        password=password,
        database='dumpdata'
    )
    return cnx

def fetch_page_title():
    cnx = create_database_connection()

    # カーソルオブジェクトを作成
    cursor = cnx.cursor()

    # SQLクエリを実行
    cursor.execute("SELECT page_title FROM red_from")

    # 結果を取得
    page_titles = cursor.fetchall()

    # データベースからの接続を閉じる
    cnx.close()

    return page_titles

def insert_links_into_database(all_red_links, all_interlanguage_links):
    cnx = create_database_connection()

    # カーソルオブジェクトを作成
    cursor = cnx.cursor()

    for red_link_title in all_red_links:
        # SQLクエリを作成
        query = "INSERT INTO red_links (title) VALUES (%s)"
        # クエリを実行
        cursor.execute(query, (red_link_title))

    for red_link_title, other_language_title, language in all_interlanguage_links:
        # SQLクエリを作成
        query = "INSERT INTO interlanguage_links (red_link_title, other_language_title, language) VALUES (%s, %s, %s))"
        # クエリを実行
        cursor.execute(query, (red_link_title, other_language_title, language))

    # 変更をコミット
    cnx.commit()

    # データベースからの接続を閉じる
    cnx.close()
