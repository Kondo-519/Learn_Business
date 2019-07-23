from Reader.XMLreader import XMLreader
from Wiki.WikiExtractorShell import WikiExtractorShell
from MeCabShell.MeCabShell import MeCabShell
from InputData import InputData

# XML形式ファイル読み込み
rpath = r"C:\Users\0729574\Documents\ai\学習用データ_20190702再配布\学習用データ_20190702再配布\06_パルプ・紙\204427.xml"
reader = XMLreader(rpath)

# inputデータ解析（XML形式ファイル読み込み）
input = InputData("","","")

# 条件指定(tag名を指定)で要素へ順次アクセス
for result in reader.elements.getiterator('title'):
    input.title = result.text

for result in reader.elements.getiterator('text'):
    input.text = result.text


# wiki形式のテキストをプレーンテキストに変換
input.text = WikiExtractorShell.extractText(0, input.text)


# MeCabに通して形態素解析を実施
input.keywords = MeCabShell.Analysis(0,input.text)

# inputData特有のゴミデータを削除
input.setAndCleanKeywords(input.keywords)

print(input.keywords)


print(wikiDocument)
# 学習する