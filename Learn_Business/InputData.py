import re
import os


class InputData(object):
    """
    主催者提供の「学習用データ」格納クラス
    
    Parameters

    ----------

    category : int

        対象のカテゴリーNo(ex.31_情報・通信なら、31)。

    title : str

        企業名
    text : str

        説明文
    keywords : str[]
        プレーンなTextに変換し、形態素解析を行った主語の配列
    """

    def __init__(self, category, title, text):
        """

        Parameters

        ----------

        category : int

            対象のカテゴリーNo(ex.31_情報・通信なら、31)。

        title : str

            企業名
        text : str

            説明文

        """
        self.category = category
        self.title = title
        self.text = text

    def setAndCleanKeywords(self, keywords):
        """
        keywordの配列をクレンジングしながらセットする。所謂、ストップワードの排除。

        Parameters

        ----------

        keywords : str[]

            クレンジング対象のキーワード群

        """
        self.keywords = keywords
        #末尾に「。」が付くワードの無害化
        #pattern = ".+。$"
        #self.keywords = [item[:-1] for item in self.keywords if not re.match(pattern, item)]

        #２byte文字の1byte化

        #Stopword辞書からストップワードを排除
        base = os.path.dirname(os.path.abspath(__file__))
        name = os.path.normpath(os.path.join(base, '.\stopwords.txt'))

        with open(name) as f:
            stopwords = f.read()
            stopwords = stopwords.split()

        self.keywords = [item for item in self.keywords if not item in stopwords]

        #正規表現でひっかけるパターンの作成

        #YYYY年、MM月、MM月DD日の排除
        pattern = '[0-9]+年|[0-9]+月|[0-9]+月[0-9]+日'
        #平成元年など和暦の排除
        pattern += '|' + '(昭和|平成|大正|明治)(元|[0-9]+)年'
        #%、X割の排除
        pattern += '|' + '([0-9]+\.[0-9]+|[0-9]+)(%|割)'
        #金額の排除
        pattern += '|' + '[0-9]+(億|億円)|[0-9]+(万|万円)|[0-9]+円'
        #X位、X番、X号、X[距離]の排除
        pattern += '|' + '[0-9]+(位|番|号|部|km|m|cm|)'
        #負数の排除
        pattern += '|' + '(－|−|-)[0-9]+'
        #大文字数字の排除
        pattern += '|' + '\d+'

        #不要ワードの削除
        self.keywords = [item for item in self.keywords if not re.match(pattern, item)]
