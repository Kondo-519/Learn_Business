from Reader.FolderReader import FolderReader
from Wiki.WikiExtractorShell import WikiExtractorShell
from MeCabShell.MeCabShell import MeCabShell
from InputData import InputData
from Check_LearnData import Check_LearnData
from ModelUtil import ModelUtil
import sys


#引数check
if len(sys.argv) < 3 :
    print("【Warn】引数が指定されていません。読み取り対象のフォルダパスと出力先のフォルダパスを引数として指定してください。")
    sys.exit

# XML形式ファイル読み込み
xmlDataList = FolderReader(sys.argv[1]).readXMLfiles()
inputDataList = FolderReader.XMLtoInputData(0, xmlDataList)

#読み込み結果チェック
if len(inputDataList) < 1 :
    print("【Warn】xmlファイルの読み込みに失敗しました。正しいフォルダパスが引数に設定されているか確認して下さい。")
    sys.exit


# wiki形式のテキストをプレーンテキストに変換
for data in inputDataList:
    data.text = WikiExtractorShell.extractText(0, data.text)

# MeCabに通して形態素解析を実施
for data in inputDataList:
    data.keywords = MeCabShell.Analysis(0,data.text)

# inputData特有のゴミデータを削除
for data in inputDataList:
    data.setAndCleanKeywords(data.keywords)

# 旧ソース：傾向分析は終了したためコメントアウト。
# データの傾向分析用データを出力する。
#cld = Check_LearnData(100,1,r'C:\Users\0729574\Documents\ai\common_words.txt', r'C:\Users\0729574\Documents\ai\rarewords.txt', r'C:\Users\0729574\Documents\ai\stopwords.txt')
#cld.output_data(inputDataList)

# 旧ソース：傾向分析は終了したためコメントアウト。
#分析その２
#Analyzer.explore_data.plot_sample_length_distribution_inputData(inputDataList)

# 文章データを配列化。
texts = []
for data in inputDataList:
    texts.append(data.keywords) # extendなら、配列が入れ子にならない(入れ子はappend）

# ラベルデータを配列化
labels = [data.category for data in inputDataList]

#モデルを作成・評価・出力
models = ModelUtil(texts, labels, sys.argv[2])
models.ValueAllModel()
models.OutputAllModel()