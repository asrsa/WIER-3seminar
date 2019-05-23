from bs4 import BeautifulSoup

# select sum(frequency) as 'frequencies', documentName,  group_concat(indexes) from Posting
# where word like 'sistem' or word like 'spot'
# group by documentName
# order by frequencies DESC

class Document:
    def __init__(self, fileName):
        self.fileName = fileName

        soup = BeautifulSoup(open(fileName, 'rb'), 'html.parser')
        body = soup.find('body')

        # remove javascript stuff
        for script in body(['script', 'style']):
            script.decompose()

        for script in body(['noscript', 'style']):
            script.decompose()

        self.htmlText = body.get_text(separator=' ')

    def getSnippet(self, index, highlight):
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