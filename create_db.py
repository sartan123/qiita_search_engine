import re
import sys
import json
import MeCab
import requests
from bs4 import BeautifulSoup


def create_database(url, main_url):
    result_dic = {}
    try:
        m = MeCab.Tagger(' -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    except:
        m = MeCab.Tagger('')
    for i in range(1, 300):
        if i >= 2:
            sub_url = url + '?page=' + str(i)
        else:
            sub_url = url
        try:
            resource = BeautifulSoup(requests.get(sub_url).text, "lxml")
        except:
            break

        for i, j in zip(resource.find_all("a", class_="u-link-no-underline"), resource.find_all('ul', class_="ItemLink__status")):
            target_url = main_url + i['href']
            target_title = i.text
            m.parse('')
            node = m.parseToNode(target_title)

            pattern = r"</span>(\s[0-9]+)</li>"
            favo = re.search(pattern, str(j))
            if favo != None:
                favo = int(favo.group(1))
            else:
                favo = 0

            while node:
                if node.feature.split(',')[0] == '名詞':
                    if node.surface not in result_dic:
                        result_dic[node.surface] = []
                        result_dic[node.surface].append({"title": target_title, "url": target_url, "favo": favo})
                    else:
                        result_dic[node.surface].append({"title": target_title, "url": target_url, "favo": favo})
                node = node.next
    return result_dic


def search_to_and_words(result_dic, search_word):
    common_url = []
    for word in search_word:
        word_url = []
        word_url = seach_to_word(result_dic, word)
        common_url.append(word_url)
    return list(set(common_url[0]) & set(common_url[1]))


def seach_to_word(result_dic, word):
    favo_list = []
    for i in sorted(result_dic[word], key=lambda x: x[2], reverse=True):
        favo_url = {}
        favo_url['title'] = i[0]
        favo_url['url'] = i[1]
        favo_list.append(favo_url)
    return favo_list


def run():
    tag = sys.argv[1]
    url = "https://qiita.com/tags/{}/items".format(tag)
    main_url = "https://qiita.com/"
    result_dic = create_database(url, main_url)
    return result_dic

if __name__ == '__main__':
    file = open('./search_engine/db/{}.json'.format(sys.argv[1]), 'w')
    json.dump(run(), file)
