from bs4 import BeautifulSoup


class Document:
    def __init__(self, fileName):
        self.fileName = fileName

        soup = BeautifulSoup(open(fileName, 'rb'), 'html.parser')
        body = soup.find('body')

        # remove javascript stuff
        for script in body(['script', 'style']):
            script.decompose()

        self.htmlText = body.get_text(separator=' ')

    def getSnippet(self, index):
        text = self.htmlText[index:]
        split = text.split()

        preText = self.htmlText[: index]
        preSplit = preText.split()

        result = '... ' if len(preSplit) > 2 else ''
        result += ' '.join(word for word in preSplit[-3:])
        result += ' ' + split[0] + ' '
        result += ' '.join(word for word in split[1:4])
        result += ' ...' if len(split) > 2 else ''

        print(result)