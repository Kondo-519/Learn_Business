import MeCab

class MeCabShell(object):
    """
    MeCabのラッパークラス
    
    """

    def Analysis(self, text):
        """
        形態素解析（morphological analysis）を実施する。

        Parameters

        ----------

        text : str

            形態素解析（morphological analysis）対象のText。


        Returns

        -------

        keywords : str[]

            主語のみを抽出したワードのリスト

        """
        # MeCabに通して形態素解析を実施
        tagger = MeCab.Tagger('')
        node = tagger.parseToNode(text)

        #名詞リスト
        keywords = []

        while node:
            if node.feature.split(",")[0] == "名詞" and node.feature.split(",")[6] != "*":
                #keywords.append(node.surface)
                keywords.append(node.feature.split(",")[6])
            node = node.next

        return keywords