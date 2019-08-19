from Reader.FolderReader import FolderReader
from Wiki.WikiExtractorShell import WikiExtractorShell
from MeCabShell.MeCabShell import MeCabShell
from InputData import InputData
from Check_LearnData import Check_LearnData
#import Analyzer.explore_data
import sys

#一時的


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

# データの傾向分析用データを出力する。
cld = Check_LearnData(100,1,r'C:\Users\0729574\Documents\ai\common_words.txt', r'C:\Users\0729574\Documents\ai\rarewords.txt', r'C:\Users\0729574\Documents\ai\stopwords.txt')
cld.output_data(inputDataList)

#分析その２
#Analyzer.explore_data.plot_sample_length_distribution_inputData(inputDataList)

# 学習する

test = 1