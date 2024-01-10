import os
import mysql.connector
from scraping.extracted_redlinks import process_results
from mysql.connector import Error
import logging

# ログ設定
logging.basicConfig(filename='wikipedia_error.log', level=logging.ERROR, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def record_no_results(keyword):
    with open('no_results_count.txt', 'a') as file:
        file.write(f"No results found for '{keyword}'\n")
        
def create_database_connection():
    password = os.getenv('DB_PASSWORD')
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password=password,
        database='w_dumpdata'
    )
    return cnx

def fecth_redlinks_title(cnx):
    cursor = cnx.cursor()
    cursor.execute("SELECT title FROM extracted_redlinks WHERE japanese_only IS NULL")
    
    redlinks_titles = cursor.fetchall()
    
    cursor.close()
    return redlinks_titles

def check_label_exists_in_database(label, cnx):
    cursor = cnx.cursor(buffered=True)
    try:
        query = "SELECT wikidata_id, label FROM extracted_redlinks2 WHERE label = %s"
        cursor.execute(query, (label,))
        result = cursor.fetchone()
        print(result)
        return result # (wikidata_id, label) or None
    except Error as e:
        print(f"Database error : {e}")
    finally:
        cursor.close()
    

def check_label_exists(redlink_title, cnx):
    cursor = cnx.cursor(buffered=True)
    
    try:
        result = check_label_exists_in_database(redlink_title, cnx)
        
        if result:
            update_query = """
            UPDATE extracted_redlinks
            SET japanese_only = False, other_language_title = %s, language = 'wikidata'
            WHERE title = %s
            """
            cursor.execute(update_query, (result[0], redlink_title,))
            print('ok')
    except Error as e:
        print(f"Database error : {e}")
    finally:
        cursor.close()
        

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
        sql = """
        SELECT * FROM text
        INNER JOIN page ON page.text_id = text.text_id
        WHERE page.page_title = %s
        """

        cursor.execute(sql, (keyword,))
        result_text = cursor.fetchall()

        cursor.close()

        if result_text:
            extracted_contents, error_contents = process_results(result_text)
            return extracted_contents, error_contents
        else:
            record_no_results(keyword)
            return [], []
    except Error as e:
        logging.error(f"An error occurred with keyword '{keyword}': {e}", exc_info=True)        # 必要に応じてログファイルに書き込むか、例外を再度投げることもできます。
        # raise
        # エラー時の結果は空のリストやNoneで返すことも一般的です。
        return None, None

def insert_links_into_database(extracted_contents, cnx):
    cursor = cnx.cursor(buffered=True)
    for content in extracted_contents:
        try:
            title = content[0]
            language = content[1]
            other_language_title = content[2]
            # titleに一致するレコードをチェック
            cursor.execute("SELECT * FROM extracted_redlinks WHERE title = %s", (title,))
            result = cursor.fetchone()

            # レコードが存在する場合はjapanese_onlyをfalseにし、他の値を更新
            if result:
                update_query = """
                UPDATE extracted_redlinks
                SET japanese_only = %s, other_language_title = %s, language = %s
                WHERE title = %s
                """
                cursor.execute(update_query, (False, other_language_title, language, title))
            else:
                # レコードが存在しない場合は新しいレコードを挿入
                insert_query = """
                INSERT INTO extracted_redlinks (title, other_language_title, language, japanese_only)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (title, other_language_title, language, True))

        except mysql.connector.errors.DataError as e:
            # titleの長さを確認
            print(f"ここでエラー: {title}, Length: {len(title)}")
            # その他のエラー情報を出力
            print(e)
    cursor.close()
