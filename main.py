from database.database_utils import create_database_connection, fetch_page_title, insert_links_into_database, search_wikipedia
from mysql.connector import Error


def main():
    # データベース接続を開始
    cnx = create_database_connection()
    error_logs = []

    try:
        # ページタイトルを取得
        page_titles = fetch_page_title(cnx)

        # 仮リンクたちを抽出
        for page_title_tuple in page_titles:
            page_title = page_title_tuple[0]
            extracted_contents, error_contents = search_wikipedia(page_title, cnx)
            print(extracted_contents)
            if error_contents:
                error_logs.append(error_contents)
            if extracted_contents:
                insert_links_into_database(extracted_contents, cnx)

        cnx.commit()

    except Error as e:
        cnx.rollback()
        raise e
    finally:
        # エラーが発生してもしなくても接続を閉じる
        cnx.close()
        if error_logs:
            print("Error logs:")
            for log in error_logs:
                print(log)


if __name__ == "__main__":
    main()
