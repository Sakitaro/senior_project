from database.database_utils import fetch_page_title, insert_links_into_database, search_wikipedia
from scraping.redlink_filter import create_linklist

def main():
    # ページタイトルを取得
    page_titles = fetch_page_title()

    extracted_ills_list = []
    # 仮リンクたちを抽出
    for page_title in page_titles:
        extracted_contents = search_wikipedia(page_title)
        for content in extracted_contents:
            extracted_ills_list.extend(content)

    # リンクリストを作成
    # all_red_links, all_interlanguage_links = create_linklist(page_titles)

    # データベースにリンクを挿入
    insert_links_into_database(extracted_ills_list)

if __name__ == "__main__":
    main()
