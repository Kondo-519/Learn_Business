import gensim
from gensim import corpora, matutils

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import pickle
import os
from pathlib import Path

## Decision Tree Model ##
from sklearn.tree import DecisionTreeClassifier

## SVM Model##
# https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html
from sklearn.svm import SVC

## Random Forest Model##
from sklearn.ensemble import RandomForestClassifier

## Naive Bayes Model##
#https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.GaussianNB.html#sklearn.naive_bayes.GaussianNB
from sklearn.naive_bayes import GaussianNB

## Logistic Regression##
from sklearn.linear_model import LogisticRegression

#評価について
#sklearnのチートシートによれば、サンプル50以下は別方式が望ましい。
#https://scikit-learn.org/stable/tutorial/machine_learning_map/
#第一候補：SVM_linear
#第二候補：ナーイブベイズ
#この二個をベースに考える。

class ModelUtil(object):
    """
    モデルデータを評価し、出力するクラス
    # 逆文章頻度で文章をベクトル化。文章の長さに結果が依存しないよう、この方式を採用。
    
    Parameters

    ----------

    texts : str[][]
        モデルデータ作成元の文章データ（分かち書き済）の２次元配列。

    train_data_std : str[][]
        モデルデータ作成元の文章データ（分かち書き済）の２次元配列。（tf-idf と 標準化済）

    labels : str[]
        文書カテゴリー情報

    X_train_std : str[][]
        評価用文章データ（標準化済）

    X_test_std : str[][]
        テスト用文章データ（標準化済）

    y_train : str[]
        評価用カテゴリーデータ

    y_test : str[]
        テスト用カテゴリーデータ

    outputFolder : Path
        出力フォルダパス
    """

    def __init__(self, texts, labels, outputPath):
        """

        Parameters

        ----------

        texts : str[][]

            モデルデータ作成元の文章データ（分かち書き済）の２次元配列。

        labels : str[]

            文書カテゴリー情報

        outputPath : str
            モデル出力先のフォルダ情報
        """
        self.texts = texts
        self.labels = labels
        
        #出力先フォルダ
        self.outputFolder = Path(outputPath)

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
        dictionary.save(os.path.join(self.outputFolder, 'dct.dict'))

        #2次元配列を作る。
        np.set_printoptions(precision=2)

        #TfidfVectorizer
        vectorizer = TfidfVectorizer(analyzer=dictionary.doc2bow, use_idf=True, token_pattern=u'(?u)\\b\\w+\\b',min_df=0.05, max_df=0.8)

        #テスト用データ作成
        train_data = vectorizer.fit_transform(np.array(texts)).toarray()
        X_train, X_test, self.y_train, self.y_test = train_test_split(train_data, labels, test_size=0.3, random_state=1)

        #標準化
        sc = StandardScaler()
        sc.fit(X_train)
        self.X_train_std = sc.transform(X_train)
        self.X_test_std = sc.transform(X_test)
        sc.fit(train_data)
        self.train_data_std = sc.transform(train_data)




    def ValueSVM(self):
        """
        SVMモデルを評価する。
        """
        #評価用モデル作成(rbf)
        model = SVC(kernel='rbf', gamma ='auto')
        model.fit(self.X_train_std, self.y_train)
        #精度確認
        score = model.score(self.X_test_std, self.y_test)
        print('SVC(rbf) score is {:.3g}'.format(score))

        #評価用モデル作成(linear)
        model = SVC(kernel='linear')
        model.fit(self.X_train_std, self.y_train)
        #精度確認
        score = model.score(self.X_test_std, self.y_test)
        print('SVC(linear) score is {:.3g}'.format(score))

    def ValueDecisionTree(self):
        """
        Decision Treeモデルを評価する。
        """
        for i in range(10):
            #評価用モデル作成(depth = i)
            model = DecisionTreeClassifier(max_depth=i+1)
            model.fit(self.X_train_std, self.y_train)

            #精度確認
            score = model.score(self.X_test_std, self.y_test)
            print('desision tree of depth' + str(i+1) + ' score is {:.3g}'.format(score))

    def ValueRandomForest(self):
        """
        RandomForestモデルを評価する。
        """
        for i in range(10):
            #評価用モデル作成(depth = i)
            model = RandomForestClassifier(max_depth=i+1, n_estimators=100)
            model.fit(self.X_train_std, self.y_train)

            #精度確認
            score = model.score(self.X_test_std, self.y_test)
            print('Random Forest of depth' + str(i+1) + ' score is {:.3g}'.format(score))

    def ValueNaiveBayes(self):
        """
        Naive Bayesモデルを評価する。
        """
        #評価用モデル作成
        model = GaussianNB()
        model.fit(self.X_train_std, self.y_train)
        #精度確認
        score = model.score(self.X_test_std, self.y_test)
        print('Naive Bayes score is {:.3g}'.format(score))

    def ValueLogistic(self):
        """
        ロジスティック回帰モデルを評価する。
        """
        #評価用モデル作成
        model = LogisticRegression(solver = 'lbfgs', multi_class='auto')
        model.fit(self.X_train_std, self.y_train)
        #精度確認
        score = model.score(self.X_test_std, self.y_test)
        print('Logistic score is {:.3g}'.format(score))

    #######ここからOutput######

    def OutputSVM(self):
        """
        SVMモデルを出力する。
        """
        model = SVC(kernel='rbf', gamma ='auto')
        model.fit(self.train_data_std, self.labels)
        filename = 'SVM_rbf_model.sav'
        pickle.dump(model, open(os.path.join(self.outputFolder, filename), 'wb'))

        model = SVC(kernel='linear', gamma ='auto')
        model.fit(self.train_data_std, self.labels)
        filename = 'SVM_linear_model.sav'
        pickle.dump(model, open(os.path.join(self.outputFolder, filename), 'wb'))

    def OutputDecisionTree(self):
        """
        Decision Treeモデルを出力する。
        """
        for i in range(10):
            #評価用モデル作成(depth = i)
            model = DecisionTreeClassifier(max_depth=i+1)
            model.fit(self.train_data_std, self.labels)

            filename = 'DecisionTree_mode_'+ str(i+1) +'.sav'
            pickle.dump(model, open(os.path.join(self.outputFolder, filename), 'wb'))

    def OutputRandomForest(self):
        """
        RandomForestモデルを出力する。
        """
        for i in range(10):
            #評価用モデル作成(depth = i)
            model = RandomForestClassifier(max_depth=i+1, n_estimators=100)
            model.fit(self.train_data_std, self.labels)

            filename = 'RandomForest_mode_'+ str(i+1) +'.sav'
            pickle.dump(model, open(os.path.join(self.outputFolder, filename), 'wb'))

    def OutputNaiveBayes(self):
        """
        NaiveBayesモデルを出力する。
        """
        model = model = GaussianNB()
        model.fit(self.train_data_std, self.labels)
        filename = 'NaiveBayes_model.sav'
        pickle.dump(model, open(os.path.join(self.outputFolder, filename), 'wb'))

    def OutputLogistic(self):
        """
        Logisticモデルを出力する。
        """
        model = model = LogisticRegression(solver = 'lbfgs', multi_class='auto')
        model.fit(self.train_data_std, self.labels)
        filename = 'Logistic_model.sav'
        pickle.dump(model, open(os.path.join(self.outputFolder, filename), 'wb'))

    #######ここからAll#######

    def ValueAllModel(self):
        """
        全てのモデルを評価する。

        """
        self.ValueSVM()
        self.ValueDecisionTree()
        self.ValueRandomForest()
        self.ValueNaiveBayes()
        self.ValueLogistic()

    def OutputAllModel(self):
        """
        全てのモデルを出力する。

        """
        self.OutputSVM()
        self.OutputDecisionTree()
        self.OutputRandomForest()
        self.OutputNaiveBayes()
        self.OutputLogistic()
