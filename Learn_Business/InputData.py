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

    def __init__(self, category, title, text): # 初期化： インスタンス作成時に自動的に呼ばれる
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
