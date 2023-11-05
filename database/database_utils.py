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

def search_wikipedia(keyword):
    try:
        cnx = create_database_connection()
        cursor = cnx.cursor(dictionary=True)

        # FULLTEXT検索用のSQLクエリに変更
        sql = """
        SELECT * FROM text
        INNER JOIN page ON page.text_id = text.text_id
        WHERE MATCH(page.page_title) AGAINST(%s IN BOOLEAN MODE)
        """

        # FULLTEXT検索の場合、like_patternは不要
        # 代わりにキーワードをそのまま使用
        cursor.execute(sql, (keyword,))
        result_text = cursor.fetchall()
        cursor.close()
        cnx.close()

        if result_text:
            print('good')
            extracted_contents = process_results(result_text)
            return extracted_contents
        else:
            print(f"No results found for '{keyword}'")
            return []
    except Error as e:
        print(f"An error occurred with keyword '{keyword}': {e}")
        # 必要に応じてログファイルに書き込むか、例外を再度投げることもできます。
        # raise
        # エラー時の結果は空のリストやNoneで返すことも一般的です。
        return None

def fetch_page_title():
    cnx = create_database_connection()

    # カーソルオブジェクトを作成
    cursor = cnx.cursor()

    # SQLクエリを実行
    cursor.execute("SELECT page_title FROM red_from_unique")

    # 結果を取得
    page_titles = cursor.fetchall()
    page_titles = list(set(page_titles))

    # データベースからの接続を閉じる
    cnx.close()

    return page_titles

def insert_links_into_database(extracted_ills_list):
    cnx = create_database_connection()

    # カーソルオブジェクトを作成
    cursor = cnx.cursor()

    # extracted_ills_list をループ処理
    for title, other_language_title, language in extracted_ills_list:
        # titleに一致するレコードをチェック
        cursor.execute("SELECT * FROM extracted_red_links WHERE title = %s", (title,))
        result = cursor.fetchone()
        test = 0
        if not result:
            test += 1

        # # レコードが存在する場合はjapanese_onlyをfalseにし、他の値を更新
        # if result:
        #     update_query = """
        #     UPDATE extracted_red_links
        #     SET japanese_only = %s, other_language_title = %s, language = %s
        #     WHERE title = %s
        #     """
        #     cursor.execute(update_query, (False, other_language_title, language, title))
        # else:
        #     # レコードが存在しない場合は新しいレコードを挿入
        #     insert_query = """
        #     INSERT INTO extracted_red_links (title, other_language_title, language, japanese_only)
        #     VALUES (%s, %s, %s, %s)
        #     """
        #     cursor.execute(insert_query, (title, other_language_title, language, True))

    print(test)

    # 変更をコミット
    cnx.commit()

    # データベースからの接続を閉じる
    cnx.close()
