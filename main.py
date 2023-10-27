from database.database_utils import fetch_page_title, insert_links_into_database
from scraping.redlink_filter import create_linklist

def main():
    # ページタイトルを取得
    page_titles = fetch_page_title()

    # リンクリストを作成
    all_red_links, all_interlanguage_links = create_linklist(page_titles)

    # データベースにリンクを挿入
    insert_links_into_database(all_red_links, all_interlanguage_links)

if __name__ == "__main__":
    main()