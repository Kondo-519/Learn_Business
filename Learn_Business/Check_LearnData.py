from collections import Counter
import os
import urllib.request

class Check_LearnData(object):
    """description of class"""


    def __init__(self, top_number, min_freq, output_path1, output_path2):
        self.n = top_number
        self.min_freq = min_freq
        self.output_path1 = output_path1
        self.output_path2 = output_path2

    def output_data(self, inputDataList):
        #ワードの出現回数でコレクションの数をAdd
        fdist = Counter()
        for data in inputDataList:
            for word in data.keywords:
               fdist[word] += 1

        #n=100
        #min_freq=1
        common_words = {word for word, freq in fdist.most_common(self.n)}
        rare_words = {word for word, freq in fdist.items() if freq <= self.min_freq}
        stopwords = common_words.union(rare_words)
        print(fdist.most_common(self.n))
        print('{}/{}'.format(len(stopwords), len(fdist)))

        rpath = self.output_path1

        with open(rpath, mode='a', encoding='UTF-8') as f:
            mostWD = [str(n) for n in fdist.most_common(self.n)]
            for line in mostWD:
                f.write(inputDataList[0].category + ',' + line + '\n')
            f.write('\n')

        rpath = self.output_path2

        with open(rpath, mode='a', encoding='UTF-8') as f:
            stpWD = [str(n) for n in stopwords]
            for line in stpWD:
                f.write(inputDataList[0].category + ',' + line + '\n')
            f.write('\n')