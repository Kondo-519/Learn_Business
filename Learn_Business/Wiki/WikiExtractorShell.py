from Wiki.WikiExtractor import Extractor
import Wiki.WikiExtractor
import re

class WikiExtractorShell(object):
    """
    Webで公開されているWikiExtractorのラッパークラス

    (参考URL)
    http://medialab.di.unipi.it/wiki/Wikipedia_Extractor
    """

    def extractText(self, wikiText):
        """
        :param wikiText: wiki形式のテキスト
        """
        ex = Extractor("id", "revid", "title", wikiText)
        
        wikiText = ex.transform(wikiText)
        wikiText = ex.wiki2text(wikiText)
        wikiText = ex.clean(wikiText)
        wikiText = re.sub('\\n\**','',wikiText)
        wikiText = re.sub('== .{,10} ==','',wikiText)

        return wikiText
