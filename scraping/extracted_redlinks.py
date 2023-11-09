import re
from database.languages import known_languages

def extract_templates(text, template_names):
    # いくつかのテンプレート名を含む正規表現を構築する
    pattern = r'\{\{(' + '|'.join(re.escape(name) for name in template_names) + r')(.*?)\}\}'
    return re.findall(pattern, text, re.DOTALL)

def process_results(text):
    for row in text:
        text_id = row['text_id']
        text_body = row['text_body'].decode('utf-8')

        templates = extract_templates(text_body, ['ill2', '仮リンク'])
        extracted_contents = extract_template_content(templates)
        return extracted_contents

def extract_template_content(templates):
    extracted_contents = []
    error_contents = []
    for template in templates:
        template_content = template[1].strip('{}')
        content_list = [item.strip() for item in template_content.split('|')]
         # 最初の要素はテンプレート名なので除外
        content_list = content_list[1:]

        if len(content_list) <= 2:
            error_contents.append(content_list)
            continue

        # label=で始まる要素を除外
        content_list = [item for item in content_list if not item.startswith('label=')]

        # 3つの要素だけ取得
        content_list = content_list[:3]

        if len(content_list) < 3 or None in content_list:
            error_contents.append(content_list)
            continue

        # 初期化
        title = content_list[0] if len(content_list) > 0 else None
        other_language_link = content_list[2] if len(content_list) > 2 else None

        if content_list[1].lower() in known_languages:
            language = content_list[1].lower()
       # もし1番目の要素が言語コードでない場合、他の要素と交換
        else:
            if title.lower() in known_languages:
                # タイトルと言語コードが入れ替わっている場合
                language, title = title.lower(), content_list[1]
            elif other_language_link.lower() in known_languages:
                # 他言語リンクと言語コードが入れ替わっている場合
                language, other_language_link = other_language_link.lower(), content_list[1]
            else:
                # 言語コードが見つからない場合はエラーリストに追加
                error_contents.append(content_list)
                continue

        # 言語コードが見つかればリストに追加
        if title and language and other_language_link:
            extracted_contents.append([title, language, other_language_link])
        else:
            error_contents.append(content_list)


    return extracted_contents, error_contents
