class XMLreader(object):
    """description of class"""

    def __init__(self, file_path):
        """
        Parameters
        ----------
        file_path : 
            読み込み先のファイルパス。フルパスで指定。

        lines : 
            ファイルの中身。１行ずつ。
        """
        # ファイルをオープンする
        test_data = open(file_path, "r" ,encoding="utf-8")

        # 行ごとにすべて読み込んでリストデータにする
        self.lines = test_data.readlines()

        # ファイルをクローズする
        test_data.close()
