import os
import mysql.connector
from scraping.extracted_redlinks import process_results
from mysql.connector import Error

def create_database_connection():
    password = os.getenv('DB_PASSWORD')
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password=password,
        database='w_dumpdata'
    )
    return cnx

def fetch_page_title(cnx):
    cursor = cnx.cursor()
    # SQLクエリを実行
    cursor.execute("SELECT page_title FROM red_from_unique")

    # 結果を取得
    page_titles = cursor.fetchall()
    page_titles = list(set(page_titles))

    cursor.close()
    return page_titles

def search_wikipedia(keyword, cnx):
    cursor = cnx.cursor(dictionary=True)
    try:
        # FULLTEXT検索用のSQLクエリに変更
        sql = """
        SELECT * FROM text
        INNER JOIN page ON page.text_id = text.text_id
        WHERE MATCH(page.page_title) AGAINST(%s IN BOOLEAN MODE)
        """

        cursor.execute(sql, (keyword,))
        result_text = cursor.fetchall()

        cursor.close()

        if result_text:
            extracted_contents, error_contents = process_results(result_text)
            return extracted_contents, error_contents
        else:
            print(f"No results found for '{keyword}'")
            return [], []
    except Error as e:
        print(f"An error occurred with keyword '{keyword}': {e}")
        # 必要に応じてログファイルに書き込むか、例外を再度投げることもできます。
        # raise
        # エラー時の結果は空のリストやNoneで返すことも一般的です。
        return None, None

def insert_links_into_database(extracted_contents, cnx):
    cursor = cnx.cursor()
    for content in extracted_contents:
        title = content[0]
        language = content[1]
        other_language_title = content[2]
        # titleに一致するレコードをチェック
        cursor.execute("SELECT * FROM extracted_red_links WHERE title = %s", (title,))
        result = cursor.fetchone()

        # レコードが存在する場合はjapanese_onlyをfalseにし、他の値を更新
        if result:
            update_query = """
            UPDATE extracted_red_links
            SET japanese_only = %s, other_language_title = %s, language = %s
            WHERE title = %s
            """
            cursor.execute(update_query, (False, other_language_title, language, title))
            print('できたよ')
        else:
            # レコードが存在しない場合は新しいレコードを挿入
            insert_query = """
            INSERT INTO extracted_red_links (title, other_language_title, language, japanese_only)
            VALUES (%s, %s, %s, %s)
            """
            print('新規できたよ')
            cursor.execute(insert_query, (title, other_language_title, language, True))

    cursor.close()
