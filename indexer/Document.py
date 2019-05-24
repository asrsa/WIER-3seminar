from bs4 import BeautifulSoup
import re

class Document:
    def __init__(self, fileName):
        self.path = self.getPath(fileName)

        soup = BeautifulSoup(open(self.path, 'rb'), 'html.parser')
        body = soup.find('body')

        # remove javascript stuff
        for script in body(['script', 'style']):
            script.decompose()

        for script in body(['noscript', 'style']):
            script.decompose()

        self.htmlText = body.get_text(separator=' ')

    def getPath(self, fileName):
        if 'e-prostor' in fileName:
            return 'data\e-prostor.gov.si\\' + fileName
        elif 'e-uprava' in fileName:
            return 'data\e-uprava.gov.si\\' + fileName
        elif 'evem' in fileName:
            return 'data\evem.gov.si\\' + fileName
        elif 'podatki' in fileName:
            return 'data\podatki.gov.si\\' + fileName

    def getSnippet(self, index, highlight=False):
        text = self.htmlText[index:]
        split = text.split()

        preText = self.htmlText[: index]
        preSplit = preText.split()

        snippet = '... ' if len(preSplit) > 2 else ''
        snippet += ' '.join(word for word in preSplit[-3:])

        snippet += '\033[92m' if highlight else ''
        snippet += ' ' + split[0] + ' '
        snippet += '\033[0m' if highlight else ''

        snippet += ' '.join(word for word in split[1:4])
        snippet += ' ...' if len(split) > 2 else ''

        return snippet

    def findWord(self, word):
        # indexes = [m.start() for m in re.finditer(r"[\"(\s]%s[\".!,;:?)\s«]" % word, self.htmlText, flags=re.IGNORECASE)]
        indexes = [m.start() for m in re.finditer(r"\W%s\W" % word, self.htmlText, flags=re.IGNORECASE)]
        return indexes