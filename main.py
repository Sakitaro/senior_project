from database.database_utils import create_database_connection, fetch_page_title, insert_links_into_database, search_wikipedia, fecth_redlinks_title, check_label_exists, update_magnitude_title
from mysql.connector import Error
from pymagnitude import Magnitude
from tqdm import tqdm



# def main():
#     # データベース接続を開始
#     cnx = create_database_connection()
#     error_logs = []

#     try:
#         # ページタイトルを取得
#         page_titles = fetch_page_title(cnx)

#         # 仮リンクたちを抽出
#         for page_title_tuple in page_titles:
#             page_title = page_title_tuple[0]
#             extracted_contents, error_contents = search_wikipedia(page_title, cnx)
#             if error_contents:
#                 error_logs.append(error_contents)
#             if extracted_contents:
#                 insert_links_into_database(extracted_contents, cnx)

#         cnx.commit()

#     except Error as e:
#         cnx.rollback()
#         raise e
#     finally:
#         # エラーが発生してもしなくても接続を閉じる
#         cnx.close()
#         if error_logs:
#             print("Error logs:")
#             for log in error_logs:
#                 print(log)

# def main():
#     # データベース接続を開始
#     cnx = create_database_connection()
#     error_logs = []

#     try:
#         # redlink titleを取得
#         redlinks_titles = fecth_redlinks_title(cnx)

#         # wikidataにラベルが存在するか確認
#         for redlink_title_tuple in redlinks_titles:
#             redlink_title = redlink_title_tuple[0]
#             check_label_exists(redlink_title, cnx)

#         cnx.commit()
#     except Error as e:
#         cnx.rollback()
#         error_logs.append(str(e))
#     finally:
#         cnx.close()
#         if error_logs:
#             print("Error logs:")
#             for log in error_logs:
#                 print(log)
from threading import Thread
from queue import Queue
from tqdm import tqdm

path = "~/wikipedia/model.magnitude"
wv = Magnitude(path)

def worker(queue):
    while True:
        redlink_title = queue.get()
        if redlink_title is None:  # Noneがキューに追加されたら終了
            break
        try:
            update_magnitude_title(redlink_title, wv)
        except Exception as e:
            print(f"Error processing {redlink_title}: {e}")
        queue.task_done()

def main():
    cnx = create_database_connection()
    error_logs = []
    redlinks_titles = fecth_redlinks_title(cnx)
    total_items = len(redlinks_titles)
    cnx.close()

    # スレッドとキューの設定
    queue = Queue()
    threads = [Thread(target=worker, args=(queue,)) for _ in range(12)]

    # スレッドの開始
    for t in threads:
        t.start()

    # タスクのキューへの追加
    for title in redlinks_titles:
        queue.put(title[0])

    # 進捗バーの表示
    with tqdm(total=total_items) as pbar:
        while total_items > 0:
            queue.get()
            pbar.update(1)
            total_items -= 1

    # スレッドの終了
    for _ in threads:
        queue.put(None)
    for t in threads:
        t.join()

    if error_logs:
        for log in error_logs:
            print(log)

if __name__ == "__main__":
    main()


# def main():
#     # データベース接続を開始
#     cnx = create_database_connection()
#     error_logs = []
#     # データのPATH
#     path = "~/wikipedia/model.magnitude"
#     wv = Magnitude(path)

#     try:
#         # redlink titleを取得
#         redlinks_titles = fecth_redlinks_title(cnx)
#         # 処理する項目の総数を取得
#         total_items = len(redlinks_titles)

#         print(total_items)

#         # for redlink_title_tuple in redlinks_titles:
#         for i in tqdm(range(total_items)):
#             redlink_title = redlinks_titles[i][0]
#             # redlink_title = redlink_title_tuple[0]
#             # 新しい関数をここで実行
#             update_magnitude_title(redlink_title, cnx, wv)
#     except Error as e:
#         error_logs.append(str(e))
#     finally:
#         cnx.close()
#         if error_logs:
#             print("Error logs:")
#             for log in error_logs:
#                 print(log)


if __name__ == "__main__":
    main()
