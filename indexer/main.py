import os
import sqlite3
from bs4 import BeautifulSoup
from nltk import word_tokenize, FreqDist

# build list of documents
rootDirectory = 'data'
documentList = set()

for root, dirs, files in os.walk(rootDirectory):
    for file in files:
        # print(file)
        relativeRoot = os.path.relpath(root, rootDirectory)
        # print(relativeRoot)
        relativePath = os.path.join(rootDirectory, relativeRoot, file)
        # print(relativePath)
        documentList.add(relativePath)

# processing documents
for file in documentList:
    print(file, end="\t")
    soup = BeautifulSoup(open(file, 'rb'), 'html.parser')
    body = soup.find('body')
    htmlText = body.get_text()

    word_tokens = word_tokenize(htmlText)
    word_tokens = [token.lower() for token in word_tokens]
    print('word tokens: ' + str(len(word_tokens)))

    try:
        documentID = file.split('\\')[2]
        # print(documentID)
        wordFrequency = FreqDist(word_tokens)
        # print(wordFrequency.keys())
        # for key in wordFrequency:
        #     print(str(key) + ': ' + str(wordFrequency[key]))

        # db connection
        con = sqlite3.connect('db/database')
        cur = con.cursor()

        for word in wordFrequency:
            # this should go somewhere in this part here
            # indices = [i for i, x in enumerate(my_list) if x == word]

            # and this?
            # [m.start() for m in re.finditer('test', 'test test test test')]
            # #[0, 5, 10, 15]

            # insert into IndexWord
            # added 'IGNORE' to avoid 'UNIQUE constraint failed: IndexWord.word' error
            sql = """INSERT OR IGNORE INTO IndexWord (word) values (?)"""
            cur.execute(sql, (word,))
            con.commit()

            # insert into posting
            sql = """INSERT into Posting(word, documentName, frequency, indexes)
                     VALUES (?,?,?,?)"""
            cur.execute(sql, (word, documentID, wordFrequency[word], 'OH NO, INDEXES MUST BE OBTAINED SOMEHOW'))
            con.commit()
        cur.close()
    except Exception as e:
        print('Fuck, sth went wrong!')
        print(e)
