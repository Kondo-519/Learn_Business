from pathlib import Path
from Reader.XMLreader import XMLreader
from InputData import InputData
import glob
import os

class FolderReader(object):
    """フォルダパス配下の全ファイルを読み込むクラス"""

    def __init__(self, folderPath):
        """

        Parameters

        ----------

        folderPath : str

            読み込み対象のフォルダパス

        """
        self.folderPath = folderPath

    def readXMLfiles(self):
        """
        フォルダ配下の.xml拡張子のファイルの中身をList形式で返却する。


        Returns

        -------

        xmlDatas : zip(str[], Element[])

            ファイルパスのListと、ElementオブジェクトのListをZip
        """
        # Pathオブジェクトを生成
        p = Path(self.folderPath)
        filePathList = list(p.glob("**/*.xml"))
        xmlDataList = []

        for path in filePathList:
            xmlDataList.append(XMLreader(path))

        xmlDatas = zip(filePathList, xmlDataList)
        return xmlDatas


    def XMLtoInputData(self, xmlDatas):
        """
        ファイルパスのListと、ElementオブジェクトのZipをInputDataのListに変換する。


        Parameters

        ----------

        xmlDatas : zip(str[], Element[])

            ファイルパスのListと、ElementオブジェクトのListをZip

        Returns

        -------

        InputDataList : InputData[]

            InputDataオブジェクトのリスト
        """
        inputDataList = []

        for (path, xml) in xmlDatas:
            #フォルダ名をカテゴリーに指定
            category = os.path.basename(path.parent)
            #先頭２文字だけ残す
            category = category[:2]
            # 条件指定(tag名を指定)で要素へ順次アクセス
            for result in xml.elements.getiterator('title'):
                title = result.text
            for result in xml.elements.getiterator('text'):
                text = result.text

            inputDataList.append(InputData(category,title,text))

        return inputDataList