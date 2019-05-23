from nltk.tokenize import word_tokenize
from stopwords import stop_words_slovene
from bs4 import BeautifulSoup
import sqlite3
from Document import Document


tmp = Document('data\e-uprava.gov.si\e-uprava.gov.si.45.html')
print(tmp.getSnippet(3539, True))


wildChars = ['(','[','{','}',']',')',';','`', '``', ':', "''", ',','.']

example_text = "»Program projektov eProstor« (en prostor za vse) ima specifični cilj zagotoviti večjo preglednost in učinkovitost pri urejanju prostora, graditvi objektov in upravljanju nepremičnin. Osnovni namen je pospešiti in izboljšati procese pri prostorskem načrtovanju, graditvi objektov in upravljanju z nepremičninami, kar je mogoče doseči s povezljivimi, enostavno dostopnimi in zanesljivimi zbirkami prostorskih podatkov."

soup = BeautifulSoup(open('data/e-prostor.gov.si/e-prostor.gov.si.1.html', 'rb'), 'html.parser')
body = soup.find('body')


#remove javascript stuff
for script in body(['script', 'style']):
    script.decompose()


htmlText = body.get_text(separator=' ')



word_tokens = word_tokenize(htmlText)
word_tokens = [token.lower() for token in word_tokens]


filtered_text = [w for w in word_tokens if w not in stop_words_slovene and w not in wildChars]

# for w in filtered_text:
#    print(w)

print(len(word_tokens))
print(len(filtered_text))

try:
    # TODO - do this part in some loop
    document = 'document_created_by_my_brain2'
    word = 'test3'

    con = sqlite3.connect('db/database')
    cur = con.cursor()

    # check if word is already in dictionary
    sql = """SELECT word FROM IndexWord where word like ?"""
    cur.execute(sql, (word,))
    data = cur.fetchone()
    print(data)

    # if word exists -> modify record in table posting
    if data is not None:
        # obtain record in tale posting
        sql = """SELECT * from Posting where word like ? and documentName like ?"""
        cur.execute(sql, (data[0], document))
        wordData = cur.fetchone()
        print(wordData)

        wordID = wordData[0]                # word
        documentID = wordData[1]            # document
        frequency = wordData[2]             # frequency
        indexes = wordData[3]               # list of indexes

        # update word record
        # TODO how to obtain index of word? -> for now fixed index of '123' will be inserted into record
        sql = """UPDATE Posting set frequency=?, indexes=?
                 where word like ? and documentName like ?"""
        cur.execute(sql, (frequency+1, indexes + ',123', wordID, documentID))
        con.commit()

    # if word does not exist -> create new record in table posting
    else:
        print('word does not exist in dictionary. Creating new record ...')
        # insert into IndexWord
        sql = """INSERT INTO IndexWord (word) values (?)"""
        cur.execute(sql, (word, ))
        con.commit()

        # insert into posting
        sql = """INSERT into Posting(word, documentName, frequency, indexes)
                 VALUES (?,?,?,?)"""
        # TODO how to calculate correct index -> for now fixed index of '42' will be inserted into record
        cur.execute(sql, (word, document, 1, '42'))
        con.commit()
    cur.close()
except Exception as e:
    print(e)


