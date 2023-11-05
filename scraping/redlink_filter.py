from bs4 import BeautifulSoup
import requests

# def create_linklist(page_titles):
#     all_red_linkis = []
#     all_interlanguage_links = []

#     for title in page_titles:
#       if title[0] != None:
#         title = title[0]
#         red_links, interlanguage_links = find_interlanguage_links_and_red_links('https://ja.wikipedia.org/wiki/' + title)
#         all_red_linkis.append(red_links)
#         all_interlanguage_links.append(interlanguage_links)

#     return all_red_linkis, all_interlanguage_links

# def find_interlanguage_links_and_red_links(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     red_links = []
#     interlanguage_links = []

#     for link in soup.find_all('a', class_='new'):
#         redlink_title = link.get('title')

#         next_element = link.find_next_sibling()

#         if next_element and next_element.name == 'span' and 'noprint' in next_element.get('class', []):
#             other_language_link = next_element.find('a', class_='extiw')
#             if other_language_link:
#                 other_language_title = other_language_link.get('title')
#                 language = other_language_title.split(':')[0]  # ':'より前の文字列を取得 ex/ title="en:Charles Rogier"
#                 interlanguage_links.append([redlink_title, other_language_title, language])
#             else:
#                 red_links.append(redlink_title)
#         elif next_element and next_element.name == 'a' and 'extiw' in next_element.get('class', []):
#             other_language_link = next_element
#             other_language_title = other_language_link.get('title')
#             language = other_language_title.split(':')[0]
#             interlanguage_links.append([redlink_title, other_language_title, language])
#         else:
#             red_links.append(redlink_title)

#     return red_links, interlanguage_links



