import xml.etree.ElementTree as ET

class XMLreader(object):
    """description of class"""

    def __init__(self, file_path):
        """
        Parameters
        ----------
        file_path : str
            読み込み先のファイルパス。フルパスで指定。

        contents :
            ファイルの中身。まとめて。

        elements :
            ファイルの中身をElementオブジェクトに変換したもの。
        """
        # ファイルをオープンする
        test_data = open(file_path, "r" ,encoding="utf-8")

        # ファイルをすべて読み込んでデータにする
        self.contents = test_data.read()

        # XML形式の文章をXML形式のオブジェクトに変換
        self.elements = ET.fromstring(self.contents)

        # ファイルをクローズする
        test_data.close()
