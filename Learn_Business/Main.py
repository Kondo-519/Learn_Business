from Reader.XMLreader import XMLreader
from Wiki.Extractor import Extractor
import subprocess

# 1:inputデータ解析

# ファイル読み込み
rpath = r"C:\Users\0729574\Documents\ai\学習用データ_20190702再配布\学習用データ_20190702再配布\06_パルプ・紙\204427.xml"
reader = XMLreader(rpath)

# XML形式の文章をXML形式のオブジェクトに変換
element = Extractor(reader.contents).element

wikiDocument = ""

# 条件指定(tag名を指定)で要素へ順次アクセス
for result in element.getiterator('text'):
    print(result.tag, " : " ,result.text)
    wikiDocument = result.text

# sample 要素への順次アクセス
#for child in element.getiterator():
#        print(child.tag, " : ", child.text)



# ２。無駄な要素を排除
path = ".\Wiki\WikiExtractor.py"
command = "python %s %.\Wiki\WikiExtractor.py"

subprocess.call(command.split())

subprocess.call("python %s"  % path)


# ３。MeCabに通す
  
# 学習する