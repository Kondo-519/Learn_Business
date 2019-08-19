from collections import Counter
import os
import urllib.request

class Check_LearnData(object):
    """
    学習用データの解析クラス
    """


    def __init__(self, top_number, min_freq, common_words_path, rare_words_path, stopwords_path):
        """
        解析の初期条件を決定する。

        Parameters

        ----------

        top_number : number
            上位何件まで、頻出ワードを出力するか。

        min_freq : number
            何回以下の出現数を、「Rare word」と定義するか。

        """
        self.n = top_number
        self.min_freq = min_freq
        self.common_words_path = common_words_path
        self.rare_words_path = rare_words_path
        self.stopwords_path = stopwords_path

    def output_data(self, inputDataList):
        """
        データの解析を行うクラス。解析結果は、init時に指定されたpathに書き込む。

        Parameters

        ----------

        inputDataList : list[InputData]

            解析したいInputDataのList。

        """
        #ワードの出現回数でコレクションの数をAdd
        fdist = Counter()
        for data in inputDataList:
            for word in data.keywords:
               fdist[word] += 1

        #出現回数順に要素を取得。出現回数の多いn要素のみを返す。
        common_words = {word for word, freq in fdist.most_common(self.n)}
        #出現回数がmin_freq以下の要素を取得。
        rare_words = {word for word, freq in fdist.items() if freq <= self.min_freq}
        #多すぎる要素と、少なすぎる要素を、stopwordとして定義。
        stopwords = common_words.union(rare_words)

        #画面出力ケース
        #print(fdist.most_common(self.n))
        #print('{}/{}'.format(len(stopwords), len(fdist)))

        wordcount = sum(fdist.values())
        header = '【' +inputDataList[0].category + '】 文章数：' + str(len(inputDataList)) + ' ／ ワード数：' + str(wordcount) + '\n'

        rpath = self.common_words_path
        with open(rpath, mode='a', encoding='UTF-8') as f:
            mostWD = [str(n) for n in fdist.most_common(self.n)]
            f.write(header)
            f.write('\n')
            for line in mostWD:
                f.write(inputDataList[0].category + ',' + line + '\n')
            f.write('\n')

        rpath = self.rare_words_path
        with open(rpath, mode='a', encoding='UTF-8') as f:
            rareWD = [str(n) for n in rare_words]
            f.write(header)
            f.write('\n')
            for line in rareWD:
                f.write(inputDataList[0].category + ',' + line + '\n')
            f.write('\n')

        rpath = self.stopwords_path
        with open(rpath, mode='a', encoding='UTF-8') as f:
            stpWD = [str(n) for n in stopwords]
            f.write(header)
            f.write('\n')
            for line in stpWD:
                f.write(inputDataList[0].category + ',' + line + '\n')
            f.write('\n')