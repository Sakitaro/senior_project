from database.database_utils import create_database_connection, fetch_page_title, insert_links_into_database, search_wikipedia
from mysql.connector import Error


def main():
    # データベース接続を開始
    cnx = create_database_connection()
    cursor = cnx.cursor()

    try:
        # ページタイトルを取得
        page_titles = fetch_page_title(cursor)

        # 仮リンクたちを抽出
        for page_title_tuple in page_titles:
            page_title = page_title_tuple[0]
            extracted_contents = search_wikipedia(page_title, cursor)
            print(extracted_contents)
            insert_links_into_database(extracted_contents, cursor)

        cnx.commit()

    except Error as e:
        cnx.rollback()
        raise e
    finally:
        # エラーが発生してもしなくても接続を閉じる
        cursor.close()
        cnx.close()


if __name__ == "__main__":
    main()
