from Wiki.WikiExtractor import Extractor
import re

class WikiExtractorShell(object):
    """
    Webで公開されているWikiExtractorのラッパークラス

    (参考URL)
    http://medialab.di.unipi.it/wiki/Wikipedia_Extractor
    """

    def extractText(self, wikiText):
        """
        wiki形式のテキストをプレーン形式に変換する。

        Parameters

        ----------

        wikiText : str

            変換したいwiki形式のText。


        Returns

        -------

        text : str

            変換後のText。

        """
        ex = Extractor("id", "revid", "title", wikiText)
        
        text = wikiText
        text = ex.transform(text)
        text = ex.wiki2text(text)
        text = ex.clean(text)
        text = re.sub('\\n\**','',text)
        text = re.sub('== .{,10} ==','',text)

        return text
