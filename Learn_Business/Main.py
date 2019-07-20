from Reader.XMLreader import XMLreader
from Wiki.WikiExtractorShell import WikiExtractorShell
import MeCab

# 1:inputデータ解析（ファイル読み込み）
rpath = r"C:\Users\0729574\Documents\ai\学習用データ_20190702再配布\学習用データ_20190702再配布\06_パルプ・紙\204427.xml"
reader = XMLreader(rpath)

wikiDocument = ""           #読み込んだwiki形式のドキュメントを格納する変数

# 条件指定(tag名を指定)で要素へ順次アクセス
for result in reader.elements.getiterator('text'):
    wikiDocument = result.text

# sample 要素への順次アクセス
#for child in element.getiterator():
#        print(child.tag, " : ", child.text)


# ２。無駄な要素を排除
wikiDocument = WikiExtractorShell.extractText(0, wikiDocument)


# ３。MeCabに通す
tagger = MeCab.Tagger('')

node = tagger.parseToNode(wikiDocument)

#名詞リスト
keywords = []

while node:
    if node.feature.split(",")[0] == "名詞" and node.feature.split(",")[6] != "*":
        keywords.append(node.feature.split(",")[6])
        #keywords.append(node.surface)
    node = node.next


print(keywords)


print(wikiDocument)
# 学習する