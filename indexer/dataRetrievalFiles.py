import os
import time
import string
from bs4 import BeautifulSoup
from nltk import word_tokenize, FreqDist
from stopwords import stop_words_slovene

def prettyPrint():
    print('{:>0} {:>9} {:>41}'.format(*['Frequencies', 'Document', 'Snippet']))
    print("-----------  ------------------------------------------ -----------------------------------------------------------")

query = input("Input your search query.\n")
queryList = query.split()
queryList = [x.lower() for x in queryList]


wildChars = ['(','[','{','}',']',')',';','`', '``', ':', "''", ',','.']

# build list of documents
rootDirectory = 'data'
documentList = set()

def getSnippet(text, index):
    split = text.split()
    index = int(index)

    snippet = '... ' if len(split[index-3 : index]) > 2 else ''
    snippet += ' '.join(word for word in split[index-3 : index])

    snippet += '\033[92m'
    snippet += ' ' + split[index] + ' '
    snippet += '\033[0m'

    snippet += ' '.join(word for word in split[index+1 : index+4])
    snippet += ' ...' if len(split[index+1 : index+4]) > 2 else ''

    return snippet

for root, dirs, files in os.walk(rootDirectory):
    for file in files:
        # print(file)
        relativeRoot = os.path.relpath(root, rootDirectory)
        # print(relativeRoot)
        relativePath = os.path.join(rootDirectory, relativeRoot, file)
        # print(relativePath)
        if('DS_Store' not in relativePath):
            documentList.add(relativePath)

#sort by domain name & page number
documentList = sorted(documentList, key=lambda x: (x.split('.')[0], int(x.split('.')[-2])))


try:

    startTime = time.time()

    results = []
    # read all files
    for file in documentList:

        # print(file)
        soup = BeautifulSoup(open(file, 'rb'), 'html.parser')
        body = soup.find('body')

        # remove javascript stuff
        for script in body(['script', 'style']):
            script.decompose()

        for script in body(['noscript', 'style']):
            script.decompose()

        htmlText = body.get_text(separator=' ')

        word_tokens = word_tokenize(htmlText)
        word_tokens = [token.lower() for token in word_tokens]

        # removing stop words and wild chars
        filtered_text = [w for w in word_tokens if w not in stop_words_slovene and w not in wildChars]


        documentID = file.split('\\')[-1]

        wordFrequency = FreqDist(filtered_text)
        docResults = []
        for word in wordFrequency:
            if word in queryList:
                indexes = [i for i, x in enumerate(htmlText.split()) if x.translate(str.maketrans('', '', string.punctuation)).lower() == word]
                docResults.append([int(wordFrequency[word]), documentID, ' '.join(getSnippet(htmlText, index) for index in indexes)])

        # multiple hits in a document
        if len(docResults) > 0:
            results.append([sum(x[0] for x in docResults), documentID, ' '.join(((x[2] for x in docResults[:5])))])




    executionTime = int(time.time() - startTime)

    print('\nResults for query: ' + '\033[94m"' + query + '"\033[0m' + '')
    print('\nResults found in ' + str(executionTime) + 's.\n\n')

    # sort results
    results = sorted(results, key=lambda x: x[0], reverse=True)

    prettyPrint()
    for row in results:
        row = list(row)

        print('{:<12} {:<42} {:<0}'.format(*row))


except Exception as e:
    print(e)