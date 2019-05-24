import sqlite3
import time
from Document import Document

def prettyPrint():
    print('{:>0} {:>9} {:>41}'.format(*['Frequencies', 'Document', 'Snippet']))
    print("-----------  ------------------------------------------ -----------------------------------------------------------")

query = input("Input your search query.\n")
queryList = query.split()

try:
    # db connection
    con = sqlite3.connect('db/database')
    cur = con.cursor()

    sql = """SELECT SUM(frequency) AS 'frequencies', documentName, group_concat(indexes) FROM Posting
             WHERE """ + "or ".join(["word LIKE ? "] * len(queryList)) + """
             GROUP BY documentName
             ORDER BY frequencies DESC"""

    startTime = time.time()

    cur.execute(sql, queryList)
    results = cur.fetchall()

    executionTime = int((time.time() - startTime) * 1000)

    print('\nResults for query: ' + '\033[94m"' + query + '"\033[0m' + '')
    print('\nResults found in ' + str(executionTime) + 'ms.\n\n')

    prettyPrint()
    for row in results:
        row = list(row)
        doc = Document(row[1])


        indices = row[2].split(',', 5)
        row[2] = " ".join(doc.getSnippet(int(index), True) for index in indices[:5])

        print('{:<12} {:<42} {:<0}'.format(*row))


    cur.close()
except Exception as e:
    print(e)