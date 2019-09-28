from Reader.FolderReader import FolderReader
from Wiki.WikiExtractorShell import WikiExtractorShell
from MeCabShell.MeCabShell import MeCabShell
from InputData import InputData
from Check_LearnData import Check_LearnData
#import Analyzer.explore_data
import sys

#一時的
import gensim
from gensim import corpora, matutils

from sklearn.feature_extraction.text import TfidfVectorizer

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

# 旧ソース：傾向分析は終了したためコメントアウト。
# データの傾向分析用データを出力する。
#cld = Check_LearnData(100,1,r'C:\Users\0729574\Documents\ai\common_words.txt', r'C:\Users\0729574\Documents\ai\rarewords.txt', r'C:\Users\0729574\Documents\ai\stopwords.txt')
#cld.output_data(inputDataList)

# 旧ソース：傾向分析は終了したためコメントアウト。
#分析その２
#Analyzer.explore_data.plot_sample_length_distribution_inputData(inputDataList)

# 学習する
# 逆文章頻度で文章をベクトル化。文章の長さに結果が依存しないよう、この方式を採用。

# DictDataをoutput
# https://qiita.com/u6k/items/5170b8d8e3f41531f08a

# extendなら、配列が入れ子にならない(入れ子はappend）
texts = []
for data in inputDataList:
    texts.append(data.keywords)
#texts = [texts.append(data.keywords) for data in inputDataList]

#Dcitionaryを作成(https://qiita.com/tatsuya-miyamoto/items/f505dfa8d5307f8c6e98)
#Dcitionary.token2id : 単語/idの辞書データ
#Dcitionary.token2id : id/df値(出現文書数)の辞書データ
dictionary = corpora.Dictionary(texts)
#単語データをフィルタリング。
#no_below: 「出現文書数≥指定値」になるような語のみを保持する（一定回数以下のゴミワードを削除）。
#no_above: 「出現文書数/全文書数≤指定値」になるような語のみを保持する（多すぎるワードを削除）。
#num_docs : 辞書作成に用いた全文章数
#num_pocs : 辞書作成に用いた全単語数
dictionary.filter_extremes(no_below = 5, no_above = 0.5)

#ベクトル化
def vec2dense(vec, num_terms):
    return list(matutils.corpus2dense([vec], num_terms=num_terms).T[0])
data_all = [vec2dense(dictionary.doc2bow(texts[i]), len(dictionary)) for i in range(len(texts))]

#TfidfVectorizer
vectorizer = TfidfVectorizer(use_idf=True, token_pattern=u'(?u)\\b\\w+\\b')
vecs = vectorizer.fit_transform(texts)

# コーパス作成(文章ごとに「単語ID・出現頻度」タプル配列を持つデータ
corpus = [dictionary.doc2bow(data.keywords) for data in inputDataList]
#corpora.MmCorpus.serialize(r'C:\Users\0729574\Documents\ai\2.mm', corpus)



test = 1