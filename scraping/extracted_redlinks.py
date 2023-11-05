import re

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
    for template in templates:
        template_content = template[1].strip('{}')
        content_list = [item.strip() for item in template_content.split('|')]
        # 最初の要素を無視して次の3つの要素のみを取得
        # テンプレートによっては3つ未満の要素しかない場合があるので、その場合のエラーを避ける
        content_list = content_list[1:4] if len(content_list) > 3 else content_list[1:]
        extracted_contents.append(content_list)

    return extracted_contents
# [
#     ['en', 'Article1', '記事１'],
#     ['ワムパム・ベルト', 'en', 'Wampum']
# ]



