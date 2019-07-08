from Reader.XMLreader import XMLreader
from Wiki.Extractor import Extractor

# 1:inputデータ解析

# ファイル読み込み
rpath = r"X:\Projects\test.xml"
reader = XMLreader(rpath)

# XML形式の文章をXML形式のオブジェクトに変換
element = Extractor(reader.contents).element

# 条件指定(tag名を指定)で要素へ順次アクセス
for result in element.getiterator('text'):
    print(result.tag, " : " ,result.text)


# sample 要素への順次アクセス
#for child in element.getiterator():
#        print(child.tag, " : ", child.text)



# ２。無駄な要素を排除



# ３。MeCabに通す
  
# 学習する