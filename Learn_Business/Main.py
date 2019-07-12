from Reader.XMLreader import XMLreader
from Wiki.WikiExtractor import Extractor
from Wiki.WikiExtractor import compact
from Wiki.WikiExtractorShell import WikiExtractorShell
import subprocess


# 1:inputデータ解析

# ファイル読み込み
rpath = r"C:\Users\0729574\Documents\ai\学習用データ_20190702再配布\学習用データ_20190702再配布\06_パルプ・紙\204427.xml"
reader = XMLreader(rpath)

wikiDocument = ""

# 条件指定(tag名を指定)で要素へ順次アクセス
for result in reader.elements.getiterator('text'):
    print(result.tag, " : " ,result.text)
    wikiDocument = result.text

# sample 要素への順次アクセス
#for child in element.getiterator():
#        print(child.tag, " : ", child.text)


# ２。無駄な要素を排除
wikiDocument = WikiExtractorShell.extractText(0, wikiDocument)

# ３。MeCabに通す
 
print(wikiDocument)

# 学習する