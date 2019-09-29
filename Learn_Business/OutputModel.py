

class OutputModel(object):
    """
    モデルデータを評価し、出力するクラス
    
    Parameters

    ----------

    texts : str[][]

        モデルデータ作成元の文章データ（分かち書き済）の２次元配列。

    labels : str[]

        文書カテゴリー情報
    """

    def __init__(self, texts, labels):
        """

        Parameters

        ----------

        texts : str[][]

            モデルデータ作成元の文章データ（分かち書き済）の２次元配列。

        labels : str[]

            文書カテゴリー情報

        """
        self.texts = texts
        self.labels = labels
