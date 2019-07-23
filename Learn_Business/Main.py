from Reader.XMLreader import XMLreader
from Reader.FolderReader import FolderReader
from Wiki.WikiExtractorShell import WikiExtractorShell
from MeCabShell.MeCabShell import MeCabShell
from InputData import InputData
import sys

#一時的
from collections import Counter
import os
import urllib.request

#引数check
if len(sys.argv) < 2 :
    print("引数が指定されていません。読み取り対象のフォルダパスを引数として指定してください。")
    sys.exit

# XML形式ファイル読み込み
xmlDataList = FolderReader(sys.argv[1]).readXMLfiles()
inputDataList = FolderReader.XMLtoInputData(0, xmlDataList)

# wiki形式のテキストをプレーンテキストに変換
for data in inputDataList:
    data.text = WikiExtractorShell.extractText(0, data.text)

# MeCabに通して形態素解析を実施
for data in inputDataList:
    data.keywords = MeCabShell.Analysis(0,data.text)

# inputData特有のゴミデータを削除
for data in inputDataList:
    data.setAndCleanKeywords(data.keywords)

#ワードの出現回数でコレクションの数をAdd
fdist = Counter()
for data in inputDataList:
    for word in data.keywords:
       fdist[word] += 1

n=100
min_freq=1
common_words = {word for word, freq in fdist.most_common(n)}
rare_words = {word for word, freq in fdist.items() if freq <= min_freq}
stopwords = common_words.union(rare_words)
print(fdist.most_common(n))
print('{}/{}'.format(len(stopwords), len(fdist)))

rpath = r"C:\Users\0729574\Documents\ai\output.txt"

with open(rpath, mode='a') as f:
    f.write('\n')
    f.write(inputDataList[0].category)
    f.write('\n')
    #f.write('most_words:' + fdist.most_common(n))
    f.write('\n')
    f.write('--------')

print(wikiDocument)
# 学習する